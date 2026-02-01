# PII Middleware (个人隐私信息保护中间件)

`pii.py` 实现了 `PIIMiddleware`，它利用 `_redaction.py` 中的工具来监控和脱敏代理对话中的个人隐私信息（PII）。

## 核心定位
该中间件的主要作用是在对话流程的多个环节（用户输入、模型输出、工具返回结果）自动拦截并处理敏感数据，防止隐私泄露给 LLM 服务商或最终用户。

## 主要特性

- **全流程覆盖**: 支持对 `HumanMessage`、`AIMessage` 和 `ToolMessage` 进行扫描。
- **可配置的作用范围**: 可以独立开启对输入 (`apply_to_input`)、输出 (`apply_to_output`) 或工具执行结果 (`apply_to_tool_results`) 的检查。
- **灵活的策略选择**: 继承了 `_redaction.py` 的所有策略（`block`, `redact`, `mask`, `hash`）。
- **同步/异步支持**: 提供了 `before_model`/`abefore_model` 和 `after_model`/`aafter_model` 的完整实现。

## 中间件配置参数

| 参数 | 类型 | 说明 |
| :--- | :--- | :--- |
| `pii_type` | `str` | 要检测的类型（如 `"email"`, `"credit_card"`, `"ip"` 等）。 |
| `strategy` | `str` | 处理策略，默认为 `"redact"`。 |
| `detector` | `Callable \| str` | 自定义检测函数或正则表达式。若为 `None` 则使用内置检测器。 |
| `apply_to_input` | `bool` | 是否检查用户消息（默认为 `True`）。 |
| `apply_to_output` | `bool` | 是否检查 AI 消息（默认为 `False`）。 |
| `apply_to_tool_results` | `bool` | 是否检查工具执行结果（默认为 `False`）。 |

## 工作原理

### 1. `before_model` (模型调用前)
- 扫描消息列表中的最后一条 `HumanMessage`。
- 如果开启了 `apply_to_tool_results`，则扫描最后一条 `AIMessage` 之后的所有 `ToolMessage`。
- 如果检测到敏感信息并配置了 `block` 策略，则抛出 `PIIDetectionError` 阻止请求。
- 否则，使用配置的策略修改消息内容并更新状态。

### 2. `after_model` (模型调用后)
- 扫描模型刚刚生成的 `AIMessage`。
- 如果发现敏感信息，则根据策略对内容进行脱敏，确保返回给用户的内容是安全的。

## 使用示例

```python
from langchain.agents.middleware import PIIMiddleware
from langchain.agents import create_agent

# 1. 简单的邮箱脱敏
middleware = [PIIMiddleware("email", strategy="redact")]

# 2. 对工具输出的 IP 地址进行哈希处理
middleware = [
    PIIMiddleware("ip", strategy="hash", apply_to_tool_results=True)
]

# 3. 使用正则阻塞 API Key 的发送
middleware = [
    PIIMiddleware("api_key", detector=r"sk-[a-zA-Z0-9]{32}", strategy="block")
]

agent = create_agent(model="...", middleware=middleware)
```

## 注意事项
1. **性能开销**: 复杂的正则检测或大量的文本扫描可能会增加响应延迟。
2. **误报风险**: 掩码（`mask`）和脱敏（`redact`）可能会改变文本语义，导致 LLM 理解出现偏差。
3. **安全边界**: 中间件是在应用程序层面运行的。如果攻击者有办法绕过中间件逻辑（例如通过复杂的提示工程），仍可能存在风险。
