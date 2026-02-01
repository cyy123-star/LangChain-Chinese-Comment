# Agents (v1) 模块

`agents` 模块是 LangChain v1 的核心，它基于 **LangGraph** 构建了一个高度灵活、可扩展且生产就绪的代理系统。

## 核心定位
不同于传统的 `AgentExecutor`，v1 的代理系统采用了“图形即代码”的理念，将代理逻辑表示为有状态的图。这带来了以下优势：
- **循环控制**：显式定义模型调用、工具执行和状态更新的循环。
- **中间件支持**：通过 `middleware` 系统，可以轻松插入日志、重试、敏感信息脱敏等横切关注点。
- **结构化输出**：内置对 Pydantic 和 JSON Schema 的支持，确保代理返回符合预期的结果。
- **状态持久化**：原生支持 Checkpointer，实现对话记忆和断点续传。

## 主要组件

### [factory.py](factory.md)
包含 `create_agent` 工厂函数，这是创建现代代理的标准入口。它负责：
- 初始化聊天模型（支持模型字符串标识）。
- 配置工具集。
- 组装中间件栈。
- 处理结构化输出策略。

### [middleware/](middleware/__init__.md)
一个强大的插件系统，允许在代理运行的各个阶段（模型调用前/后、工具执行前/后）注入自定义逻辑。

### [structured_output.md](structured_output.md)
定义了多种结构化输出策略（如 `ToolStrategy`, `ProviderStrategy`），用于控制模型如何生成结构化数据。

## 使用建议
对于新项目，强烈建议使用 `create_agent` 而非 `langchain_classic` 中的 `initialize_agent`。它不仅性能更好，而且更容易调试和维护。

