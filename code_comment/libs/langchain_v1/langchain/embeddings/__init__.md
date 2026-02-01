# Embeddings (嵌入模型)

`embeddings` 模块是 LangChain v1 中处理文本嵌入的入口点。它通过统一的工厂接口简化了向量化模型的实例化。

## 核心导出

- **[init_embeddings](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain_v1/langchain/embeddings/base.md)**: 推荐的工厂函数，用于根据名称和提供商初始化嵌入模型。
- **Embeddings**: 所有嵌入模型的抽象基类（从 `langchain_core` 重新导出）。

## 模块迁移说明 ⚠️

在 `langchain 1.0.0` 版本中，为了保持核心包的精简，许多嵌入模型实现已移至其他位置：
- **`langchain-classic`**: 包含了旧版的 `CacheBackedEmbeddings` 以及所有社区提供的第三方嵌入模型。
- **集成包**: 官方支持的模型现在由专门的集成包提供（如 `langchain-openai`, `langchain-huggingface` 等）。

`init_embeddings` 函数会自动处理这些集成包的加载，开发者无需手动导入具体的实现类。

## 快速开始

```python
from langchain.embeddings import init_embeddings

# 初始化模型
embeddings = init_embeddings("openai:text-embedding-3-small")

# 嵌入单条查询
query_vector = embeddings.embed_query("LangChain 的核心优势是什么？")

# 嵌入多条文档
doc_vectors = embeddings.embed_documents(["文档 A 内容", "文档 B 内容"])
```

详情请参考 **[Base 模块文档](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain_v1/langchain/embeddings/base.md)**。
