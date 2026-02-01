# langchain_text_splitters.html

`html.py` 提供了针对 HTML 文档的结构化切分功能。它能够识别 HTML 标签（如 `<h1>` 到 `<h6>`），并根据这些标签将网页内容切分为带有层级元数据的文档块。

## **文件概述**
该文件主要实现了 `HTMLHeaderTextSplitter` 类。与普通的文本切分器不同，它利用 HTML 的 DOM 结构来保留文档的语义层次，非常适合处理网页爬虫抓取的内容。

## **导入依赖**
- `bs4 (BeautifulSoup)`: 用于解析 HTML DOM 树（必需依赖）。
- `lxml`: 可选的高性能 HTML 解析引擎。
- `langchain_core.documents.Document`: 标准文档对象。

## **类与函数详解**

### **HTMLHeaderTextSplitter (类)**
**功能描述**：根据指定的 HTML 标题标签切分 HTML 内容，并将这些标题信息作为元数据附加到生成的 Document 中。

#### **构造函数 `__init__`**
| 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `headers_to_split_on` | `list[tuple]` | 无 | 是 | 需要切分的标签及其对应的元数据键。如 `[("h1", "Header 1"), ("h2", "Header 2")]`。 |
| `return_each_element` | `bool` | `False` | 否 | 是否将每个检测到的元素作为独立文档返回。 |

#### **核心方法**
- **`split_text(text: str) -> list[Document]`**:
    - **功能**: 解析 HTML 字符串。它会遍历 DOM 树，根据指定的 `headers_to_split_on` 标签来划分区块。
- **`split_text_from_url(url: str) -> list[Document]`**:
    - **功能**: 从指定的 URL 下载并切分 HTML 内容。

## **核心逻辑解析**
1. **DOM 遍历**：该切分器不是基于正则表达式，而是使用 BeautifulSoup 解析完整的 DOM 树。它会跟踪当前遍历到的最高级别标题，并将其后的所有内容归属于该标题。
2. **元数据继承**：类似于 Markdown 切分器，它会维护一个上下文环境。例如，一个在 `<h1>` 和 `<h2>` 之后的 `<p>` 标签，其生成的文档将包含这两个层级的标题信息。
3. **清洗与提取**：在切分过程中，它会自动去除 HTML 标签，只保留纯文本内容，同时保持结构的语义。

## **使用示例**
```python
from langchain_text_splitters import HTMLHeaderTextSplitter

html_string = """
<!DOCTYPE html>
<html>
<body>
    <div>
        <h1>LangChain 简介</h1>
        <p>LangChain 是一个开发 LLM 应用的框架。</p>
        <div>
            <h2>核心模块</h2>
            <p>包括 Model I/O, Retrieval, Chains 等。</p>
            <h3>切分器</h3>
            <p>HTML 切分器是 Retrieval 模块的一部分。</p>
        </div>
    </div>
</body>
</html>
"""

headers_to_split_on = [
    ("h1", "Header 1"),
    ("h2", "Header 2"),
    ("h3", "Header 3"),
]

splitter = HTMLHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
docs = splitter.split_text(html_string)

for doc in docs:
    print(f"Content: {doc.page_content}")
    print(f"Metadata: {doc.metadata}")
    print("-" * 20)
```

## **注意事项**
- 必须安装 `beautifulsoup4` 包。
- 如果 HTML 结构不规范（如标题标签嵌套混乱），切分结果可能不符合预期。
- 它只处理 `headers_to_split_on` 中指定的标签。其他标签（如 `<div>`, `<span>`）会被视为普通内容容器。

## **相关链接**
- [BeautifulSoup 官方文档](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [MarkdownHeaderTextSplitter 文档](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/text-splitters/langchain_text_splitters/markdown.md#2-markdownheadertextsplitter-类)
