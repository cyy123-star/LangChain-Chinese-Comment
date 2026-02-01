# libs\langchain\langchain_classic\chains\hyde\base.py

`HypotheticalDocumentEmbedder` (HyDE) 是一种增强型检索技术。它不是直接对用户的原始查询（Query）进行向量化，而是先让 LLM 生成一个“假设性文档”（Hypothetical Document），然后再对该文档进行向量化检索。

## 功能描述

该模块实现了 HyDE 算法（参考论文 [2212.10496](https://arxiv.org/abs/2212.10496)）。其核心思想是：原始查询通常很短且缺乏语义丰富度，而 LLM 生成的伪文档（尽管事实可能不准确）在向量空间中往往更接近真实的答案文档，从而提高检索召回率。

### 核心逻辑流程
1.  **伪文档生成**：接收用户查询，使用 `llm_chain` 生成一个或多个假设性的回答文档。
2.  **向量化**：使用 `base_embeddings` 对生成的伪文档进行向量化。
3.  **向量聚合**：如果生成了多个伪文档，则将它们的向量进行平均处理（通常使用 NumPy）。
4.  **检索使用**：将聚合后的向量作为查询向量，在向量数据库中进行检索。

## 参数说明

### HypotheticalDocumentEmbedder

| 参数名 | 类型 | 默认值 | 描述 |
| :--- | :--- | :--- | :--- |
| `base_embeddings` | `Embeddings` | **必填** | 底层的向量化模型（如 OpenAIEmbeddings）。 |
| `llm_chain` | `Runnable` | **必填** | 用于生成假设性文档的链（通常是 `prompt | llm | parser`）。 |

## 执行逻辑 (Verbatim Snippet)

### 1. 查询向量化 (`embed_query`)

这是 HyDE 的入口方法，它重写了 `Embeddings` 接口的 `embed_query`：

```python
def embed_query(self, text: str) -> list[float]:
    """生成假设文档并对其进行向量化。"""
    var_name = self.input_keys[0]
    # 1. 调用 LLM 生成伪文档
    result = self.llm_chain.invoke({var_name: text})
    
    if isinstance(self.llm_chain, LLMChain):
        documents = [result[self.output_keys[0]]]
    else:
        documents = [result]
    
    # 2. 对伪文档进行向量化
    embeddings = self.embed_documents(documents)
    
    # 3. 聚合（平均）向量
    return self.combine_embeddings(embeddings)
```

### 2. 向量聚合 (`combine_embeddings`)

```python
def combine_embeddings(self, embeddings: list[list[float]]) -> list[float]:
    """将多个向量合并为最终的查询向量。"""
    try:
        import numpy as np
        return list(np.array(embeddings).mean(axis=0)) # 均值聚合
    except ImportError:
        # 如果没有 numpy，使用纯 Python 实现
        num_vectors = len(embeddings)
        return [
            sum(dim_values) / num_vectors
            for dim_values in zip(*embeddings, strict=False)
        ]
```

## 迁移建议 (LCEL)

HyDE 在现代 LangChain 中通常作为一个 `Embeddings` 包装器使用，或者通过简单的 LCEL 链实现。

### LCEL 替代方案

```python
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# 1. 定义生成伪文档的链
hyde_prompt = ChatPromptTemplate.from_template("Write a scientific paper passage to answer this: {question}")
hyde_chain = hyde_prompt | llm | StrOutputParser()

# 2. 在检索流程中使用
def hyde_retriever(question):
    hypothetical_doc = hyde_chain.invoke({"question": question})
    return vectorstore.similarity_search(hypothetical_doc)
```

## 注意事项

1.  **延迟增加**：由于在检索前增加了一次 LLM 调用，检索的总响应时间会显著增加。
2.  **成本**：每次检索都会消耗额外的 LLM Token。
3.  **NumPy 依赖**：强烈建议安装 `numpy` (`pip install numpy`) 以获得更好的向量聚合性能。
4.  **幻觉双刃剑**：HyDE 利用了 LLM 的“幻觉”能力。如果生成的伪文档偏离主题太远，可能会导致检索质量下降。

