# libs\langchain\langchain_classic\chains\conversational_retrieval\base.py

`ConversationalRetrievalChain` 是经典 LangChain 中用于构建 RAG（检索增强生成）聊天机器人的核心链。它在 `RetrievalQA` 的基础上增加了对对话历史的处理能力。

## 功能描述

该模块定义了 `BaseConversationalRetrievalChain` 及其实现。其核心目标是处理“后续问题”（Follow-up Questions），即那些依赖于之前对话上下文的问题。

### 核心逻辑流程
1.  **历史格式化**：将输入的对话历史（消息列表或元组列表）转换为字符串。
2.  **问题压缩 (Condense Question)**：使用 `question_generator` (LLMChain) 将当前问题和历史记录结合，生成一个不依赖上下文的“独立问题”。
3.  **文档检索**：使用独立问题通过 `retriever` 获取相关文档。
4.  **答案生成**：将获取的文档和独立问题（或原始问题）传递给 `combine_docs_chain` 生成最终回答。

## 参数说明

### BaseConversationalRetrievalChain

| 参数名 | 类型 | 默认值 | 描述 |
| :--- | :--- | :--- | :--- |
| `combine_docs_chain` | `BaseCombineDocumentsChain` | **必填** | 用于合并文档并生成答案的链。 |
| `question_generator` | `LLMChain` | **必填** | 负责生成独立问题的 LLM 链。 |
| `output_key` | `str` | `"answer"` | 最终答案在输出字典中的键名。 |
| `rephrase_question` | `bool` | `True` | 是否将压缩后的独立问题传给 `combine_docs_chain`。如果为 `False`，则传原始问题。 |
| `return_source_documents` | `bool` | `False` | 是否在结果中返回检索到的原始文档。 |
| `return_generated_question` | `bool` | `False` | 是否在结果中返回生成的独立问题。 |
| `get_chat_history` | `Callable` | `None` | 自定义历史格式化函数。若为 `None` 则使用默认逻辑。 |
| `response_if_no_docs_found` | `str` | `None` | 若未检索到文档，返回的固定响应。 |

## 执行逻辑 (Verbatim Snippet)

核心执行逻辑位于 `_call` 方法中：

```python
def _call(
    self,
    inputs: dict[str, Any],
    run_manager: CallbackManagerForChainRun | None = None,
) -> dict[str, Any]:
    _run_manager = run_manager or CallbackManagerForChainRun.get_noop_manager()
    question = inputs["question"]
    # 1. 格式化对话历史
    get_chat_history = self.get_chat_history or _get_chat_history
    chat_history_str = get_chat_history(inputs["chat_history"])

    # 2. 如果存在历史记录，生成独立问题
    if chat_history_str:
        callbacks = _run_manager.get_child()
        new_question = self.question_generator.run(
            question=question,
            chat_history=chat_history_str,
            callbacks=callbacks,
        )
    else:
        new_question = question
    
    # 3. 检索文档
    docs = self._get_docs(new_question, inputs, run_manager=_run_manager)
    
    # 4. 生成最终回答
    new_inputs = inputs.copy()
    if self.rephrase_question:
        new_inputs["question"] = new_question # 使用压缩后的问题
    new_inputs["chat_history"] = chat_history_str
    
    answer = self.combine_docs_chain.run(
        input_documents=docs,
        callbacks=_run_manager.get_child(),
        **new_inputs,
    )
    
    output = {self.output_key: answer}
    if self.return_source_documents:
        output["source_documents"] = docs
    if self.return_generated_question:
        output["generated_question"] = new_question
    return output
```

## 历史记录处理逻辑

默认的 `_get_chat_history` 函数处理两种格式：
-   `tuple[str, str]`：`(HumanMessage, AIMessage)` 的字符串元组。
-   `BaseMessage`：来自 `langchain_core.messages` 的消息对象。

```python
def _get_chat_history(chat_history: list[CHAT_TURN_TYPE]) -> str:
    buffer = ""
    for dialogue_turn in chat_history:
        if isinstance(dialogue_turn, BaseMessage):
            role_prefix = _ROLE_MAP.get(dialogue_turn.type, f"{dialogue_turn.type}: ")
            buffer += f"\n{role_prefix}{dialogue_turn.content}"
        elif isinstance(dialogue_turn, tuple):
            human = "Human: " + dialogue_turn[0]
            ai = "Assistant: " + dialogue_turn[1]
            buffer += f"\n{human}\n{ai}"
    return buffer
```

## 迁移建议 (LCEL)

`ConversationalRetrievalChain` 现已弃用。建议使用更模块化的 LCEL 实现方式，通常涉及两个步骤：
1.  使用 `create_history_aware_retriever` 创建能理解上下文的检索器。
2.  使用 `create_retrieval_chain` 结合问答逻辑。

### LCEL 示例

```python
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# 定义压缩问题的提示词
rephrase_prompt = ChatPromptTemplate.from_messages([
    ("placeholder", "{chat_history}"),
    ("user", "{input}"),
    ("user", "Given the above conversation, generate a standalone search query...")
])

# 1. 历史感知检索器
retriever_chain = create_history_aware_retriever(llm, retriever, rephrase_prompt)

# 2. 文档组合链
combine_docs_chain = create_stuff_documents_chain(llm, qa_prompt)

# 3. 完整的 RAG 链
rag_chain = create_retrieval_chain(retriever_chain, combine_docs_chain)
```

## 注意事项

1.  **独立问题质量**：RAG 的效果很大程度上取决于 `question_generator` 生成的问题是否足够清晰且包含所有必要的关键词。
2.  **Token 消耗**：每次对话都需要调用两次 LLM（一次压缩问题，一次生成答案），增加了延迟和成本。
3.  **内存管理**：该链本身不存储内存，需要外部传入 `chat_history` 或配合 `ConversationBufferMemory` 使用。
