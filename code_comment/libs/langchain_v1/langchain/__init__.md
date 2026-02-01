# LangChain v1 (Main) 模块概览

## 模块定位
`langchain_v1`（在代码库中对应 `libs/langchain_v1`）是 LangChain 1.2.7 版本中的**主应用层**。它不同于 `langchain-classic`，主要聚焦于：
1. **LangGraph 集成**：提供与有状态图编排框架的深度整合。
2. **现代代理架构**：推荐使用基于 LangGraph 的智能代理，而非传统的 `AgentExecutor`。
3. **统一工厂接口**：通过 `init_chat_model` 等函数简化多供应商模型的初始化。

## 目录结构
- **[agents/](agents/factory.md)**: 现代智能代理的工厂类和结构化输出支持。
- **[chat_models/](chat_models/base.md)**: 统一的聊天模型初始化接口。
- **[tools/](tools/tool_node.md)**: 与 LangGraph 配合使用的工具执行节点。
- **[embeddings/](embeddings/base.md)**: 统一的嵌入模型接口。
- **[rate_limiters/](rate_limiters/__init__.md)**: 速率限制器支持。

## 核心设计理念
LangChain v1 的设计目标是解耦。核心抽象留在 `langchain-core`，而具体的应用组合逻辑（尤其是复杂的循环代理逻辑）则通过 `langchain` (v1) 配合 `langgraph` 来实现。

## 学习建议
如果你正在开发新的 LLM 应用，建议优先参考本模块中的组件，特别是使用 LCEL 和 LangGraph 来构建你的业务逻辑。
