# Retry Utilities (重试通用工具)

`_retry.py` 模块包含了模型和工具重试中间件共享的通用常量、类型定义和逻辑。

## 核心组件 (Core Components)

### 类型定义 (Type Aliases)

- **`RetryOn`**: 指定触发重试的异常。
    - `tuple[type[Exception], ...]`: 异常类型元组。
    - `Callable[[Exception], bool]`: 接收异常并返回是否需要重试的布尔值的函数。
- **`OnFailure`**: 指定重试次数耗尽后的处理行为。
    - `'error'`: 重新抛出异常，停止代理运行。
    - `'continue'`: 注入包含错误信息的辅助消息（`ToolMessage` 或 `AIMessage`），允许代理继续运行。
    - `Callable[[Exception], str]`: 接收异常并返回自定义错误消息字符串的函数。

## 核心函数 (Core Functions)

### `validate_retry_params`
验证重试参数（`max_retries`, `initial_delay`, `max_delay`, `backoff_factor`）是否合法（非负）。

### `should_retry_exception`
检查当前异常是否匹配 `RetryOn` 的定义。

### `calculate_delay`
计算重试延迟时间，支持：
- **指数退避 (Exponential Backoff)**: 延迟随重试次数按 `backoff_factor` 指数增长。
- **最大延迟限制 (`max_delay`)**: 限制退避增长的上限。
- **抖动 (Jitter)**: 增加 `±25%` 的随机抖动，防止“惊群效应”。

## 计算公式 (Calculation Logic)

1.  如果 `backoff_factor == 0.0`，则 `delay = initial_delay`（固定延迟）。
2.  否则，`delay = initial_delay * (backoff_factor ** retry_number)`。
3.  应用 `min(delay, max_delay)`。
4.  如果开启抖动，`delay = delay + random.uniform(-0.25 * delay, 0.25 * delay)`。

