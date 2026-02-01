# langchain_text_splitters.markdown

`markdown.py` 专门用于处理 Markdown 格式的文本切分。它不仅支持按字符切分，还提供了强大的按标题（Headers）切分的功能，能够将 Markdown 结构转化为带有层级元数据的文档。

## **文件概述**
该文件定义了两个核心类：
1. **MarkdownTextSplitter**: 继承自 `RecursiveCharacterTextSplitter`，预设了适用于 Markdown 的分隔符。
2. **MarkdownHeaderTextSplitter**: 一个独立的切分器，专门根据 Markdown 的标题（如 `#`, `##`）来切分文档，并将标题内容存入 `Document` 的元数据中。

## **导入依赖**
- `re`: 正则表达式，用于解析 Markdown 语法。
- `langchain_core.documents.Document`: 基础文档对象。
- `langchain_text_splitters.character.RecursiveCharacterTextSplitter`: 递归字符切分器。

## **类与函数详解**

### **1. MarkdownTextSplitter (类)**
**功能描述**：一种预配置的递归切分器。它使用 Markdown 特有的分隔符（如标题、代码块、列表项等）来尝试保持文本块的结构完整性。

---

### **2. MarkdownHeaderTextSplitter (类)**
**功能描述**：根据 Markdown 标题层级进行切分。这在构建知识库时非常有用，因为它可以保持段落与其所属章节标题的关联。

#### **构造函数 `__init__`**
| 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `headers_to_split_on` | `list[tuple]` | 无 | 是 | 定义需要切分的标题级别及其在元数据中的键名。例如 `[("#", "Header 1"), ("##", "Header 2")]`。 |
| `return_each_line` | `bool` | `False` | 否 | 是否按行返回。 |
| `strip_headers` | `bool` | `True` | 否 | 切分后是否从正文中移除标题行。 |
| `custom_header_patterns`| `dict` | `None` | 否 | 自定义标题模式（如 `**Header**`）。 |

#### **核心方法**
- **`split_text(text: str) -> list[Document]`**:
    - **功能**: 执行切分。它会遍历每一行，维护一个标题栈（header stack），并根据当前行是否为标题来更新元数据。
- **`aggregate_lines_to_chunks(lines) -> list[Document]`**:
    - **功能**: 内部方法。将具有相同元数据（即属于同一层级标题下）的连续行合并为单个 `Document`。

## **核心逻辑解析**
1. **标题追踪**：`MarkdownHeaderTextSplitter` 并不只是简单地切开文本。它会记录当前所在的各级标题。例如，如果你在 `## Section 2` 下，生成的 `Document` 元数据会包含 `{"Header 1": "Chapter 1", "Header 2": "Section 2"}`。
2. **代码块保护**：在解析标题时，代码块（` ``` ` 或 ` ~~~ `）内部的内容会被视为普通文本，即使包含 `#` 也不会被误判为标题。
3. **元数据传播**：这种切分方式确保了每个文本块都携带了其完整的上下文路径，极大提高了向量搜索后的回答质量。

## **使用示例**

### **按标题切分并提取元数据**
```python
from langchain_text_splitters import MarkdownHeaderTextSplitter

markdown_document = """
# 介绍
这是关于 LangChain 的介绍。

## 核心组件
### Text Splitter
切分器是关键组件。

### Memory
内存用于持久化对话。
"""

headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]

splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
docs = splitter.split_text(markdown_document)

for doc in docs:
    print(f"Content: {doc.page_content}")
    print(f"Metadata: {doc.metadata}")
    print("-" * 20)
```

## **注意事项**
- `MarkdownHeaderTextSplitter` 返回的是 `Document` 对象列表，而 `MarkdownTextSplitter.split_text` 返回的是字符串列表。
- 如果标题行没有紧跟空格（例如 `#Header` 而不是 `# Header`），默认情况下可能无法识别，除非它是自定义模式。
- 建议先使用 `MarkdownHeaderTextSplitter` 按语义结构切分大块，然后再对过大的块使用 `RecursiveCharacterTextSplitter` 进行二次切分。

## **相关链接**
- [RecursiveCharacterTextSplitter 文档](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/text-splitters/langchain_text_splitters/character.md#2-recursivecharactertextsplitter-类)
- [LangChain 官方 RAG 指南](https://python.langchain.com/docs/modules/data_connection/document_transformers/post_processors/header_metadata_splitter/)
