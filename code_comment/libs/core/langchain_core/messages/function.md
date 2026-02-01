# LangChain 函数消息 (Function Message) 规范

## 文件概述

`function.py` 定义了 `FunctionMessage` 类及其块变体 `FunctionMessageChunk`。该类用于将外部函数或工具的执行结果返回给大语言模型（LLM）。

**注意**：`FunctionMessage` 是较旧的消息模式。在现代 LangChain 开发中，推荐优先使用 `ToolMessage`，因为它包含 `tool_call_id` 字段，能够更好地支持并行工具调用。

---

## 导入依赖

| 模块 | 作用 |
| :--- | :--- |
| `typing` | 提供类型注解支持（`Any`, `Literal`）。 |
| `typing_extensions` | 提供 `override` 装饰器，明确方法重写。 |
| `langchain_core.messages.base` | 导入基础消息类 `BaseMessage`、`BaseMessageChunk` 及内容合并工具 `merge_content`。 |
| `langchain_core.utils._merge` | 导入字典合并工具 `merge_dicts`。 |

---

## 类与函数详解

### 1. FunctionMessage
**功能描述**: 继承自 `BaseMessage`，专门用于封装函数执行的输出结果。它通过 `name` 字段标识执行的函数名称。

| 字段名 | 类型 | 默认值 | 必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `name` | `str` | - | 是 | 已执行的函数名称。 |
| `content` | `MessageContent` | - | 是 | 函数执行的结果内容（通常是字符串形式的 JSON 或纯文本）。 |
| `type` | `Literal["function"]` | "function" | 否 | 消息类型标识，用于序列化。 |

---

### 2. FunctionMessageChunk
**功能描述**: `FunctionMessage` 的流式块版本，支持通过 `+` 运算符与其他块进行合并。

| 方法/属性 | 描述 |
| :--- | :--- |
| `type` | 类型标识为 `"FunctionMessageChunk"`，以便在流式处理中进行区分。 |
| `__add__` | 重写加法运算符。支持将两个 `FunctionMessageChunk` 合并为一个。要求两个块的 `name` 必须一致，否则抛出 `ValueError`。 |

---

## 核心逻辑

- **标识与关联**: `FunctionMessage` 主要依赖 `name` 字段与之前的函数调用进行关联。
- **局限性**: 与 `ToolMessage` 不同，它缺乏唯一的调用 ID。在模型一次性请求多个同名函数调用时，可能会产生歧义。
- **块合并**: `FunctionMessageChunk` 的合并逻辑确保了在流式获取函数输出时，内容（`content`）、附加参数（`additional_kwargs`）和响应元数据（`response_metadata`）能够被正确累加。

---

## 使用示例

### 1. 基本用法
展示如何创建一个函数消息并将其传递给模型。

```python
from langchain_core.messages import FunctionMessage

# 假设模型之前调用了名为 "get_weather" 的函数
function_result = FunctionMessage(
    name="get_weather",
    content='{"location": "北京", "temperature": "25°C", "condition": "晴"}'
)

print(function_result)
```

### 2. 流式块合并
演示如何合并两个函数消息块。

```python
from langchain_core.messages import FunctionMessageChunk

chunk1 = FunctionMessageChunk(name="search", content="这是搜索结果")
chunk2 = FunctionMessageChunk(name="search", content=" 的第一部分。")

full_chunk = chunk1 + chunk2
print(full_chunk.content) # 输出: 这是搜索结果 的第一部分。
```

---

## 注意事项

- **优先建议**: 除非你正在维护旧系统或对接仅支持旧版协议的模型，否则请使用 `ToolMessage`。
- **名称一致性**: 在合并 `FunctionMessageChunk` 时，必须确保 `name` 字段完全匹配。
- **序列化**: 该消息类型在序列化时会被标记为 `function`，以便前端或存储系统正确识别其角色。

---

## 内部调用关系

- **`BaseMessage`**: 作为父类提供基础的字段和方法。
- **`ChatModel`**: 聊天模型在接收到 `FunctionMessage` 后，会将其作为上下文的一部分，用于生成下一步的回复。

---

## 相关链接

- [LangChain 官方文档 - ToolMessage](https://python.langchain.com/docs/concepts/messages/#toolmessage)
- [LangChain 源码 - BaseMessage](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/core/langchain_core/messages/base.md)

---

**最后更新时间**: 2026-01-29
**对应源码版本**: LangChain Core v1.2.7
