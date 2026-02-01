# Embeddings (文本嵌入)

`embeddings` 模块提供了将文本转换为数值向量（Vector）的接口。这些向量捕获了文本的语义信息，是实现语义搜索、聚类和向量数据库的核心。

## 核心接口

### `Embeddings`
所有嵌入模型的抽象基类。它定义了两个核心方法：
- `embed_documents(texts)`: 为一批文档生成向量（通常用于索引）。
- `embed_query(text)`: 为单个查询字符串生成向量（通常用于搜索）。

## 常见实现

| 提供商 | 说明 |
| :--- | :--- |
| `OpenAIEmbeddings` | 行业标准，使用 OpenAI 的 `text-embedding-3-small/large` 模型。 |
| `HuggingFaceEmbeddings` | 在本地运行开源模型（如 `sentence-transformers` 系列）。 |
| `CohereEmbeddings` | 高性能的商业嵌入模型，支持多语言。 |
| `OllamaEmbeddings` | 配合 Ollama 运行本地嵌入模型。 |
| `BedrockEmbeddings` | 使用 AWS Bedrock 提供的 Titan 嵌入模型。 |

## 使用示例

```python
from langchain_openai import OpenAIEmbeddings

embeddings_model = OpenAIEmbeddings()

# 嵌入文档
doc_vectors = embeddings_model.embed_documents([
    "Hi there!",
    "Oh, hello!",
    "What's your name?"
])

# 嵌入查询
query_vector = embeddings_model.embed_query("What is the greeting?")
```

## 应用场景

1. **RAG (检索增强生成)**: 将文档库向量化并存入向量数据库。
2. **相似度计算**: 通过计算向量间的余弦相似度来判断文本相关性。
3. **数据可视化**: 将高维向量降维后在二维或三维空间展示。

## 迁移指南

- **集成包**: 实际的实现现在主要位于 `langchain-openai`, `langchain-huggingface` 等集成包中。
- **缓存**: 如果需要节省费用，可以使用 `CacheBackedEmbeddings` 来缓存已经生成的向量。
