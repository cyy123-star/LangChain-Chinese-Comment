# InMemoryVectorStore 模块文档

## 文件概述
`in_memory.py` 实现了 LangChain 的内存向量存储（`InMemoryVectorStore`）。它是一个轻量级的向量数据库实现，将文档及其向量嵌入存储在 Python 字典中，并使用 NumPy 计算余弦相似度进行检索。该组件非常适合快速原型开发、单元测试或小型数据集的本地处理。

## 导入依赖
- `numpy`: 用于向量计算和相似度比较。
- `uuid`: 用于为新添加的文档生成唯一 ID。
- `langchain_core.documents`: 引入 `Document` 类。
- `langchain_core.vectorstores`: 继承 `VectorStore` 基类。
- `langchain_core.load`: 支持序列化和反序列化。

## 类与函数详解

### 1. InMemoryVectorStore
**功能描述**: 提供基于内存的向量存储功能。它支持添加文档、删除文档、按 ID 获取文档以及多种搜索模式（相似度搜索、带分数的搜索、MMR 搜索等）。

#### 核心属性
- `store`: `dict[str, dict[str, Any]]` - 内部存储字典，键为文档 ID，值为包含向量、文本和元数据的字典。
- `embedding`: `Embeddings` - 用于将文本转换为向量的嵌入模型。

#### 核心方法
- **`add_documents(documents, ids=None, **kwargs)`**:
    - **功能**: 将文档列表添加到存储中。如果未提供 ID，则自动生成 UUID。
    - **参数**:
        | 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
        | :--- | :--- | :--- | :--- | :--- |
        | `documents` | `list[Document]` | - | 是 | 要存储的文档对象列表。 |
        | `ids` | `list[str]` | `None` | 否 | 对应的文档 ID 列表。 |
    - **返回值**: `list[str]` - 成功添加的文档 ID 列表。

- **`similarity_search_with_score(query, k=4, **kwargs)`**:
    - **功能**: 根据查询文本查找最相似的 `k` 个文档及其相似度分数。
    - **参数**:
        | 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
        | :--- | :--- | :--- | :--- | :--- |
        | `query` | `str` | - | 是 | 查询字符串。 |
        | `k` | `int` | `4` | 否 | 返回的结果数量。 |
    - **返回值**: `list[tuple[Document, float]]` - 文档及其相似度分数的元组列表。

- **`max_marginal_relevance_search(query, k=4, fetch_k=20, lambda_mult=0.5, **kwargs)`**:
    - **功能**: 执行最大边际相关性（MMR）搜索，在保证相关性的同时增加结果的多样性。
    - **参数**:
        | 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
        | :--- | :--- | :--- | :--- | :--- |
        | `query` | `str` | - | 是 | 查询字符串。 |
        | `k` | `int` | `4` | 否 | 最终返回的结果数量。 |
        | `fetch_k` | `int` | `20` | 否 | 初始获取的候选文档数量。 |
        | `lambda_mult` | `float` | `0.5` | 否 | 多样性权重（0-1），值越小多样性越高。 |
    - **返回值**: `list[Document]` - 经过 MMR 筛选后的文档列表。

- **`dump(path)` / `load(path, embedding)`**:
    - **功能**: 将内存中的数据保存到本地 JSON 文件或从文件加载。
    - **参数**: `path` (str) - 文件路径。

## 核心逻辑
1. **相似度计算**: 使用 `numpy` 计算查询向量与存储向量之间的点积，并除以模的乘积得到余弦相似度。
2. **过滤机制**: 支持传入自定义的 `filter` 函数，在计算相似度前对 `Document` 对象进行筛选。
3. **MMR 算法**: 先通过相似度搜索获取 `fetch_k` 个候选，再通过 `maximal_marginal_relevance` 算法平衡相关性和冗余，选出最终的 `k` 个结果。

## 使用示例
```python
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

# 初始化
vector_store = InMemoryVectorStore(OpenAIEmbeddings())

# 添加文档
doc1 = Document(page_content="LangChain 是一个开发框架", metadata={"category": "tech"})
doc2 = Document(page_content="今天天气不错", metadata={"category": "life"})
vector_store.add_documents([doc1, doc2])

# 搜索
results = vector_store.similarity_search("介绍一下 LangChain", k=1)
print(results[0].page_content)

# 带过滤器的搜索
def my_filter(doc):
    return doc.metadata.get("category") == "tech"

results = vector_store.similarity_search("天气", k=1, filter=my_filter)
# 即使“天气”语义更近，但因为 category 过滤，只会返回 tech 相关的文档
```

## 注意事项
- **非持久化**: 默认情况下数据只存在于内存中，程序重启后会丢失。需要手动调用 `dump` 保存。
- **性能限制**: 由于是在内存中进行线性搜索（计算所有向量的相似度），当文档数量达到数万级别时，搜索性能会明显下降。
- **依赖库**: 必须安装 `numpy` 才能运行相似度计算逻辑。

## 内部调用关系
- 调用 `self.embedding.embed_query` 将查询文本转化为向量。
- 内部使用 `_cosine_similarity`（来自 `utils.py`）进行批量向量计算。
- 继承自 `VectorStore`，实现了其定义的抽象接口。

## 相关链接
- [LangChain 向量存储官方文档](https://python.langchain.com/docs/modules/data_connection/vectorstores/)
- [NumPy 官方文档](https://numpy.org/doc/)

---
**最后更新时间**: 2026-01-29
**对应源码版本**: LangChain Core v1.2.7
