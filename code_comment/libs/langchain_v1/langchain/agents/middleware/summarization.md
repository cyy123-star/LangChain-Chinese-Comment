# Summarization Middleware (会话总结中间件)

`summarization.py` 实现了 `SummarizationMiddleware`，它在会话接近 Token 限制时，自动利用 LLM 对旧的对话历史进行总结，从而在保留关键上下文的同时释放空间。

## 核心功能 (Core Features)

1.  **自动触发**: 基于消息数量或 Token 数量触发总结。
2.  **结构化总结**: 使用预定义的 Prompt 生成包含“会话意图”、“总结”、“产物”和“下一步”的结构化摘要。
3.  **上下文保留策略**: 支持配置总结后保留多少最近的消息或 Token。
4.  **智能裁剪**: 确保 AI 消息与其工具响应消息对成对保留，避免上下文断裂。

## 类定义与参数 (Class Definition & Parameters)

### `SummarizationMiddleware`

| 参数 | 类型 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- |
| `model` | `str \| BaseChatModel` | - | 用于执行总结任务的模型。 |
| `trigger` | `ContextSize \| list[ContextSize]` | `None` | 触发阈值（消息数、Token 数或模型限制比例）。 |
| `keep` | `ContextSize` | `("messages", 20)` | 总结后保留的上下文量。 |
| `summary_prompt` | `str` | `DEFAULT_SUMMARY_PROMPT` | 自定义总结用的系统提示词。 |

### `ContextSize` 类型说明
- `("fraction", 0.8)`: 模型最大输入 Token 的 80%。
- `("tokens", 3000)`: 固定 3000 Token。
- `("messages", 50)`: 固定 50 条消息。

## 执行逻辑 (Execution Logic)

1.  **状态监控**: 拦截 `before_agent` 钩子，检查当前 `AgentState` 中的消息列表。
2.  **触发条件**: 如果满足任何 `trigger` 条件：
    - 根据 `keep` 策略确定需要被总结的“旧消息”和需要保留的“新消息”。
    - 调用 `model` 对旧消息进行总结，生成一段结构化的文本。
    - 将总结结果作为一条新的 `HumanMessage` 或系统提示的一部分（取决于具体实现）。
    - 发送 `RemoveMessage` 指令给 LangGraph 状态机，删除已被总结的旧消息。
3.  **无缝衔接**: 代理继续运行，看到的将是：`[总结消息] + [保留的最近消息]`。

## 默认总结模板 (`DEFAULT_SUMMARY_PROMPT`)

模板要求模型提取以下四个维度的信息：
- **SESSION INTENT**: 用户的主要目标。
- **SUMMARY**: 关键决策、结论和推理。
- **ARTIFACTS**: 创建或修改的文件路径及变更。
- **NEXT STEPS**: 待完成的具体任务。

## 使用示例 (Example Usage)

```python
from langchain.agents.middleware import SummarizationMiddleware

# 当消息超过 50 条时触发总结，保留最近 15 条
summary_mw = SummarizationMiddleware(
    model="gpt-4o-mini",
    trigger=("messages", 50),
    keep=("messages", 15)
)

agent = create_agent(model, tools=tools, middleware=[summary_mw])
```

