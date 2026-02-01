# RunnableWithMessageHistory：聊天历史管理组件

`history.py` 模块定义了 `RunnableWithMessageHistory` 类，它是 LangChain 中用于为任意 `Runnable` 序列自动管理聊天上下文历史的核心工具。

## 文件概述

| 特性 | 描述 |
| :--- | :--- |
| **角色** | 历史记录管理器、Runnable 装饰器 |
| **主要职责** | 自动读取、注入和持久化聊天消息历史 |
| **所属模块** | `langchain_core.runnables.history` |

该文件通过包装一个现有的 `Runnable`，在调用前从指定的存储（如 Redis、内存等）加载历史消息，并在调用完成后将新的交互（用户输入和 AI 输出）保存回存储。

## 导入依赖

| 模块/类 | 作用 |
| :--- | :--- |
| `BaseChatMessageHistory` | 聊天记录存储的基类接口 |
| `BaseMessage`, `HumanMessage`, `AIMessage` | 标准的消息对象模型 |
| `Runnable`, `RunnableBindingBase` | Runnable 核心基类，提供链式调用能力 |
| `RunnablePassthrough` | 用于在不改变原始输入的情况下注入历史数据 |
| `ConfigurableFieldSpec` | 用于定义如何从 `config` 中提取会话 ID 等配置 |

## 类详解：RunnableWithMessageHistory

### 功能描述
`RunnableWithMessageHistory` 是一个包装器，它拦截 `Runnable` 的输入，将历史消息合并进去，执行内部 `Runnable`，最后将结果存入历史记录。它解决了开发者手动管理 `BaseChatMessageHistory` 的繁琐过程。

### 参数说明

| 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `runnable` | `Runnable` | - | 是 | 需要被包装的核心业务逻辑（如 LLM 链）。 |
| `get_session_history` | `Callable` | - | 是 | 工厂函数，根据 `session_id` 等参数返回 `BaseChatMessageHistory` 实例。 |
| `input_messages_key` | `str` | `None` | 否 | 如果输入是字典，指定哪个键包含当前的用户消息。 |
| `output_messages_key` | `str` | `None` | 否 | 如果输出是字典，指定哪个键包含 AI 的响应消息。 |
| `history_messages_key` | `str` | `None` | 否 | 如果输入是字典，指定将历史消息注入到哪个键中。 |
| `history_factory_config` | `list[ConfigurableFieldSpec]` | `None` | 否 | 自定义如何从配置中识别会话参数（默认为 `session_id`）。 |

### 核心逻辑解读

1.  **历史加载 (`_enter_history`)**：
    *   在主逻辑运行前，根据 `config` 中的 `session_id` 调用 `get_session_history` 获取历史实例。
    *   读取历史消息。如果未指定 `history_messages_key`，则将历史消息直接拼接到输入列表前。
2.  **动态绑定**：
    *   构造一个内部链，首先运行历史加载逻辑，然后根据同步或异步环境选择执行包装的 `runnable`。
3.  **结果持久化 (`_exit_history`)**：
    *   运行结束后，提取本次输入的 `HumanMessage` 和输出的 `AIMessage`。
    *   调用 `hist.add_messages` 将这一轮交互保存到持久化存储中。

### 使用示例

```python
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

# 1. 定义存储字典
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# 2. 定义提示词模板，必须包含占位符用于注入历史
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个得力的助手"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

chain = prompt | ChatOpenAI()

# 3. 包装链
with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history"
)

# 4. 调用（必须传入 session_id）
config = {"configurable": {"session_id": "user_1"}}
response = with_history.invoke({"input": "你好，我是张三"}, config=config)
print(response.content)

# 第二次调用，它会自动带上“我是张三”的记忆
response2 = with_history.invoke({"input": "我刚才说我叫什么？"}, config=config)
print(response2.content)
```

### 注意事项

*   **配置依赖**：调用时必须在 `config` 的 `configurable` 字典中提供 `session_id`（或自定义的键），否则会抛出 `ValueError`。
*   **输入输出匹配**：
    *   如果 `runnable` 接受字典，必须正确配置 `input_messages_key`。
    *   如果 `runnable` 返回字典，必须正确配置 `output_messages_key`。
*   **消息自动转换**：如果输入是字符串，它会自动转换为 `HumanMessage`；如果输出是字符串，会自动转换为 `AIMessage`。
*   **内存管理**：对于 `InMemoryChatMessageHistory`，注意在大规模并发下内存占用。生产环境建议配合 Redis 或数据库实现。

## 内部调用关系

*   **RunnableBindingBase**：`RunnableWithMessageHistory` 继承自此类，利用其绑定配置和参数的能力。
*   **RunnablePassthrough.assign**：用于在字典输入中动态插入历史消息键值对。
*   **BaseChatMessageHistory**：通过多态调用用户提供的存储实现，完成消息的读写。

## 相关链接

*   [LangChain 官方文档 - 记忆管理](https://python.langchain.com/docs/expression_language/how_to/message_history)
*   [BaseChatMessageHistory 源码定义](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/core/langchain_core/chat_history.py)

---
最后更新时间：2026-01-29
对应源码版本：LangChain Core v1.2.7
