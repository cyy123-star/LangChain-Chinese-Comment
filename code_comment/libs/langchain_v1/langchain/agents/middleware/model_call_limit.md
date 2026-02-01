# Model Call Limit Middleware (模型调用次数限制中间件)

`model_call_limit.py` 实现了 `ModelCallLimitMiddleware`，用于监控和限制代理调用 LLM 的次数，防止陷入死循环或超出预算。

## 核心定位
该中间件提供了对代理运行成本和生命周期的精细化控制。它通过在状态中维护计数器，确保代理在达到预设的调用上限时能够及时停止。

## 主要特性

- **双层计数机制**:
    - **线程级 (`thread_level`)**: 跨多次运行（Run）持久化计数，适用于限制整个会话的总成本。
    - **运行级 (`run_level`)**: 单次运行（Invoke）内计数，适用于限制单个任务的推理深度。
- **灵活的退出策略**: 支持静默结束（返回说明消息）或抛出异常。
- **状态感知**: 自动更新 `AgentState` 中的计数器字段。

## 中间件配置参数

| 参数 | 类型 | 说明 |
| :--- | :--- | :--- |
| `thread_limit` | `int \| None` | 每个线程允许的最大模型调用总数。`None` 表示不限制。 |
| `run_limit` | `int \| None` | 每次运行允许的最大模型调用数。`None` 表示不限制。 |
| `exit_behavior` | `str` | 达到上限后的行为。可选值：`"end"` (默认) 或 `"error"`。 |

## 退出行为说明

### 1. `"end"` (默认)
- **行为**: 代理立即停止当前任务。
- **反馈**: 在消息列表中追加一条人工生成的 `AIMessage`，说明超出了哪项限制（例如：`Model call limits exceeded: run limit (5/5)`）。
- **优点**: 体验平滑，用户可以看到代理停止的原因。

### 2. `"error"`
- **行为**: 抛出 `ModelCallLimitExceededError` 异常。
- **优点**: 适合在代码中捕获异常并进行特定的错误处理。

## 核心数据结构

### `ModelCallLimitState`
扩展了 `AgentState`，包含以下私有属性：
- `thread_model_call_count`: 当前线程的总调用次数。
- `run_model_call_count`: 当前运行的调用次数。

## 使用示例

```python
from langchain.agents.middleware import ModelCallLimitMiddleware
from langchain.agents import create_agent

# 限制单次任务最多调用 5 次模型，超出时报错
middleware = [
    ModelCallLimitMiddleware(run_limit=5, exit_behavior="error")
]

agent = create_agent(model="...", middleware=middleware)
```

## 注意事项
1. **死循环防护**: 它是防止代理由于 Prompt 问题或 Tool 循环调用而产生高昂账单的第一道防线。
2. **状态持久化**: 线程级计数依赖于 LangGraph 的 `Checkpointer`。如果没有配置持久化，线程级计数将回退为单次运行计数。
3. **计数时机**: 计数是在 `after_model` 钩子中增加的，这意味着只有成功的模型响应才会被计入。
