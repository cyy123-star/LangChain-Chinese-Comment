# libs\langchain\langchain_classic\chains\conversation\base.py

## 文件概述

`base.py` 定义了 `ConversationChain`，这是一个专门用于构建聊天机器人的链。它继承自 `LLMChain`，但增加了对记忆（Memory）的内置支持，使得 LLM 能够“记住”之前的对话上下文。

## 核心类：ConversationChain (已弃用)

### 功能描述

`ConversationChain` 是一个预配置的链，它自动管理输入、记忆和 Prompt。每次调用时，它会从 Memory 中加载历史记录，注入到 Prompt 中，然后调用 LLM 生成回复，最后将新的输入输出对存回 Memory。

### 核心属性

| 属性名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `memory` | `BaseMemory` | 记忆组件，默认为 `ConversationBufferMemory`。 |
| `prompt` | `BasePromptTemplate` | 对话使用的 Prompt 模板，默认为内置的 `PROMPT`。 |
| `input_key` | `str` | 用户输入的键名，默认为 `input`。 |
| `output_key` | `str` | 模型回复的键名，默认为 `response`。 |

### 验证逻辑

在模型初始化后，会执行 `validate_prompt_input_variables`：

1. **键名冲突检查**：确保 `input_key` 不在 Memory 的变量列表中。
2. **变量完整性检查**：确保 Prompt 期望的输入变量集合等于 Memory 提供的变量加上 `input_key`。

### 使用示例

```python
from langchain_classic.chains import ConversationChain
from langchain_openai import OpenAI

llm = OpenAI()
conversation = ConversationChain(llm=llm, verbose=True)

# 第一轮对话
conversation.invoke({"input": "你好，我是 Bob"})
# 输出: "你好 Bob！有什么我可以帮你的吗？"

# 第二轮对话（自动携带历史记录）
conversation.invoke({"input": "我刚才说我叫什么？"})
# 输出: "你刚才说你叫 Bob。"
```

## 迁移建议 (LCEL)

该类已被弃用，建议使用 `RunnableWithMessageHistory` 来实现更现代、支持流式传输和异步的对话系统。

### 现代替代示例

```python
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

model = ChatOpenAI()
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

chain = RunnableWithMessageHistory(model, get_session_history)

chain.invoke(
    "Hi I'm Bob.",
    config={"configurable": {"session_id": "1"}},
)
```

## 注意事项

1. **默认 Prompt**：如果不指定 Prompt，默认使用的是一个简单的 "The following is a friendly conversation..." 模板。
2. **内存管理**：对于长对话，建议使用 `ConversationSummaryMemory` 或 `ConversationBufferWindowMemory` 以避免超出 Token 限制。
