# ConversationChain (Deprecated)

`ConversationChain` 是 LangChain 中最基础的对话链。它继承自 `LLMChain`，旨在简化与 LLM 的多轮对话管理。它会自动处理对话历史（Memory）的加载和更新。

> **警告**: 该类自 v0.2.7 起已弃用。建议使用 `langchain_core.runnables.history.RunnableWithMessageHistory` 实现更现代、更灵活的对话管理。

## 核心功能

`ConversationChain` 封装了以下逻辑：
1. **历史加载**: 从 `Memory` 对象中获取之前的对话记录。
2. **提示词填充**: 将历史记录和当前用户输入填充到模板中。
3. **模型调用**: 发送给 LLM 获取回答。
4. **历史更新**: 将当前的问答对存回 `Memory`。

## 核心参数

| 参数 | 类型 | 说明 |
| :--- | :--- | :--- |
| `llm` | `BaseLanguageModel` | 执行对话的模型。 |
| `memory` | `BaseMemory` | 负责存储和检索对话历史的对象，默认为 `ConversationBufferMemory`。 |
| `prompt` | `BasePromptTemplate` | 对话模板，通常包含 `{history}` 和 `{input}` 占位符。 |

## 执行逻辑

```python
# 核心逻辑 (简化)
def _call(self, inputs: dict[str, Any]) -> dict[str, Any]:
    # 1. 获取历史 (由 LLMChain 自动处理)
    # 2. 生成回答
    response = super()._call(inputs)
    # 3. 结果返回 (历史更新由 Chain 基类在回调中处理)
    return response
```

## 迁移方案 (LCEL)

使用 `RunnableWithMessageHistory` 可以获得更好的异步支持、流式输出以及多线程会话管理：

```python
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

model = ChatOpenAI()
# 这种方式将逻辑与存储解耦，更符合生产环境的需求
chain = RunnableWithMessageHistory(model, get_session_history)

chain.invoke(
    "你好，我是小明。",
    config={"configurable": {"session_id": "user_123"}}
)
```

## 常见 Memory 类型

在使用 `ConversationChain` 时，可以搭配不同的 Memory：
- `ConversationBufferMemory`: 存储所有对话原始文本。
- `ConversationSummaryMemory`: 对之前的对话进行总结，节省 Token。
- `ConversationBufferWindowMemory`: 只保留最近的 K 轮对话。
