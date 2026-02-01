# LangChain Classic Chains

本目录包含了 LangChain 传统的 **Chain (链)** 架构实现。这些组件在 LangChain 的早期版本中是核心，虽然现在大部分已被 **LCEL (LangChain Expression Language)** 和 **LangGraph** 所取代，但它们在现有代码库和某些特定场景中仍具有重要价值。

## 核心架构

所有链都继承自 [Chain 基类](./base.md)，提供了统一的接口：
- **状态管理**: 集成 Memory 系统。
- **可观察性**: 内置 Callback 钩子。
- **组合能力**: 支持嵌套和顺序执行。

## 主要子模块

### 1. 基础构建块
- [LLMChain](./llm.md): 最基础的链，连接提示词、模型和解析器。
- [SequentialChain](./sequential.md): 按顺序执行多个子链。
- [TransformChain](./transform.md): 用于对输入数据进行自定义 Python 函数转换。

### 2. 文档处理与问答
- [Combine Documents](./combine_documents/base.md): 包含 Stuff, Map-Reduce, Refine 等文档合并策略。
- [Retrieval QA](./retrieval_qa/base.md): 基于检索器的问答系统。
- [Conversational Retrieval](./conversational_retrieval/base.md): 支持对话历史的检索问答。

### 3. 特定任务链
- [SQL Database](./sql_database/base.md): 自然语言转 SQL 查询。
- [API Chain](./api/base.md): 与 REST API 进行自然语言交互。
- [Graph QA](./graph_qa/base.md): 基于图数据库（Neo4j等）的问答。
- [Constitutional AI](./constitutional_ai/base.md): 带有自我修正和准则审查的链。

### 4. 路由与分发
- [Router](./router/base.md): 根据输入内容自动选择最佳的下游链。

## 弃用与迁移指南

大多数 Classic Chains 已被标记为弃用（Deprecated）。

| 弃用组件 | 现代替代方案 |
| :--- | :--- |
| `LLMChain` | `prompt | llm | output_parser` (LCEL) |
| `RetrievalQA` | `create_retrieval_chain` |
| `ConversationalRetrievalChain` | `create_history_aware_retriever` + `create_retrieval_chain` |
| `AgentExecutor` | [LangGraph ReAct Agent](https://langchain-ai.github.io/langgraph/how-tos/create-react-agent/) |
| `SequentialChain` | LCEL 管道操作符 `|` |

## 设计哲学

Classic Chains 采用了“黑盒”式的设计，将复杂的逻辑封装在类内部。虽然易于上手，但在灵活性和透明度上不如现代的 LCEL 架构。建议在新项目中优先选择 LCEL 和 LangGraph。
