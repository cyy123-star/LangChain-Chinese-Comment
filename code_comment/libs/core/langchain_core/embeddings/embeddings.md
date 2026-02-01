# Embeddings

## 文件概述
`embeddings.py` 定义了 `Embeddings` 抽象基类。它是所有文本嵌入模型（Text Embedding Models）的通用接口。嵌入模型的主要作用是将文本映射为高维空间中的向量（浮点数列表），使得语义相似的文本在空间中彼此接近。

## 导入依赖
- `abc.ABC`, `abc.abstractmethod`: 用于定义抽象接口。
- `langchain_core.runnables.config.run_in_executor`: 用于支持同步方法的异步执行。

## 类与函数详解
### 1. Embeddings
**功能描述**: 定义了文本嵌入的标准操作。它区分了“文档嵌入”和“查询嵌入”，虽然大多数模型对两者的处理逻辑相同，但这种设计允许某些模型对检索库和用户提问采用不同的处理策略。

#### 核心方法
- **`embed_documents(texts)`**:
    - **功能**: 为一组搜索文档生成嵌入向量。
    - **参数**: `texts: list[str]` - 待处理的文本列表。
    - **返回值**: `list[list[float]]` - 嵌套列表，每个内层列表代表一个文档的向量。
- **`embed_query(text)`**:
    - **功能**: 为单个查询文本（用户的问题）生成嵌入向量。
    - **参数**: `text: str` - 查询字符串。
    - **返回值**: `list[float]` - 单个浮点数列表。
- **`aembed_documents(texts)`**:
    - **功能**: 异步版本的文档嵌入。默认使用 `run_in_executor` 运行。
- **`aembed_query(text)`**:
    - **功能**: 异步版本的查询嵌入。

#### 注意事项
- **距离度量**: “相似性”的具体定义及“距离”的计算方式（如余弦相似度、欧氏距离）取决于具体的嵌入模型和向量数据库的配置。
- **性能优化**: 子类可以重写异步方法（`aembed_...`），利用特定模型库的原生异步支持来提高并发性能。

## 内部调用关系
- **在 RAG 中的位置**: 嵌入模型是向量存储（Vector Stores）的核心依赖，用于在入库阶段生成文档索引，以及在检索阶段生成查询向量。

## 相关链接
- [LangChain 官方文档 - Text Embedding Models](https://python.langchain.com/docs/modules/data_connection/text_embedding/)
- [源码文件](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/core/langchain_core/embeddings/embeddings.py)

---
最后更新时间: 2026-01-29
对应源码版本: LangChain Core v1.2.7
