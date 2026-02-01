# LangChain Classic (传统接口层)

`langchain_classic` 是 LangChain 框架中的一个重要包，它保留了 LangChain v0.0.x 时代的传统接口和组件实现。

## 项目定位

随着 LangChain 迈向 v0.2 和 v0.3 版本，核心架构已经转向了 **LCEL (LangChain Expression Language)** 和 **LangGraph**。为了保证向下兼容性，许多传统的 Chain、Agent 和工具类被保留在 `langchain_classic` 中。

## 核心组件概览

| 模块 | 说明 |
| :--- | :--- |
| `chains` | 包含传统的顺序链（Sequential）、映射归约（Map-Reduce）等预定义链。 |
| `agents` | 包含 ReAct、MRKL、对话式 Agent 等传统执行器实现。 |
| `runnables` | LCEL 的底层基石，定义了 `invoke`, `stream`, `batch` 等统一接口。 |
| `schema` | 定义了消息（Message）、文档（Document）等核心数据结构。 |
| `base_memory` | 传统的记忆组件基类，用于维护对话状态。 |
| `cache` | 跨模型的 LLM 响应缓存系统。 |

## 目录结构说明

- **`_api`**: 内部使用的 API 工具，主要负责处理弃用警告和动态导入。
- **`adapters`**: 与第三方 SDK（如 OpenAI）的兼容适配层。
- **`chat_loaders`**: 用于从 Slack, WhatsApp, Gmail 等平台加载对话数据的工具。
- **`evaluation`**: 用于衡量 LLM 输出质量的评估框架。
- **`utilities`**: 各种第三方 API（如 Google Search, SQL）的底层客户端封装。

## 开发建议

1. **新项目**: 强烈建议优先使用 `langchain-core` 中的 LCEL 接口和 `LangGraph` 来构建应用。
2. **迁移**: 对于存量项目，可以参考各子目录下的 `README.md` 中的“迁移指南”逐步将传统 Chain 转换为 LCEL 形式。
3. **集成分离**: 许多具体的模型和工具实现已经移至 `langchain-openai`, `langchain-community` 等包中。

## 快速导航

- [Chains 详细文档](./chains/README.md)
- [Agents 详细文档](./agents/README.md)
- [LCEL (Runnables) 文档](./runnables/README.md)
- [Memory 迁移指南](./base_memory.md)
- [向后兼容层说明](./compatibility.md)
