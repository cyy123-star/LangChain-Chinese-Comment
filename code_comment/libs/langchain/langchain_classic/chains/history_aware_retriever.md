# libs\langchain\langchain_classic\chains\history_aware_retriever.py

`create_history_aware_retriever` 是一个工厂函数，用于创建一个能够处理对话历史的检索链。它是构建 RAG (检索增强生成) 应用的核心组件，特别是在需要处理多轮对话上下文时。

## 功能描述

该方法通过 LCEL 构建了一个逻辑分支：
1.  **无历史处理**：如果输入中没有 `chat_history`（或为空），则直接将用户的问题 (`input`) 传递给检索器。
2.  **有历史处理**：如果存在 `chat_history`，则先利用 LLM 将“对话历史 + 当前问题”重写为一个独立的搜索查询（Search Query），然后再将该查询传递给检索器。

## 核心方法：create_history_aware_retriever

### 参数说明

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `llm` | `LanguageModelLike` | 用于根据对话历史重写查询的语言模型。 |
| `retriever` | `RetrieverLike` | 最终执行检索的检索器对象。 |
| `prompt` | `BasePromptTemplate` | 用于重写查询的 Prompt。必须包含 `input` 变量，通常还包含 `chat_history`。 |

### 执行逻辑 (LCEL 流程)

该函数返回一个 `RunnableBranch`，逻辑如下：

```python
retrieve_documents: RetrieverOutputLike = RunnableBranch(
    (
        # 分支 1：如果没有聊天历史
        lambda x: not x.get("chat_history", False),
        # 直接透传 input 给 retriever
        (lambda x: x["input"]) | retriever,
    ),
    # 分支 2：如果有聊天历史
    # 使用 prompt + llm 重写查询，然后交给 retriever
    prompt | llm | StrOutputParser() | retriever,
).with_config(run_name="chat_retriever_chain")
```

## 使用示例

```python
from langchain_openai import ChatOpenAI
from langchain_classic.chains import create_history_aware_retriever
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 1. 定义重写 Prompt
contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
)
contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

# 2. 创建链
llm = ChatOpenAI(model="gpt-4o")
retriever = ... # 你的检索器
history_aware_retriever = create_history_aware_retriever(
    llm, retriever, contextualize_q_prompt
)

# 3. 调用
# 第一次提问 (无历史)
history_aware_retriever.invoke({"input": "What is LCEL?"})

# 第二次提问 (带历史)
history_aware_retriever.invoke({
    "input": "How do I use it?",
    "chat_history": [
        ("human", "What is LCEL?"),
        ("ai", "LCEL is LangChain Expression Language...")
    ]
})
```

## 注意事项

1.  **Prompt 要求**：`prompt` 必须包含 `input` 占位符。如果模型需要参考历史，还应包含 `chat_history` 占位符。
2.  **输入格式**：`chat_history` 可以是消息对象列表（`BaseMessage`）或特定格式的字符串，具体取决于 Prompt 的定义。
3.  **性能开销**：在有历史的情况下，会额外增加一次 LLM 调用来重写查询。为了优化，可以使用较小且快速的模型（如 GPT-4o-mini）来执行重写任务。
