# Conversational Retrieval Chain

`ConversationalRetrievalChain` 是一个用于基于检索到的文档进行对话的经典链。它结合了聊天历史和新问题，生成一个独立的检索问题，然后使用该问题检索文档并生成回答。

## 核心组件

| 组件 | 类型 | 说明 |
| :--- | :--- | :--- |
| `combine_docs_chain` | `BaseCombineDocumentsChain` | 用于组合检索到的文档并生成最终回答的链（如 Stuff, Map-Reduce 等）。 |
| `question_generator` | `LLMChain` | 用于根据聊天历史和当前问题生成独立问题的链。 |
| `retriever` | `BaseRetriever` | 用于检索相关文档的检索器。 |
| `get_chat_history` | `Callable` | 可选函数，用于将聊天历史列表格式化为字符串。 |

## 参数表格

| 参数 | 类型 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- |
| `output_key` | `str` | `"answer"` | 输出字典中回答的键名。 |
| `rephrase_question` | `bool` | `True` | 是否将重新生成的独立问题传递给 `combine_docs_chain`。 |
| `return_source_documents` | `bool` | `False` | 是否在输出中返回检索到的源文档。 |
| `return_generated_question` | `bool` | `False` | 是否在输出中返回生成的独立问题。 |
| `response_if_no_docs_found` | `str \| None` | `None` | 如果未找到文档，返回的固定响应。 |
| `max_tokens_limit` | `int \| None` | `None` | 限制传递给 `StuffDocumentsChain` 的文档总 token 数。 |

## 执行逻辑 (Verbatim Snippet)

以下是 `BaseConversationalRetrievalChain._call` 的核心执行逻辑：

```python
def _call(
    self,
    inputs: dict[str, Any],
    run_manager: CallbackManagerForChainRun | None = None,
) -> dict[str, Any]:
    _run_manager = run_manager or CallbackManagerForChainRun.get_noop_manager()
    question = inputs["question"]
    get_chat_history = self.get_chat_history or _get_chat_history
    chat_history_str = get_chat_history(inputs["chat_history"])

    if chat_history_str:
        callbacks = _run_manager.get_child()
        new_question = self.question_generator.run(
            question=question,
            chat_history=chat_history_str,
            callbacks=callbacks,
        )
    else:
        new_question = question
    
    # 检索文档
    docs = self._get_docs(new_question, inputs, run_manager=_run_manager)
    
    output: dict[str, Any] = {}
    if self.response_if_no_docs_found is not None and len(docs) == 0:
        output[self.output_key] = self.response_if_no_docs_found
    else:
        new_inputs = inputs.copy()
        if self.rephrase_question:
            new_inputs["question"] = new_question
        new_inputs["chat_history"] = chat_history_str
        # 生成回答
        answer = self.combine_docs_chain.run(
            input_documents=docs,
            callbacks=_run_manager.get_child(),
            **new_inputs,
        )
        output[self.output_key] = answer

    if self.return_source_documents:
        output["source_documents"] = docs
    if self.return_generated_question:
        output["generated_question"] = new_question
    return output
```

## 迁移指南 (LCEL)

`ConversationalRetrievalChain` 已被弃用。建议使用 `create_history_aware_retriever` 和 `create_retrieval_chain` 的组合。

### 现代写法示例：

```python
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 1. 创建历史感知检索器
contextualize_q_prompt = ChatPromptTemplate.from_messages([
    ("system", "Given a chat history and the latest user question..."),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])
history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)

# 2. 创建问答链
qa_prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer the question using the context: {context}"),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])
question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

# 3. 组合成最终的 RAG 链
rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

# 使用方式
rag_chain.invoke({"input": "What is LCEL?", "chat_history": []})
```
