# langchain_core.output_parsers.list

## 文件概述
`list.py` 包含一系列用于将模型输出解析为列表格式的解析器。这些解析器能够处理逗号分隔、编号列表以及 Markdown 列表等常见的文本结构，并支持流式输出。

---

## 导入依赖
| 模块 | 作用 |
| :--- | :--- |
| `csv` | 用于处理逗号分隔值（CSV）的解析。 |
| `re` | 提供正则表达式支持，用于匹配列表模式。 |
| `io.StringIO` | 将字符串包装为类文件对象，供 `csv.reader` 使用。 |
| `langchain_core.output_parsers.transform` | 导入 `BaseTransformOutputParser` 以支持流式解析。 |

---

## 类与函数详解

### 1. ListOutputParser (抽象基类)
**功能描述**: 所有列表解析器的基类。它实现了流式解析的核心逻辑，能够将逐步生成的文本流切分为独立的列表项。

#### 核心方法
- **`parse` (抽象方法)**: 将完整文本解析为字符串列表。
- **`_transform`**: 实现流式转换。它维护一个缓冲区，利用 `parse_iter` 或 `parse` 尝试从不完整的文本中提取已完成的列表项并立即 yield。

---

### 2. CommaSeparatedListOutputParser
**功能描述**: 将模型输出解析为逗号分隔的列表（CSV 格式）。

#### 核心方法
- **`get_format_instructions`**: 返回提示语：“Your response should be a list of comma separated values, eg: `foo, bar, baz`”。
- **`parse`**: 使用 `csv.reader` 处理文本。它支持带引号的字符串和空格过滤。

---

### 3. NumberedListOutputParser
**功能描述**: 解析带数字编号的列表（例如 `1. item1\n2. item2`）。

#### 属性
| 属性名 | 类型 | 默认值 | 详细用途 |
| :--- | :--- | :--- | :--- |
| `pattern` | `str` | `r"\d+\.\s([^\n]+)"` | 用于匹配编号及后续内容的正则表达式。 |

---

### 4. MarkdownListOutputParser
**功能描述**: 解析 Markdown 格式的无序列表（使用 `-` 或 `*` 作为前缀）。

#### 属性
| 属性名 | 类型 | 默认值 | 详细用途 |
| :--- | :--- | :--- | :--- |
| `pattern` | `str` | `r"^\s*[-*]\s([^\n]+)$"` | 用于匹配 Markdown 列表项的正则表达式。 |

---

## 核心逻辑
1. **流式分块**: `ListOutputParser` 在流式模式下非常智能。它不会等到整个列表生成完才输出，而是会监测文本中的分隔符（如换行或逗号）。
2. **缓冲区管理**: 解析器会将未完成解析的片段保留在 `buffer` 中，直到下一个块到达并补全该列表项。
3. **健壮性**: `CommaSeparatedListOutputParser` 优先使用 `csv` 模块以正确处理包含逗号的加引号字符串，如果失败则回退到简单的 `.split(",")`。

---

## 使用示例

### 逗号分隔列表解析
```python
from langchain_core.output_parsers import CommaSeparatedListOutputParser

parser = CommaSeparatedListOutputParser()
result = parser.invoke("苹果, 香蕉, 橙子")
print(result) # ['苹果', '香蕉', '橙子']
```

### Markdown 列表解析（流式）
```python
from langchain_core.output_parsers import MarkdownListOutputParser

parser = MarkdownListOutputParser()
# 模拟流式输入
chunks = ["- 选项 A\n", "- 选项 B\n", "- 选项 C"]
for list_chunk in parser.transform(chunks):
    print(f"提取到项: {list_chunk}")
# 输出:
# 提取到项: ['选项 A']
# 提取到项: ['选项 B']
# 提取到项: ['选项 C']
```

---

## 注意事项
- **提示语的重要性**: 列表解析器非常依赖 `get_format_instructions()` 提供的指令。如果模型不遵循特定格式（如漏掉编号），解析可能会失败或丢失数据。
- **空白处理**: 默认情况下，大多数解析器会去除列表项两端的空白。

---

## 内部调用关系
- 继承自 `BaseTransformOutputParser`，确保其可以作为 LCEL 链的一部分。
- 被 `langchain` 主包中的许多高层工具所引用。

---

## 元信息
- **最后更新时间**: 2026-01-29
- **对应源码版本**: LangChain Core v1.2.7
