# langchain_core/messages/tool.py

`ToolMessage` 是 LangChain 中用于承载工具执行结果的消息类。它在 Agent 或具有工具调用能力（Tool Calling）的链中扮演着连接“工具输出”与“模型下一步决策”的关键角色。

## 文件概述

该文件定义了 `ToolMessage` 类、`ToolMessageChunk` 类，以及用于描述工具调用请求的 `ToolCall` 和 `ToolCallChunk` 等数据结构。

## 导入依赖

| 依赖模块 | 作用 |
| :--- | :--- |
| `pydantic` | 提供数据验证（`model_validator`）和字段定义。 |
| `typing_extensions` | 提供 `TypedDict` 和 `NotRequired` 等增强类型注解。 |
| `langchain_core.messages.base` | 导入消息基类和合并工具。 |

## 类与函数详解

### ToolMessage

代表工具执行结果的消息。

#### 功能描述
当 AI 模型请求调用某个工具时，系统会执行该工具并将其返回的结果封装在 `ToolMessage` 中发送回模型。通过 `tool_call_id` 字段，模型可以将该结果与其之前的请求对应起来。

#### 参数说明
| 参数名 | 类型 | 默认值 | 是否必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `content` | `str \| list` | - | 是 | 工具执行的输出结果。通常是字符串，也支持多模态内容。 |
| `tool_call_id` | `str` | - | 是 | 与该结果关联的工具调用请求 ID。 |
| `artifact` | `Any` | `None` | 否 | 工具执行生成的原始附件（如图像数据、复杂对象），不直接发送给模型，但可用于后续处理。 |
| `status` | `str` | `"success"` | 否 | 工具执行状态（`"success"` 或 `"error"`）。 |

#### 核心逻辑
- **参数校验**：通过 `coerce_args` 校验器，自动将非字符串/列表类型的 `content` 强制转换为字符串。
- **序列化**：`type` 字段固定为 `"tool"`。

### ToolCall (TypedDict)

代表 AI 发出的工具调用请求。

#### 字段说明
| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `name` | `str` | 要调用的工具名称。 |
| `args` | `dict` | 传递给工具的参数字典。 |
| `id` | `str \| None` | 该调用的唯一标识符。 |

### ToolCallChunk (TypedDict)

流式传输中的工具调用片段。

#### 核心逻辑
- **合并机制**：在流式输出中，多个 `ToolCallChunk` 会根据 `index` 字段进行合并。`args` 字段通常在片段中是部分 JSON 字符串，合并后可解析为完整字典。

## 使用示例

```python
from langchain_core.messages import ToolMessage

# 1. 创建一个简单的工具返回消息
tool_msg = ToolMessage(
    content="当前北京的气温是 25 摄氏度。",
    tool_call_id="call_123456"
)

# 2. 包含附加信息的工具消息
tool_msg_with_artifact = ToolMessage(
    content="已生成销售图表。",
    artifact={"chart_data": [10, 20, 30], "format": "png"},
    tool_call_id="call_789"
)

# 3. 标记执行失败
error_msg = ToolMessage(
    content="错误：无法连接到数据库。",
    status="error",
    tool_call_id="call_000"
)
```

## 注意事项

1. **ID 匹配**：`tool_call_id` 必须与 `AIMessage` 中 `tool_calls` 的 `id` 完全一致，否则模型可能无法理解该结果属于哪个请求。
2. **内容强制转换**：如果工具返回的是数字或复杂对象，`ToolMessage` 会尝试将其转换为字符串。建议在工具实现中自行处理好序列化逻辑。
3. **Artifact 的用途**：`artifact` 字段非常适合存储模型不需要知道但下游流程需要的中间结果（如数据帧、图像字节流等）。

## 内部调用关系

- 继承自 [base.py](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/core/langchain_core/messages/base.py) 中的 `BaseMessage`。
- 被 [ai.py](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/core/langchain_core/messages/ai.py) 中的 `AIMessage` 引用（用于定义 `tool_calls` 结构）。

## 相关链接

- [LangChain 官方文档 - Tool Output](https://python.langchain.com/docs/how_to/tool_artifacts/)
- [源码文件: langchain_core/messages/tool.py](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/core/langchain_core/messages/tool.py)
- [术语表: TERMINOLOGY.md](file:///d:/TraeProjects/langchain_code_comment/TERMINOLOGY.md)

---
最后更新时间: 2026-01-29
对应源码版本: LangChain Core v1.2.7
