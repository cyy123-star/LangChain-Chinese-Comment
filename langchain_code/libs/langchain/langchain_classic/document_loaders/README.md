# Document Loaders (文档加载器)

`document_loaders` 模块负责从各种不同的数据源（如本地文件、网页、数据库、第三方 API 等）加载内容，并将其统一转换为 LangChain 的 `Document` 对象。

## 核心接口

### `BaseLoader`
所有加载器的抽象基类。主要方法包括：
- `load()`: 加载数据并返回一个 `Document` 对象列表。
- `lazy_load()`: 延迟加载数据，适用于处理超大规模数据集。

## Document 对象结构
每个 `Document` 包含两个部分：
1. `page_content`: 文档的原始文本内容（字符串）。
2. `metadata`: 文档的元数据（字典），如文件名、页码、URL、发布时间等。

## 常用加载器

| 类别 | 示例 | 说明 |
| :--- | :--- | :--- |
| **本地文件** | `TextLoader`, `PyPDFLoader`, `CSVLoader`, `UnstructuredWordDocumentLoader` | 处理各种常见的文档格式。 |
| **网络资源** | `WebBaseLoader`, `SitemapLoader`, `RecursiveUrlLoader` | 爬取网页内容。 |
| **云服务** | `S3FileLoader`, `GCSDirectoryLoader`, `GoogleDriveLoader` | 从云存储加载。 |
| **第三方平台** | `WikipediaLoader`, `ArxivLoader`, `GitHubLoader`, `NotionDirectoryLoader` | 从特定 API 获取结构化数据。 |

## 使用示例

```python
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("example.pdf")
docs = loader.load()

# 查看第一个文档的内容和元数据
print(docs[0].page_content[:100])
print(docs[0].metadata)
```

## 迁移指南

- **集成分离**: 绝大多数具体的加载器实现现在都位于 `langchain-community` 中。
- **Unstructured**: 许多复杂的文档解析（如 PDF 中的表格提取）依赖于 `unstructured` 库。
- **RAG 流程**: 文档加载器通常是 RAG 流程的第一步，后续接 `TextSplitter` 进行文本切分。
