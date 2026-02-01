# Hypothetical Document Embeddings (HyDE)

`HypotheticalDocumentEmbedder` (简称 HyDE) 是一种增强检索的技术。它首先利用 LLM 根据查询生成一个“虚构文档”，然后对该虚构文档进行嵌入（Embedding），并以此向量在向量数据库中检索真实文档。

> **论文参考**: [Precise Zero-Shot Dense Retrieval without Relevance Labels](https://arxiv.org/abs/2212.10496)

## 核心原理

传统的检索是计算 `Query` 和 `Document` 的相似度。HyDE 的逻辑是：
1. **Query -> LLM -> Fake Document**: LLM 擅长预测问题的答案（即使不准确）。
2. **Fake Document -> Embedding -> Vector**: 虚构文档在向量空间中通常比原始查询更接近相关的真实文档。
3. **Vector -> VectorDB -> Real Documents**: 使用虚构文档的向量进行检索。

## 核心组件

| 参数 | 类型 | 说明 |
| :--- | :--- | :--- |
| `base_embeddings` | `Embeddings` | 用于计算最终向量的基础嵌入模型。 |
| `llm_chain` | `Runnable` | 用于生成虚构文档的链（通常是一个 `LLMChain` 或 LCEL 序列）。 |

## 核心方法

### `embed_query(text: str)`
这是 HyDE 的核心入口：
1. 调用 `llm_chain` 根据查询生成一个或多个虚构文档。
2. 调用 `base_embeddings.embed_documents()` 对生成的文档进行向量化。
3. 调用 `combine_embeddings()`（默认为取平均值）将多个文档向量合并为一个查询向量。

```python
# 核心逻辑 (简化)
def embed_query(self, text: str) -> list[float]:
    # 1. 生成虚构文档
    fake_document = self.llm_chain.invoke({"question": text})
    # 2. 向量化虚构文档
    embeddings = self.base_embeddings.embed_documents([fake_document])
    # 3. 合并向量 (取平均)
    return self.combine_embeddings(embeddings)
```

## 使用示例

```python
from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain_classic.chains import HypotheticalDocumentEmbedder

# 1. 设置基础嵌入模型
base_embeddings = OpenAIEmbeddings()
llm = OpenAI()

# 2. 使用内置模板或自定义链
# HypotheticalDocumentEmbedder.from_llm 提供了一些预置模板，如 "web_search"
hyde_embeddings = HypotheticalDocumentEmbedder.from_llm(
    llm, base_embeddings, "web_search"
)

# 3. 像普通 Embedding 一样使用
query_vector = hyde_embeddings.embed_query("什么是 HyDE？")
```

## 适用场景

- **跨领域检索**: 当查询和文档在语言风格或词汇分布上差异较大时。
- **冷启动检索**: 缺乏相关性标签的零样本检索场景。
- **短查询检索**: 当用户提问过于简短，不足以捕捉语义特征时，通过 LLM 扩展语义。
