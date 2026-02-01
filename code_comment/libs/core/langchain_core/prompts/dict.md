# dict.py

## 文件概述
`dict.py` 模块定义了 `DictPromptTemplate` 类，这是一种基于字典结构的提示词模板。与生成单一字符串或消息列表的模板不同，`DictPromptTemplate` 允许开发者定义一个复杂的嵌套字典结构作为模板，并能递归地替换其中字符串值里的变量占位符。

该类特别适用于需要向模型传递结构化配置、JSON 对象或多模态数据（如包含图像 URL 的字典）的场景。

---

## 导入依赖
- `langchain_core.load`: 用于对象的序列化与反序列化。
- `langchain_core.prompts.string`: 复用模板变量提取逻辑（`get_template_variables`）和格式化映射。
- `langchain_core.runnables`: 继承自 `RunnableSerializable`，支持 LCEL 链式调用。

---

## 类与函数详解

### 1. `DictPromptTemplate` (类)
以字典形式表示的提示词模板。

#### 属性说明
| 属性名 | 类型 | 默认值 | 是否必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `template` | `dict[str, Any]` | - | 是 | 作为模板的字典对象。其中的字符串值可以包含变量（如 `{var}`）。 |
| `template_format` | `Literal["f-string", "mustache"]` | - | 是 | 模板语法格式。注意此处不支持 `jinja2`。 |

#### 核心方法
- `input_variables` (property): 递归遍历 `template` 字典，提取所有嵌套字符串中的变量名。
- `format`: 将输入变量填充到字典模板中，返回一个新的格式化后的字典。
- `invoke`: 实现 Runnable 接口，允许将该模板作为链的一个环节调用。

---

### 2. 辅助函数

#### `_get_input_variables` (递归函数)
深度优先搜索字典模板，提取所有字符串值中的变量占位符。它会处理嵌套的字典、列表和元组。

#### `_insert_input_variables` (递归函数)
将实际的输入值插入到字典模板中。
- **安全性逻辑**：如果字典中包含 `image_url` 且其中有 `path` 字段，会发出安全警告（类似于 `image.py` 的处理逻辑，防范文件读取漏洞）。

---

## 核心逻辑特点
1. **递归处理**：能够处理任意深度的嵌套字典和列表。
2. **仅针对值**：变量占位符仅在字典的 **值（Value）** 中被识别和替换，**键（Key）** 不会被当作模板处理。
3. **LCEL 集成**：由于继承自 `RunnableSerializable`，它可以无缝集成到 LangChain 的表达语言中，作为处理结构化输入/输出的中间层。

---

## 使用示例
```python
from langchain_core.prompts import DictPromptTemplate

# 定义字典模板
template = {
    "user_info": {
        "name": "{name}",
        "action": "greeting"
    },
    "metadata": ["id_{id}", "type_user"]
}

prompt = DictPromptTemplate(
    template=template,
    template_format="f-string"
)

# 格式化
result = prompt.format(name="Alice", id="001")
print(result)
# 输出: 
# {
#     "user_info": {"name": "Alice", "action": "greeting"},
#     "metadata": ["id_001", "type_user"]
# }
```

---

## 内部调用关系
- **继承关系**: `DictPromptTemplate` -> `RunnableSerializable[dict, dict]`。
- **依赖关系**: 依赖 `langchain_core.prompts.string` 进行底层的模板变量解析。

---

## 相关链接
- [LangChain 官方文档 - Runnables](https://python.langchain.com/docs/expression_language/interface)
- [langchain_core.prompts.string 源码](./string.py)

---
**对应源码版本**: LangChain Core v1.2.7
**最后更新时间**: 2026-01-29
