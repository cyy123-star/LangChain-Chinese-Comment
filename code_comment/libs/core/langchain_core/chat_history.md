# chat_history.py

- **最后更新时间**: 2026-01-29
- **对应源码版本**: LangChain Core v1.2.7

## 文件概述
`chat_history.py` 定义了聊天消息历史（Chat Message History）的抽象接口和内存实现。它负责持久化存储对话中的消息序列，使得语言模型能够“记住”之前的上下文。

## 导入依赖
| 模块 | 作用 |
| :--- | :--- |
| `langchain_core.messages` | 包含 `BaseMessage`, `AIMessage`, `HumanMessage` 等消息基类。 |
| `langchain_core.runnables.config.run_in_executor` | 用于提供同步方法的默认异步实现。 |

## 类与函数详解

### 1. BaseChatMessageHistory (抽象基类)
- **功能描述**: 所有聊天历史存储器的接口定义。支持同步和异步的消息读写。
- **核心方法**:
  - **messages (属性)**: **抽象属性**。同步获取所有历史消息。
  - **aget_messages()**: 异步获取消息。
  - **add_messages(messages)**: 批量添加消息（推荐使用，以减少 IO 次数）。
  - **aadd_messages(messages)**: 批量异步添加消息。
  - **clear()**: **抽象方法**。清空历史记录。
  - **add_user_message(message)**: 便捷方法，添加用户消息。
  - **add_ai_message(message)**: 便捷方法，添加 AI 消息。

### 2. InMemoryChatMessageHistory
- **功能描述**: 聊天历史的简单内存实现。将消息存储在 Python 列表中。
- **适用场景**: 快速原型开发、单元测试或不需要持久化的短期会话。

## 核心逻辑
1. **批处理优化**: 开发者应优先使用 `add_messages` 而非多次调用 `add_message`，以减少与数据库或外部存储的往返次数。
2. **异步支持**: 大多数方法提供了默认的异步实现（通过在执行器中运行同步版本），子类可以重写这些方法以实现真正的非阻塞 IO。

## 使用示例
```python
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage

history = InMemoryChatMessageHistory()

# 添加消息
history.add_user_message("你好")
history.add_ai_message("你好！有什么我可以帮你的吗？")

# 获取所有消息
print(history.messages)

# 清空历史
history.clear()
```

## 相关链接
- [langchain_core.messages](file:///d%3A/TraeProjects/langchain_code_comment/code_comment/libs/core/langchain_core/messages/base.md)
