# langchain_core.embeddings

## 模块概述
`langchain_core.embeddings` 模块定义了 LangChain 框架中所有文本嵌入模型（Text Embedding Models）的标准接口。嵌入模型是语义搜索、聚类和数据可视化的核心。

## 核心组件导出
本模块采用了动态导入机制，主要导出以下核心类：

### 1. 核心接口 (from `embeddings.py`)
- **`Embeddings`**: 所有嵌入模型的抽象基类。它强制子类实现同步和异步的文档嵌入（`embed_documents`）及查询嵌入（`embed_query`）方法。

### 2. 测试工具 (from `fake.py`)
- **`FakeEmbeddings`**: 生成随机向量的模拟模型。
- **`DeterministicFakeEmbedding`**: 基于输入哈希生成固定随机向量的模拟模型，适用于测试断言。

## 使用场景
1. **文档入库**: 在将 `Document` 对象存入向量数据库之前，调用 `embed_documents` 将文本转换为向量。
2. **检索查询**: 当用户提出问题时，调用 `embed_query` 将问题转换为向量，用于在向量空间中进行相似性搜索。
3. **缓存优化**: 结合 `CacheBackedEmbeddings` 可以避免对相同文本进行重复的 API 调用。

## 相关链接
- [LangChain 官方文档 - Embeddings](https://python.langchain.com/docs/modules/data_connection/text_embedding/)
- [源码目录](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/core/langchain_core/embeddings/)

---
最后更新时间: 2026-01-29
对应源码版本: LangChain Core v1.2.7
