# langchain_core.output_parsers.xml

## 文件概述
`xml.py` 提供了将语言模型输出解析为 XML 格式的功能。它不仅支持解析完整的 XML 字符串，还支持流式解析（Streaming Parsing），能够随着模型的输出实时构建和 yield 已完成的 XML 节点。

---

## 导入依赖
| 模块 | 作用 |
| :--- | :--- |
| `xml.etree.ElementTree` | Python 标准库中的 XML 处理模块，用于核心解析逻辑。 |
| `defusedxml` | (可选) 安全增强版 XML 解析库，用于防御 XML 漏洞（如实体扩展攻击）。 |
| `re` | 用于在文本中定位 XML 块及处理编码声明。 |
| `langchain_core.output_parsers.transform` | 导入 `BaseTransformOutputParser` 以支持流式解析。 |

---

## 类与函数详解

### 1. XMLOutputParser
**功能描述**: 将 LLM 输出转换为 Python 字典。它通过正则表达式提取三反引号内的 XML 块，并支持递归地将 XML 树映射为嵌套字典。

#### 属性
| 属性名 | 类型 | 默认值 | 详细用途 |
| :--- | :--- | :--- | :--- |
| `tags` | `list[str] \| None` | `None` | 期望模型输出的 XML 标签列表，用于生成格式指令。 |
| `parser` | `Literal["defusedxml", "xml"]` | `"defusedxml"` | 指定底层的 XML 解析引擎。推荐使用 `defusedxml` 以保证安全性。 |

#### 核心方法
- **`get_format_instructions`**: 生成提示语，告知模型必须遵循的 XML 结构。
- **`parse`**:
    - **步骤 1**: 查找文本中的 ```xml ... ``` 块。
    - **步骤 2**: 清理编码声明。
    - **步骤 3**: 调用底层解析引擎（`defusedxml` 或 `xml`）将字符串转换为 `Element` 对象。
    - **步骤 4**: 调用 `_root_to_dict` 将 XML 树转换为字典。

---

### 2. _StreamingParser (内部类)
**功能描述**: 实现 XML 的增量解析。它利用 `ET.XMLPullParser` 监听 `start` 和 `end` 事件。

#### 核心方法
- **`parse`**: 接收文本块并喂给 `pull_parser`。当检测到 `end` 事件且该路径下没有未闭合的子节点时，yield 当前解析出的完整元素。

---

## 核心逻辑
1. **安全解析**: 默认使用 `defusedxml`。如果环境中未安装该库，且用户显式要求使用它，解析器会抛出 `ImportError` 并提供安装建议。
2. **字典映射规则 (`_root_to_dict`)**:
    - 如果节点仅包含文本且无子节点：返回 `{tag: text}`。
    - 如果节点包含子节点：返回 `{tag: [{child1_tag: child1_val}, ...]}`。
3. **流式触发**: 流式解析器会跟踪当前路径。只有当一个标签完全闭合（收到 `end` 事件）时，才会将该节点及其内容作为字典输出。

---

## 使用示例

### 基本使用
```python
from langchain_core.output_parsers import XMLOutputParser

parser = XMLOutputParser(tags=["book", "author", "title"])
xml_text = """
<book>
    <author>J.K. Rowling</author>
    <title>Harry Potter</title>
</book>
"""
result = parser.invoke(xml_text)
print(result)
# 输出: {'book': [{'author': 'J.K. Rowling'}, {'title': 'Harry Potter'}]}
```

### 流式解析
```python
# 模拟流式输出
chunks = ["<book>", "<title>LangChain", " Guide</title>", "</book>"]
for part in parser.transform(chunks):
    print(part)
# 输出:
# {'book': [{'title': 'LangChain Guide'}]}
```

---

## 注意事项
- **三反引号支持**: 解析器会尝试提取 ` ```xml ` 或 ` ``` ` 包裹的内容，这增加了对模型输出格式不规范的容错性。
- **安全警告**: 如果使用原生 `xml` 解析器，请确保输入来源可信，以防止 XML 外部实体（XXE）攻击。
- **嵌套限制**: `_root_to_dict` 的转换逻辑相对简单，可能无法完美映射所有复杂的 XML Schema（如属性处理）。

---

## 内部调用关系
- `XMLOutputParser` 依赖于 `_StreamingParser` 来实现其 `_transform` 和 `_atransform` 逻辑。
- 使用 `AddableDict` 作为流式输出的容器，便于后续可能的累加操作。

---

## 元信息
- **最后更新时间**: 2026-01-29
- **对应源码版本**: LangChain Core v1.2.7
