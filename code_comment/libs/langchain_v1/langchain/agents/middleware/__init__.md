# Agent Middleware (代理中间件)

`middleware` 目录包含了 `langchain_v1` 中强大的代理扩展系统。中间件允许开发者通过挂钩（Hooks）机制，在代理运行、模型调用和工具调用的各个阶段注入自定义逻辑。

## 中间件分类 (Middleware Categories)

### 1. 稳定性与可靠性 (Stability & Reliability)
- **[ModelFallbackMiddleware](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain_v1/langchain/agents/middleware/model_fallback.md)**: 主模型失败时自动切换备选模型。
- **[ModelRetryMiddleware](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain_v1/langchain/agents/middleware/model_retry.md)**: 模型调用失败时带退避策略的重试。
- **[ToolRetryMiddleware](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain_v1/langchain/agents/middleware/tool_retry.md)**: 工具调用失败时带退避策略的重试。

### 2. 上下文与 Token 管理 (Context & Token Management)
- **[ContextEditingMiddleware](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain_v1/langchain/agents/middleware/context_editing.md)**: 自动清理旧的工具结果以释放 Token 空间。
- **[SummarizationMiddleware](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain_v1/langchain/agents/middleware/summarization.md)**: 自动总结长对话历史。
- **[LLMToolSelectorMiddleware](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain_v1/langchain/agents/middleware/tool_selection.md)**: 从大量工具中预选最相关的工具，减少 Token 浪费。

### 3. 安全与合规 (Security & Compliance)
- **[PIIMiddleware](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain_v1/langchain/agents/middleware/pii.md)**: 自动检测并脱敏对话中的个人隐私信息。
- **[ShellToolMiddleware](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain_v1/langchain/agents/middleware/shell_tool.md)**: 提供安全的、带策略控制的持久化 Shell 访问。

### 4. 资源限制 (Resource Limits)
- **[ModelCallLimitMiddleware](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain_v1/langchain/agents/middleware/model_call_limit.md)**: 限制单次任务或线程内的模型调用次数。
- **[ToolCallLimitMiddleware](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain_v1/langchain/agents/middleware/tool_call_limit.md)**: 限制工具的调用频率或总量。

### 5. 增强功能与开发工具 (Enhancements & Dev Tools)
- **[TodoListMiddleware](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain_v1/langchain/agents/middleware/todo.md)**: 为代理提供结构化的任务规划和进度管理能力。
- **[HumanInTheLoopMiddleware](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain_v1/langchain/agents/middleware/human_in_the_loop.md)**: 在敏感工具执行前引入人工审批。
- **[FilesystemFileSearchMiddleware](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain_v1/langchain/agents/middleware/file_search.md)**: 为代理注入高效的文件搜索工具。
- **[LLMToolEmulator](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain_v1/langchain/agents/middleware/tool_emulator.md)**: 使用 LLM 模拟工具输出，加速测试。

## 核心机制 (Core Mechanism)

中间件通过继承 `AgentMiddleware` 类并实现以下一个或多个钩子来工作：

- `before_agent`: 在代理逻辑启动前运行。
- `after_agent`: 在代理逻辑结束后运行。
- `before_model`: 在模型调用前修改请求。
- `after_model`: 在模型返回响应后处理结果。
- `wrap_model_call`: 包装整个模型调用过程（常用于重试、回退）。
- `wrap_tool_call`: 包装整个工具调用过程（常用于拦截、模拟）。

## 使用方式 (Usage)

在创建代理时，通过 `middleware` 参数传入中间件实例列表：

```python
from langchain.agents import create_agent
from langchain.agents.middleware import ModelRetryMiddleware, PIIMiddleware

agent = create_agent(
    model=model,
    tools=tools,
    middleware=[
        ModelRetryMiddleware(),
        PIIMiddleware()
    ]
)
```

