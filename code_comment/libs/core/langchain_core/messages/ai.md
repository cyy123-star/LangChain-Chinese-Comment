# langchain_core/messages/ai.py

`AIMessage` 是 LangChain 中代表模型输出的消息类。它封装了 AI 生成的文本、工具调用（Tool Calls）以及相关的元数据。

## 文件概述

该文件定义了 `AIMessage` 类、`AIMessageChunk` 类，以及用于描述 Token 使用情况的 `UsageMetadata`、`InputTokenDetails` 和 `OutputTokenDetails` 等类型定义。它是处理模型响应的核心模块。

## 导入依赖

| 依赖模块 | 作用 |
| :--- | :--- |
| `pydantic` | 用于数据验证和 `Field` 定义。 |
| `langchain_core.messages.base` | 导入消息基类和内容合并工具。 |
| `langchain_core.messages.tool` | 导入工具调用相关的类（ToolCall, ToolCallChunk）。 |
| `langchain_core.utils.usage` | 处理 Token 使用计量的辅助工具。 |

## 类与函数详解

### UsageMetadata (TypedDict)

标准化的 Token 使用元数据。

#### 字段说明
| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `input_tokens` | `int` | 输入（提示词）Token 总数。 |
| `output_tokens` | `int` | 输出（完成）Token 总数。 |
| `total_tokens` | `int` | 总 Token 数（输入 + 输出）。 |
| `input_token_details` | `InputTokenDetails` | 输入 Token 的详细分解（如缓存、音频等）。 |
| `output_token_details` | `OutputTokenDetails` | 输出 Token 的详细分解（如推理、音频等）。 |

### AIMessage

代表来自 AI 的消息。

#### 功能描述
`AIMessage` 用于封装聊天模型生成的响应。除了文本内容外，它还承载了模型是否决定调用工具、Token 消耗统计等关键信息。

#### 参数说明
| 参数名 | 类型 | 默认值 | 是否必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `content` | `str \| list[str \| dict]` | `None` | 否 | AI 生成的文本或内容块。 |
| `tool_calls` | `list[ToolCall]` | `[]` | 否 | 模型请求调用的工具列表。 |
| `invalid_tool_calls` | `list[InvalidToolCall]` | `[]` | 否 | 解析失败的工具调用。 |
| `usage_metadata` | `UsageMetadata` | `None` | 否 | Token 使用统计信息。 |
| `**kwargs` | `Any` | - | 否 | 其他元数据（如 `name`, `id`, `response_metadata`）。 |

#### 核心逻辑
- **初始化**：支持多种初始化方式，内部会自动处理内容块的转换。
- **序列化**：`type` 字段固定为 `"ai"`。

### AIMessageChunk

`AIMessage` 的流式片段。

#### 功能描述
在流式输出（Streaming）中，模型会分多次返回 `AIMessageChunk`。这些片段可以通过 `+` 运算符进行合并，最终还原为完整的 `AIMessage`。

## 使用示例

```python
from langchain_core.messages import AIMessage

# 1. 简单的纯文本响应
ai_msg = AIMessage(content="你好！我是 AI 助手。")

# 2. 带有工具调用的响应
tool_call_msg = AIMessage(
    content="",
    tool_calls=[{
        "name": "get_weather",
        "args": {"location": "Beijing"},
        "id": "call_123"
    }]
)

# 3. 包含 Token 使用信息的响应
usage_msg = AIMessage(
    content="这是一条测试消息。",
    usage_metadata={
        "input_tokens": 10,
        "output_tokens": 5,
        "total_tokens": 15
    }
)
```

## 注意事项

1. **合并逻辑**：`AIMessageChunk` 的合并不仅仅是文本拼接，还包括 `tool_calls` 的增量合并和 `usage_metadata` 的累加。
2. **推理 Token**：对于支持“思考”过程的模型（如 OpenAI o1），其推理 Token 通常包含在 `output_token_details` 中，但不一定计入 `content`。
3. **工具调用解析**：如果 `invalid_tool_calls` 不为空，说明模型生成的工具调用格式有误。

## 内部调用关系

- 继承自 [base.py](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/core/langchain_core/messages/base.py) 中的 `BaseMessage`。
- 使用 [tool.py](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/core/langchain_core/messages/tool.py) 中定义的工具调用结构。

## 相关链接

- [LangChain 官方文档 - Tool Calling](https://python.langchain.com/docs/how_to/tool_calling/)
- [源码文件: langchain_core/messages/ai.py](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/core/langchain_core/messages/ai.py)
- [术语表: TERMINOLOGY.md](file:///d:/TraeProjects/langchain_code_comment/TERMINOLOGY.md)

---
最后更新时间: 2026-01-29
对应源码版本: LangChain Core v1.2.7
