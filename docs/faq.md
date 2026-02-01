# 常见问题解答 (FAQ)

## 1. 什么是 LCEL？
LCEL 全称 LangChain Expression Language（LangChain 表达式语言）。它是一种声明式的方式，允许你通过 `|` 操作符将不同的组件（Prompt, Model, Parser 等）连接起来。它的优势在于支持自动并行化、异步调用、流式输出以及中间步骤的追踪。

## 2. 为什么 `invoke` 和 `batch` 的表现不一致？
通常情况下，`batch` 是在线程池中并行调用 `invoke` 的封装。如果某个组件（如某些本地模型）不支持并发调用，可能会导致性能下降或报错。你可以通过在 `config` 中设置 `max_concurrency` 来限制并发数。

## 3. 如何在链中添加日志或调试信息？
有两种推荐方式：
- **全局调试**: 使用 `from langchain_core.globals import set_debug; set_debug(True)`。
- **自定义 Callback**: 实现 `BaseCallbackHandler` 并将其传入 `invoke(..., config={"callbacks": [...]})`。

## 4. `PromptTemplate` 里的变量缺失怎么办？
如果在调用时缺失了 `input_variables` 中定义的变量，LangChain 会抛出 `KeyError`。建议在开发阶段开启调试模式，或查看对应的 [Prompt 文档](../code_comment/libs/core/langchain_core/prompts/base.md) 确认输入要求。

## 5. 本项目支持哪些版本的 LangChain？
本项目主要针对 LangChain 1.2.7 版本进行注释。虽然大部分核心概念在 0.x 版本中也适用，但建议优先参考官方版本更新日志。
