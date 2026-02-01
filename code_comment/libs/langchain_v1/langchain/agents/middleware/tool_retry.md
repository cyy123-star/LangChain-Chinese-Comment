# Tool Retry Middleware (工具调用重试中间件)

`tool_retry.py` 实现了 `ToolRetryMiddleware`，它在工具执行失败时自动执行带退避策略的重试。

## 核心功能 (Core Features)

1.  **自动重试**: 捕获工具执行过程中的异常并自动发起重试。
2.  **细粒度控制**: 可以指定仅对特定的工具或特定的异常类型应用重试逻辑。
3.  **灵活的退避策略**: 支持指数退避、固定延迟和随机抖动。
4.  **失败处理机制**: 支持在重试失败后抛出错误或返回包含错误信息的 `ToolMessage` 告知 LLM 错误原因。

## 类定义与参数 (Class Definition & Parameters)

### `ToolRetryMiddleware`

| 参数 | 类型 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- |
| `max_retries` | `int` | `2` | 初始调用之后的重试次数。 |
| `tools` | `list[BaseTool \| str] \| None` | `None` | 指定应用重试的工具列表。`None` 表示所有工具。 |
| `retry_on` | `RetryOn` | `(Exception,)` | 指定哪些异常触发重试。 |
| `on_failure` | `OnFailure` | `'continue'` | 重试耗尽后的行为 (`'continue'`, `'error'`, 或自定义函数)。 |
| `backoff_factor` | `float` | `2.0` | 指数退避倍数。`0.0` 表示固定延迟。 |
| `initial_delay` | `float` | `1.0` | 第一次重试前的延迟秒数。 |
| `max_delay` | `float` | `60.0` | 最大延迟秒数。 |
| `jitter` | `bool` | `True` | 是否增加随机抖动。 |

## 执行逻辑 (Execution Logic)

1.  **工具过滤**: 在 `wrap_tool_call` 中首先判断当前工具是否在 `self.tools` 监控范围内。
2.  **重试循环**:
    - 调用 `handler(request)` 执行工具。
    - 如果捕获到符合 `retry_on` 的异常且未达到 `max_retries`：
        - 计算并执行延迟。
        - 增加重试计数并重新尝试。
    - 如果不满足重试条件，调用 `_handle_failure`。

3.  **失败处理 (`_handle_failure`)**:
    - 如果 `on_failure == 'error'`，抛出原始异常。
    - 如果 `on_failure == 'continue'`，返回一个包含错误信息的 `ToolMessage`。这通常会让 LLM 意识到工具出错了，并尝试其他方法或报告错误。

## 使用示例 (Example Usage)

```python
from langchain.agents import create_agent
from langchain.agents.middleware import ToolRetryMiddleware

# 为特定的数据库查询工具配置重试
retry_mw = ToolRetryMiddleware(
    max_retries=3,
    tools=["query_database"],
    initial_delay=2.0
)

agent = create_agent(model, tools=[query_database, other_tool], middleware=[retry_mw])
```
