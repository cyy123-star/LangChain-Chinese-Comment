# libs\langchain_v1\langchain\agents\factory.py

`factory.py` 是 LangChain v1 中创建代理的核心工厂模块。它引入了基于 **LangGraph** 的现代化代理构建方式，支持 **Middleware (中间件)** 系统和 **Structured Output (结构化输出)**。

## 核心函数：`create_agent`

`create_agent` 是创建代理图（Agent Graph）的统一入口。它将模型、工具和中间件组合成一个可编译的 LangGraph 状态图。

### 参数说明

| 参数 | 类型 | 描述 |
| :--- | :--- | :--- |
| `model` | `str \| BaseChatModel` | 代理使用的语言模型。如果是字符串，将通过 `init_chat_model` 初始化。 |
| `tools` | `Sequence[BaseTool \| Callable]` | 代理可以调用的工具列表。 |
| `system_prompt` | `str \| SystemMessage` | 代理的系统提示词，定义其角色和行为。 |
| `middleware` | `Sequence[AgentMiddleware]` | 中间件序列，用于拦截和修改代理、模型或工具的调用过程。 |
| `response_format` | `ResponseFormat \| type[ResponseT]` | 指定代理的输出格式（如 Pydantic 模型或 JSON Schema）。 |
| `state_schema` | `type[AgentState]` | 自定义代理的状态模式。默认为 `AgentState`。 |
| `checkpointer` | `Checkpointer` | 用于持久化代理状态的检查点。 |
| `interrupt_before` | `list[str]` | 在进入指定节点前中断执行。 |
| `interrupt_after` | `list[str]` | 在退出指定节点后中断执行。 |
| `debug` | `bool` | 是否开启调试模式，输出详细执行日志。 |

### 执行逻辑

1. **中间件链初始化**: 将传入的 `middleware` 序列组合成嵌套的调用栈（Middleware Stack）。第一个中间件处于最外层。
2. **状态图构建**: 
   - 使用 `StateGraph` 定义代理的执行流程。
   - 核心节点包括 `agent`（决策节点）和 `tools`（执行节点）。
3. **循环迭代**: 
   - 代理根据当前 `messages` 决定调用工具或直接回复。
   - 如果调用工具，则进入 `tools` 节点，执行后将 `ToolMessage` 返回给代理。
   - 如果满足停止条件（如生成了最终回复或达到了最大调用次数），则结束流程。

## 核心机制

### 1. 中间件组合 (`_chain_model_call_handlers`)
该模块内部使用递归方式将多个中间件的 `wrap_model_call` 处理器组合在一起。
- **外层优先**: 序列中前面的中间件会包裹后面的中间件。
- **请求/响应拦截**: 中间件可以在模型调用前后修改 `ModelRequest` 或 `ModelResponse`。

### 2. 动态工具支持
如果在中间件中动态添加了工具（即不在 `create_agent` 初始列表中的工具），需要注意：
- 必须在 `wrap_tool_call` 中手动处理这些动态工具的执行。
- 否则，代理会因为找不到对应的工具执行器而报错。

### 3. 错误恢复模板
模块定义了 `STRUCTURED_OUTPUT_ERROR_TEMPLATE`，当结构化输出解析失败时，会自动将错误信息反馈给模型，引导其修正输出。

## 使用示例

```python
from langchain.agents import create_agent
from langchain.agents.middleware import ModelRetryMiddleware

# 定义一个带重试机制的代理
agent = create_agent(
    model="gpt-4o",
    tools=[my_tool],
    middleware=[ModelRetryMiddleware(max_attempts=3)],
    system_prompt="你是一个专业的助手。"
)

# 编译并运行
app = agent.compile()
result = app.invoke({"messages": [("user", "执行任务")]})
```

## 注意事项
- **LangGraph 依赖**: `create_agent` 返回的是一个 `CompiledStateGraph`，需要通过 `invoke`、`stream` 等方法运行。
- **状态一致性**: 确保自定义的 `state_schema` 与中间件中使用的数据结构保持兼容。
