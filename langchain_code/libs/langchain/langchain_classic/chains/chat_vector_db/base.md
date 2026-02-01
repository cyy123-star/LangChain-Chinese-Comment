# Chat Vector DB Chain

`ChatVectorDBChain` 是一个已弃用的经典链，用于与向量数据库进行对话。它是 `ConversationalRetrievalChain` 的前身，功能基本一致，但直接绑定了 `VectorStore`。

## 核心组件

| 组件 | 类型 | 说明 |
| :--- | :--- | :--- |
| `vectorstore` | `VectorStore` | 存储文档向量的数据库。 |
| `combine_docs_chain` | `BaseCombineDocumentsChain` | 用于组合检索到的文档并生成最终回答的链。 |
| `question_generator` | `LLMChain` | 用于根据聊天历史和当前问题生成独立问题的链。 |

## 参数表格

| 参数 | 类型 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- |
| `top_k_docs_for_context` | `int` | `4` | 检索时返回的文档数量。 |
| `search_kwargs` | `dict` | `{}` | 传递给向量数据库搜索方法的额外参数。 |

## 执行逻辑 (Verbatim Snippet)

以下是 `ChatVectorDBChain._get_docs` 的核心检索逻辑：

```python
def _get_docs(
    self,
    question: str,
    inputs: dict[str, Any],
    *,
    run_manager: CallbackManagerForChainRun,
) -> list[Document]:
    """获取文档。"""
    vectordbkwargs = inputs.get("vectordbkwargs", {})
    full_kwargs = {**self.search_kwargs, **vectordbkwargs}
    return self.vectorstore.similarity_search(
        question,
        k=self.top_k_docs_for_context,
        **full_kwargs,
    )
```

## 迁移指南 (LCEL)

`ChatVectorDBChain` 已被弃用。请直接使用 `ConversationalRetrievalChain` 或者现代的 `create_retrieval_chain`。

### 迁移建议：
1. 使用 `ConversationalRetrievalChain.from_llm(llm, vectorstore.as_retriever(), ...)`。
2. 或者使用 LCEL 写法（详见 `conversational_retrieval/base.md`）。
