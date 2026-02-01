# API 参考手册

本手册汇总了 LangChain 核心模块的主要 API。详细信息请参考 `code_comment/` 目录下的对应文档。

## langchain_core (核心抽象层)

### [Runnables](../code_comment/libs/core/langchain_core/runnables/base.md)
- `Runnable`: 所有可运行对象的基类。
- `RunnableLambda`: 将 Python 函数转换为 Runnable。
- `RunnableParallel`: 并行运行多个 Runnable。
- `RunnableSequence`: 顺序运行多个 Runnable (即 `|` 操作符的底层实现)。

### [Prompts](../code_comment/libs/core/langchain_core/prompts/base.md)
- `BasePromptTemplate`: 提示词模板基类。
- `PromptTemplate`: 用于纯文本提示词。
- `ChatPromptTemplate`: 用于聊天模型消息列表。

### [Messages](../code_comment/libs/core/langchain_core/messages/base.md)
- `HumanMessage`: 用户消息。
- `AIMessage`: 模型消息。
- `SystemMessage`: 系统消息。
- `ToolMessage`: 工具返回结果消息。

### [Language Models](../code_comment/libs/core/langchain_core/language_models/base.md)
- `BaseLanguageModel`: 语言模型基类。
- `BaseChatModel`: 聊天模型基类。

## langchain (应用层)

### [langchain-classic (经典组件)](../code_comment/libs/langchain/langchain_classic/__init__.md)
包含传统的链式结构和代理实现：
- `LLMChain`: 最基础的链（已逐渐被 LCEL 取代）。
- `RetrievalQA`: 用于问答任务的链。
- `AgentExecutor`: 代理执行器。

### [langchain-main (新版应用)](../code_comment/libs/langchain_v1/langchain/__init__.md)
当前推荐的主应用包，包含：
- **LangGraph 集成**: 支持更复杂的有状态代理。
- **新版 Agents**: 基于 LangGraph 的智能代理实现。

---
*注：更多模块正在持续更新中...*
