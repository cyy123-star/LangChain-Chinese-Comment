# Human In The Loop Middleware (人工干预中间件)

`human_in_the_loop.py` 实现了 `HumanInTheLoopMiddleware`，它允许在代理执行特定敏感工具前拦截操作，并请求人工审查、修改或拒绝。

## 核心功能 (Core Features)

1.  **操作拦截**: 在工具调用执行前触发中断（Interrupt）。
2.  **细粒度配置**: 可以针对不同的工具配置不同的审批策略。
3.  **三种决策支持**:
    - **Approve (批准)**: 直接执行。
    - **Edit (修改)**: 修改工具参数后再执行。
    - **Reject (拒绝)**: 不执行，并将拒绝原因反馈给模型。
4.  **动态描述**: 支持通过字符串或回调函数动态生成展示给人类的审批描述信息。

## 核心组件 (Core Components)

### `InterruptOnConfig` (配置字典)

| 字段 | 类型 | 说明 |
| :--- | :--- | :--- |
| `allowed_decisions` | `list[DecisionType]` | 允许的决策类型（`approve`, `edit`, `reject`）。 |
| `description` | `str \| Callable` | 展示给人类的描述信息或生成函数。 |
| `args_schema` | `dict` (可选) | 如果允许 `edit`，可提供 JSON Schema 校验修改后的参数。 |

### `HumanInTheLoopMiddleware`

| 参数 | 类型 | 说明 |
| :--- | :--- | :--- |
| `interrupt_on` | `dict[str, bool \| InterruptOnConfig]` | 工具名到配置的映射。`True` 表示开启全功能审批。 |
| `description_prefix` | `str` | 默认的描述前缀。 |

## 执行逻辑 (Execution Logic)

1.  **工具拦截 (`wrap_tool_call`)**:
    - 检查当前工具是否在 `interrupt_on` 配置中。
    - 如果需要审批，调用 `langgraph.types.interrupt` 挂起当前线程。
    - 此时代理会停止运行，等待外部（如 UI 或 CLI）输入 `HITLResponse`。
2.  **恢复执行**:
    - 接收到人类决策后，中间件恢复运行。
    - 根据 `Decision` 类型执行对应逻辑（继续调用 `handler`、修改参数后调用、或直接返回拒绝消息）。

## 使用示例 (Example Usage)

```python
from langchain.agents.middleware import HumanInTheLoopMiddleware

# 为敏感操作配置人工审批
hitl_mw = HumanInTheLoopMiddleware(
    interrupt_on={
        "delete_database": True,  # 全部允许
        "send_email": {
            "allowed_decisions": ["approve", "reject"],
            "description": "发送邮件前需要确认"
        }
    }
)

agent = create_agent(model, tools=tools, middleware=[hitl_mw])
```

