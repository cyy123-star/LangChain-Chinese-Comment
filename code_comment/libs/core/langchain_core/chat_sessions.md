# chat_sessions.py - 聊天会话数据模型

- **最后更新时间**: 2026-01-29
- **对应源码版本**: LangChain Core v1.2.7

## 文件概述

`chat_sessions.py` 定义了聊天会话的数据结构 `ChatSession`。它是一个轻量级的 `TypedDict`，用于封装一组消息（`BaseMessage`）以及相关的函数调用定义（Function Calling specs）。该模型主要用于聊天加载器（Chat Loaders）的输出，为 LangChain 处理历史对话数据提供统一的格式。

## 导入依赖

| 依赖模块 | 作用 |
| :--- | :--- |
| `collections.abc` | 提供 `Sequence` 类型提示，用于表示有序的消息序列。 |
| `typing` | 提供 `TypedDict` 用于定义具有固定键的字典结构。 |
| `langchain_core.messages` | 导入 `BaseMessage`，代表聊天中的单条消息。 |

## 类型详解

### 1. ChatSession (TypedDict)

代表单个对话、频道或其他消息组的容器。

#### 字段说明

| 字段名 | 类型 | 默认值 | 是否必填 | 功能描述 |
| :--- | :--- | :--- | :--- | :--- |
| `messages` | `Sequence[BaseMessage]` | N/A | 是 | 从源加载的 LangChain 聊天消息序列。 |
| `functions` | `Sequence[dict]` | N/A | 否 | 与这些消息相关的函数调用规范（Specs）。 |

#### 核心逻辑
- **非强制性结构**: 使用 `total=False` 定义，意味着 `functions` 字段是可选的。
- **消息序列**: `messages` 字段通常包含 `HumanMessage`, `AIMessage`, `SystemMessage` 等。

#### 使用示例

```python
from langchain_core.chat_sessions import ChatSession
from langchain_core.messages import HumanMessage, AIMessage

# 创建一个简单的聊天会话
session: ChatSession = {
    "messages": [
        HumanMessage(content="帮我查一下明天的天气"),
        AIMessage(content="", additional_kwargs={"function_call": {"name": "get_weather", "arguments": '{"city": "Beijing"}'}})
    ],
    "functions": [
        {
            "name": "get_weather",
            "description": "获取指定城市的天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"}
                }
            }
        }
    ]
}

print(f"会话包含 {len(session['messages'])} 条消息")
if "functions" in session:
    print(f"可用函数数: {len(session['functions'])}")
```

#### 注意事项
- `ChatSession` 本身不包含任何业务逻辑，仅作为数据载体。
- 在 LangChain 的最新版本中，函数调用已逐渐向 `tool_calls` 迁移，但在历史数据加载场景中，`functions` 字段依然重要。

## 内部调用关系

- **被调用**: 被 `BaseChatLoader` 的 `load` 和 `lazy_load` 方法作为返回值类型。
- **依赖**: 依赖于 `BaseMessage` 及其子类来表示具体的对话内容。

## 相关链接
- [BaseChatLoader 源码文档](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/core/langchain_core/chat_loaders.md)
- [BaseMessage 源码文档](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/core/langchain_core/messages/base.md)
