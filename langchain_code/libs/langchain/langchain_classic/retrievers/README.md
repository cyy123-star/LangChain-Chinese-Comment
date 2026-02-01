# Retrievers (检索器)

`retrievers` 模块定义了如何根据非结构化查询获取相关文档的逻辑。与 `VectorStore` 不同，检索器不需要具备存储功能，它只负责“获取”这一动作。

## 核心接口

### `BaseRetriever`
定义了 `get_relevant_documents(query)` 方法。它是 RAG 流程中模型获取外部知识的标准化入口。

## 检索增强技术

### 1. 组合与重排 (Ensemble & Rerank)
- `EnsembleRetriever`: 结合多个检索器（如 BM25 和 向量检索）的结果。
- **Rerank (重排序)**: 使用交叉编码器（Cross-Encoder）或专用 API（如 Cohere Rerank）对初步检索结果进行精准排序。

### 2. 上下文压缩 (Contextual Compression)
- `ContextualCompressionRetriever`: 自动提取文档中与查询最相关的部分，减少输入 LLM 的 Token 数量。

### 3. 查询转换 (Query Transformation)
- `MultiQueryRetriever`: 将一个查询生成多个变体，从不同角度检索。
- `ParentDocumentRetriever`: 检索小的文本块以保证相关性，但返回其所属的完整父文档以提供完整上下文。
- `SelfQueryRetriever`: 将自然语言查询转换为包含元数据过滤器的结构化查询。

## 常用检索器实现

| 类型 | 说明 |
| :--- | :--- |
| `VectorStoreRetriever` | 最基础的检索器，包装自向量数据库。 |
| `BM25Retriever` | 基于关键词匹配的经典检索算法（不需要 Embedding）。 |
| `ArxivRetriever` | 从 Arxiv 论文库检索。 |
| `WikipediaRetriever` | 从维基百科检索。 |
| `TavilySearchAPIRetriever` | 专为 AI 代理优化的互联网搜索检索。 |

## 使用示例

```python
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
docs = retriever.invoke("What are the benefits of LCEL?")
```

## 迁移指南

- **集成分离**: 具体的检索器实现现在多位于 `langchain-community`。
- **LCEL**: 检索器在 LCEL 中被视为 `Runnable`，可以直接参与管道：`{"context": retriever, "question": RunnablePassthrough()} | prompt | llm`。
