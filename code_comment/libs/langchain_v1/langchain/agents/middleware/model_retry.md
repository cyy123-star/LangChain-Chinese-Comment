# Model Retry Middleware (模型调用重试中间件)

`model_retry.py` 实现了 `ModelRetryMiddleware`，它在模型调用（LLM）失败时自动执行带退避策略的重试。

## 核心功能 (Core Features)

1.  **自动重试**: 捕获模型调用过程中的异常并自动发起重试。
2.  **灵活的退避策略**: 支持指数退避、固定延迟和随机抖动。
3.  **异常过滤**: 可以配置仅针对特定的异常类型（如 `RateLimitError`, `Timeout`）进行重试。
4.  **失败处理机制**: 支持在重试失败后抛出错误或返回包含错误信息的 `AIMessage` 引导代理继续处理。

## 类定义与参数 (Class Definition & Parameters)

### `ModelRetryMiddleware`

| 参数 | 类型 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- |
| `max_retries` | `int` | `2` | 初始调用之后的重试次数。 |
| `retry_on` | `RetryOn` | `(Exception,)` | 指定哪些异常触发重试。 |
| `on_failure` | `OnFailure` | `'continue'` | 重试耗尽后的行为 (`'continue'`, `'error'`, 或自定义函数)。 |
| `backoff_factor` | `float` | `2.0` | 指数退避倍数。`0.0` 表示固定延迟。 |
| `initial_delay` | `float` | `1.0` | 第一次重试前的延迟秒数。 |
| `max_delay` | `float` | `60.0` | 最大延迟秒数。 |
| `jitter` | `bool` | `True` | 是否增加随机抖动。 |

## 执行逻辑 (Execution Logic)

1.  **请求包装 (`wrap_model_call`)**:
    - 在循环中调用 `handler(request)`。
    - 如果捕获到符合 `retry_on` 的异常且未达到 `max_retries`：
        - 计算延迟时间。
        - 记录日志。
        - 等待（支持 `asyncio.sleep` 或 `time.sleep`）。
        - 增加重试计数并继续。
    - 如果达到最大重试次数或捕获到不匹配的异常，调用 `_handle_failure`。

2.  **失败处理 (`_handle_failure`)**:
    - 如果 `on_failure == 'error'`，抛出异常。
    - 如果 `on_failure == 'continue'`，返回一个包含错误描述的 `AIMessage` 作为响应。

## 使用示例 (Example Usage)

```python
from langchain.agents import create_agent
from langchain.agents.middleware import ModelRetryMiddleware
from openai import RateLimitError

# 配置重试：最多4次，仅限速率限制错误，指数倍数为1.5
retry_mw = ModelRetryMiddleware(
    max_retries=4,
    retry_on=(RateLimitError,),
    backoff_factor=1.5
)

agent = create_agent(model, tools=tools, middleware=[retry_mw])
```
