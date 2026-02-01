# Context Editing Middleware (上下文编辑中间件)

`context_editing.py` 实现了 `ContextEditingMiddleware`，它允许在对话超出配置的 Token 阈值时，通过清理旧的工具结果来管理上下文大小。这与 Anthropic 的上下文编辑功能（如 `clear_tool_uses`）对齐。

## 核心概念 (Core Concepts)

- **Token 计数**: 支持多种计数方法（如模型内置计数或近似计数）。
- **编辑策略 (`ContextEdit`)**: 定义如何修改消息列表的协议。
- **清理工具调用 (`ClearToolUsesEdit`)**: 目前支持的主要策略，用于在达到限制时清理旧的 `ToolMessage` 内容。

## 核心组件 (Core Components)

### `ClearToolUsesEdit` (数据类)

用于配置清理 `ToolMessage` 的具体行为。

| 参数 | 类型 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- |
| `trigger` | `int` | `100,000` | 触发清理的 Token 阈值。 |
| `clear_at_least` | `int` | `0` | 每次清理至少回收的 Token 数量。 |
| `keep` | `int` | `3` | 必须保留的最近工具结果的数量。 |
| `clear_tool_inputs` | `bool` | `False` | 是否同时清除 AI 消息中的工具调用参数。 |
| `exclude_tools` | `Sequence[str]` | `()` | 不参与清理的工具名称列表。 |
| `placeholder` | `str` | `"[cleared]"` | 清理后填充的占位符文本。 |

### `ContextEditingMiddleware`

| 参数 | 类型 | 说明 |
| :--- | :--- | :--- |
| `edits` | `list[ContextEdit]` | 要应用的编辑策略列表。 |
| `token_count_method` | `Literal["approximate", "model"]` | Token 计数方法。 |

## 执行逻辑 (Execution Logic)

1.  **触发检查**: 每次模型调用前，计算当前消息列表的总 Token 数。
2.  **应用策略**: 如果超过 `trigger` 阈值，按顺序应用 `edits` 列表中的策略。
3.  **原地修改**: `ClearToolUsesEdit` 会查找 `ToolMessage`，保留最近的 `keep` 个，将其余的消息内容替换为占位符。
4.  **关联修改**: 如果开启 `clear_tool_inputs`，它还会回溯对应的 `AIMessage` 并清空其 `tool_calls` 中的 `args`。

## 使用场景 (Usage Scenarios)

- **超长对话管理**: 防止因上下文过长导致模型性能下降或触发 Token 限制。
- **成本控制**: 通过主动缩减不必要的上下文来减少 API 调用费用。
- **模型兼容性**: 使任何 LangChain 聊天模型都能具备类似 Claude 的上下文管理能力。

## 注意事项 (Notes)

- **信息丢失**: 清理后的工具结果对模型不再可见（仅剩占位符），可能会影响模型对过去操作的理解。
- **Token 估算**: `approximate` 模式下可能存在误差，建议在高精要求场景下使用 `model` 模式。

