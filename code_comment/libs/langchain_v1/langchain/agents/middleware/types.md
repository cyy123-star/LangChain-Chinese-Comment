# Middleware Types (中间件类型定义)

`types.py` 定义了 LangChain v1 中间件系统的核心数据结构和协议。

## 核心模型

### `ModelRequest`
表示发给 LLM 的请求信息。它是**不可变**的，修改属性需要使用 `override()` 方法。
- **属性**:
  - `model`: `BaseChatModel` 实例。
  - `messages`: 消息列表（不含系统消息）。
  - `system_message`: `SystemMessage` 实例。
  - `tools`: 可用工具列表。
  - `tool_choice`: 工具选择策略。
  - `response_format`: 结构化输出格式。
  - `state`: 当前代理状态。
  - `runtime`: 运行时上下文。

### `ModelResponse`
表示 LLM 返回的结果。
- **属性**:
  - `result`: 返回的消息列表（通常是一个 `AIMessage`）。
  - `structured_response`: 如果请求了结构化输出，这里存放解析后的 Python 对象。

## 核心接口

### `AgentMiddleware`
所有中间件的抽象基类。通过继承此类并重写特定钩子方法来定制代理行为。

| 钩子方法 | 执行时机 | 典型用途 |
| :--- | :--- | :--- |
| `before_agent` | 代理图启动前 | 初始化状态、注入上下文信息。 |
| `before_model` | 每次调用 LLM 前 | 动态修改 Prompt、调整工具集。 |
| `wrap_model_call` | 包裹 LLM 调用 | **核心钩子**。用于重试、缓存、模拟输出。 |
| `after_model` | LLM 返回结果后 | 处理 Jump 逻辑、日志记录。 |
| `wrap_tool_call` | 包裹工具执行 | 权限校验、结果拦截、脱敏。 |

## 状态管理

### `AgentState`
定义了代理图的状态架构。
- `messages`: 消息序列。
- `jump_to`: 控制图跳转的临时变量（如跳过工具执行直接结束）。
- `structured_response`: 存放最终的结构化结果。

## 辅助标记
- `OmitFromInput`: 标记状态属性不作为输入 Schema 的一部分。
- `PrivateStateAttr`: 标记状态属性为中间件内部私有，不对外暴露。

