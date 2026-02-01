# langchain_core.example_selectors.semantic_similarity

`langchain_core.example_selectors.semantic_similarity` 模块提供了一系列基于向量相似度的示例选择器。它能够根据用户输入的语义含义，从库中挑选出语义上最接近的示例，是实现高质量少样本提示词的关键工具。

## 文件概述

- **角色**: 语义相似度示例选择器。
- **主要职责**: 利用嵌入（Embeddings）和向量存储（Vector Stores）技术，实现基于余弦相似度或 MMR（最大边际相关性）的示例检索。
- **所属模块**: `langchain_core.example_selectors`

## 导入依赖

- `pydantic`: 用于模型定义和配置。
- `langchain_core.example_selectors.base`: 导入基类。
- `langchain_core.vectorstores`: 导入向量存储接口。
- `langchain_core.embeddings`: 导入嵌入模型接口（用于类型检查）。

## 类与函数详解

### 1. SemanticSimilarityExampleSelector
- **功能描述**: 最常用的语义选择器。它将示例转换为向量并存储，在运行时根据输入变量的向量进行相似度搜索。
- **核心方法**:
  - `select_examples(input_variables)`: 在向量存储中执行相似度搜索，返回最接近的 `k` 个示例。
  - `from_examples(...)`: **类方法**。便捷地从示例列表、嵌入模型和向量存储类创建一个选择器实例。

### 2. MaxMarginalRelevanceExampleSelector
- **功能描述**: 基于 MMR 算法的选择器。MMR 不仅考虑相似度，还考虑结果的多样性，防止选出的示例过于雷同。
- **参数说明**:
  - `fetch_k`: 初始检索的候选数量。
  - `k`: 最终选择的数量。

### 3. _VectorStoreExampleSelector (内部基类)
- **功能描述**: 封装了向量存储操作的通用逻辑，包括将字典转换为文本、添加示例到向量存储以及将文档转换回示例字典。

## 核心逻辑

- **文本化处理**: 示例（字典）在存入向量库前需要转换为纯文本。默认实现是将字典的所有值按键名排序后用空格连接。可以通过 `input_keys` 指定只对某些特定字段进行文本化和搜索。
- **元数据存储**: 原始示例字典作为元数据（Metadata）与文本向量一起存入向量存储，以便检索时能完整还原示例内容。

## 使用示例

```python
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.embeddings import DeterministicFakeEmbedding

examples = [
    {"input": "愉快", "output": "高兴"},
    {"input": "难过", "output": "悲伤"},
]

# 初始化选择器
example_selector = SemanticSimilarityExampleSelector.from_examples(
    examples,
    DeterministicFakeEmbedding(size=10),
    InMemoryVectorStore,
    k=1
)

# 搜索与 "开心" 语义接近的例子
selected = example_selector.select_examples({"input": "开心"})
print(selected) # 应返回与 "愉快" 相关的例子
```

## 注意事项

- **嵌入模型选择**: 搜索质量高度依赖于所选的 `Embeddings` 模型。
- **多样性需求**: 如果你的示例库中有大量重复或高度相似的内容，建议使用 `MaxMarginalRelevanceExampleSelector` 以获得更丰富的上下文。
- **性能**: 向量搜索通常很快，但如果示例库达到百万量级，应选择生产级的向量数据库（如 FAISS, Pinecone 等）。

## 内部调用关系

- **VectorStore**: 调用 `similarity_search` 或 `max_marginal_relevance_search`。
- **Embeddings**: 在向量化过程中由 `VectorStore` 调用。

## 相关链接
- [LangChain 官方文档 - 语义相似度选择器](https://python.langchain.com/docs/modules/model_io/prompts/example_selectors/semantic_similarity/)

---
- **最后更新时间**: 2026-01-29
- **对应源码版本**: LangChain Core v1.2.7
