# Tool Call Limit Middleware (工具调用次数限制中间件)

`tool_call_limit.py` 实现了 `ToolCallLimitMiddleware`，用于监控和限制代理调用特定工具或所有工具的次数。

## 核心定位
相比于全局的模型调用限制，该中间件提供了更细粒度的控制。你可以针对某个高成本工具（如搜索、代码执行）设置独立的配额，或者为所有工具设置一个总的调用上限。

## 主要特性

- **细粒度过滤**: 支持针对特定工具名 (`tool_name`) 进行计数，也支持对所有工具 (`__all__`) 进行全局计数。
- **智能拦截**: 当模型一次性发起多个工具调用（并行调用）时，能够自动识别并拦截超出配额的部分。
- **多种响应模式**:
    - **继续运行 (`continue`)**: 仅拦截超额工具并返回错误信息给模型，允许模型继续尝试其他逻辑。
    - **立即结束 (`end`)**: 停止代理运行并向用户展示超限说明。
    - **抛出异常 (`error`)**: 适合需要编程处理的严苛限制场景。

## 中间件配置参数

| 参数 | 类型 | 说明 |
| :--- | :--- | :--- |
| `tool_name` | `str \| None` | 要限制的工具名称。为 `None` 时限制所有工具的总和。 |
| `thread_limit` | `int \| None` | 每个线程允许的最大调用次数。 |
| `run_limit` | `int \| None` | 每次运行允许的最大调用次数。 |
| `exit_behavior` | `str` | 超限后的行为。可选值：`"continue"` (默认), `"end"`, `"error"`。 |

## 响应模式详解

### 1. `"continue"` (默认)
- **机制**: 为超限的工具调用注入一个状态为 `error` 的 `ToolMessage`。
- **给模型的消息**: `"Tool call limit exceeded. Do not call '...' again."`
- **优点**: 代理不会死掉，它被告知某个工具不可用后，可以尝试通过其他方式解决问题。

### 2. `"end"`
- **机制**: 注入错误 `ToolMessage` 后紧跟一个 `AIMessage` 说明情况，并执行 `jump_to="end"`。
- **局限性**: 如果模型同时发起了多个不同工具的并行调用，该模式会抛出 `NotImplementedError`，因为无法在保持状态一致性的前提下部分终止。

### 3. `"error"`
- **机制**: 抛出 `ToolCallLimitExceededError`。

## 核心数据结构

### `ToolCallLimitState`
包含两个字典，记录每个工具的调用频次：
- `thread_tool_call_count`: `dict[str, int]`
- `run_tool_call_count`: `dict[str, int]`

## 使用示例

```python
from langchain.agents.middleware import ToolCallLimitMiddleware
from langchain.agents import create_agent

# 限制搜索工具在整个会话中只能使用 3 次
search_limit = ToolCallLimitMiddleware(
    tool_name="search", 
    thread_limit=3, 
    exit_behavior="continue"
)

# 限制单次任务中所有工具的总调用次数不超过 10 次
global_limit = ToolCallLimitMiddleware(
    run_limit=10, 
    exit_behavior="end"
)

agent = create_agent(model="...", middleware=[search_limit, global_limit])
```

## 注意事项
1. **并行调用处理**: 在 `continue` 模式下，中间件会按顺序检查并行调用列表，一旦达到上限，后续所有匹配的调用都会被标记为错误。
2. **状态更新**: 只有被允许执行的工具调用才会增加线程级计数；而被拦截的调用仅计入运行级计数（作为一次尝试）。
3. **模型反馈**: 给模型的错误提示非常直接，旨在引导模型停止尝试受限的工具。
