# VectorStore 模块文档

## 功能描述
`VectorStore` 是 LangChain 中所有向量数据库（如 Chroma, FAISS, Pinecone 等）的标准接口。它负责存储文档及其对应的向量嵌入（Embeddings），并提供基于相似度的检索功能。

向量存储是 RAG（检索增强生成）系统的核心组件，用于高效地从海量非结构化数据中查找相关上下文。

---

### 4. 核心方法 (Core Methods)

#### similarity_search
- **功能描述**: 返回与查询最相似的文档。
- **参数说明**:
  - `query` (str): 查询文本。
  - `k` (int): 返回的文档数量，默认为 4。
  - `**kwargs`: 传递给搜索方法的其他参数。
- **返回值**: `List[Document]`，最相似的文档列表。

#### asimilarity_search (Async)
- **功能描述**: `similarity_search` 的异步版本。
- **参数说明**: 同 `similarity_search`。
- **返回值**: `Awaitable[List[Document]]`。

#### similarity_search_with_score
- **功能描述**: 返回与查询最相似的文档及其相似度分数（通常是距离）。
- **参数说明**:
  - `query` (str): 查询文本。
  - `k` (int): 返回的文档数量。
  - `**kwargs`: 其他参数。
- **返回值**: `List[Tuple[Document, float]]`，包含文档和对应分数的元组列表。

#### similarity_search_with_relevance_scores
- **功能描述**: 返回文档及其相关性分数，分数范围在 `[0, 1]` 之间（1 表示最相关）。
- **参数说明**:
  - `query` (str): 查询文本。
  - `k` (int): 返回数量。
  - `score_threshold` (float, 可选): 最小相关性阈值。
- **返回值**: `List[Tuple[Document, float]]`。

#### add_documents
- **功能描述**: 将 `Document` 对象列表添加到向量存储中。
- **参数说明**:
  - `documents` (List[Document]): 文档列表。
  - `**kwargs`: 其他参数。
- **返回值**: `List[str]`，添加文档的 ID 列表。

#### as_retriever
- **功能描述**: 将向量存储转换为 `BaseRetriever` 对象，以便在 LCEL 中使用。
- **参数说明**:
  - `search_type` (str): 搜索类型，如 `"similarity"`, `"mmr"`, `"similarity_score_threshold"`。
  - `search_kwargs` (dict): 传递给搜索方法的参数。
- **返回值**: `VectorStoreRetriever`。

### 5. 代码示例 (Code Examples)

#### 基础用法示例
```python
from langchain_core.vectorstores import VectorStore
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# 1. 准备数据
texts = ["LangChain 是一个开发 LLM 应用的框架", "向量数据库用于存储嵌入向量"]
embeddings = OpenAIEmbeddings()

# 2. 创建向量存储
vectorstore = FAISS.from_texts(texts, embeddings)

# 3. 执行相似度搜索
query = "什么是 LangChain？"
docs = vectorstore.similarity_search(query, k=1)

for doc in docs:
    print(f"内容: {doc.page_content}")
    print(f"元数据: {doc.metadata}")

# 4. 转换为检索器
retriever = vectorstore.as_retriever(search_kwargs={"k": 1})
result = retriever.invoke(query)
```

#### 异步搜索示例
```python
import asyncio
from langchain_community.vectorstores import Qdrant

async def async_search():
    # 假设 vectorstore 已经初始化
    query = "异步搜索示例"
    docs = await vectorstore.asimilarity_search(query, k=2)
    for doc in docs:
        print(doc.page_content)

# asyncio.run(async_search())
```

### 6. 注意事项 (Notes)
- **分数含义**: 不同向量数据库对 `score` 的定义不同（有的是欧氏距离，有的是余弦相似度）。`similarity_search_with_relevance_scores` 尝试将其标准化为 `[0, 1]`。
- **性能优化**: 对于大规模数据，建议使用支持持久化和索引优化的向量数据库（如 Pinecone, Milvus, Weaviate, Chroma）。
- **异步支持**: 并非所有向量存储实现都原生支持异步。对于不支持的，LangChain 会在线程池中运行同步方法以模拟异步。
