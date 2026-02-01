# Vector Stores (向量数据库)

`vectorstores` 模块提供了与各种向量数据库（Vector Databases）交互的统一接口。它允许开发者存储经过嵌入（Embedding）处理的文档，并根据语义相似度进行高效检索。

## 核心接口

### `VectorStore`
所有向量数据库的基类。常用方法包括：
- `add_documents(documents)`: 将带元数据的文档存入数据库。
- `similarity_search(query, k=4)`: 查找与查询最相似的前 K 个文档。
- `as_retriever()`: 将向量数据库转换为 `Retriever` 对象，方便在 Chain 中使用。

## 常见实现

| 数据库 | 类型 | 特点 |
| :--- | :--- | :--- |
| `Chroma` | 本地/开源 | 简单易用，适合开发和测试环境。 |
| `FAISS` | 本地/开源 | 由 Meta 开发，极其高效的相似度搜索库。 |
| `Pinecone` | 托管服务 | 生产级云原生向量数据库。 |
| `Milvus` | 开源/集群 | 专为大规模向量数据设计的开源数据库。 |
| `Redis` | 内存数据库 | 支持向量搜索插件，响应速度极快。 |
| `Elasticsearch` | 搜索引擎 | 强大的全文检索 + 向量搜索能力。 |

## 检索算法

- **Similarity Search**: 纯向量距离计算。
- **Max Marginal Relevance (MMR)**: 在保证相关性的同时，尽量增加返回文档的多样性，避免信息冗余。
- **Self-Querying**: 能够将自然语言查询解析为结构化的元数据过滤器。

## 使用示例

```python
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

vectorstore = FAISS.from_texts(
    ["LangChain is a framework", "Vector stores are cool"],
    OpenAIEmbeddings()
)

# 搜索
docs = vectorstore.similarity_search("What is LangChain?")
```

## 迁移指南

- **集成分离**: 绝大多数向量数据库实现现在都位于 `langchain-community` 或特定的第三方包中（如 `langchain-chroma`）。
- **LangGraph**: 在构建复杂的 RAG 应用时，向量数据库通常作为 Graph 中的一个 Node 或 Tool 使用。
