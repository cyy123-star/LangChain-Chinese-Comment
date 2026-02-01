# libs\langchain\langchain_classic\agents\output_parsers\__init__.py

此文档提供了 `libs\langchain\langchain_classic\agents\output_parsers\__init__.py` 文件的详细中文注释。该模块是代理输出解析器的入口，负责将模型的文本输出转化为结构化的指令。

## 模块概述

输出解析器（Output Parsers）是代理决策循环的关键组件。它们的作用是将 LLM 生成的原始字符串解析为以下两种对象之一：

1. **`AgentAction`**: 表示代理决定采取某个行动。包含工具名称、输入参数以及思维日志。
2. **`AgentFinish`**: 表示代理决定结束任务并给出最终回答。包含返回结果字典和思维日志。

## 导出的解析器类

该模块统一导出了以下常用的解析器：

- **`JSONAgentOutputParser`**: 解析标准 JSON 格式的指令。
- **`OpenAIFunctionsAgentOutputParser`**: 解析 OpenAI 旧版 Function Calling 输出。
- **`ReActJsonSingleInputOutputParser`**: 解析结合了思维链与 JSON 代码块的输出。
- **`ReActSingleInputOutputParser`**: 解析经典的 ReAct 文本格式（Thought/Action/Action Input）。
- **`SelfAskOutputParser`**: 解析 Self-Ask 模式下的追问或最终答案。
- **`ToolsAgentOutputParser`**: 解析现代的多工具调用（Tool Calling）输出。
- **`XMLAgentOutputParser`**: 解析 XML 标签格式的指令（常用于 Claude）。

## 设计哲学

LangChain 的输出解析器设计遵循“健壮性原则”：对输入尽可能宽容（例如自动处理 JSON 代码块前后的杂乱文本），而对输出则保持严格的结构化，确保下游的 `AgentExecutor` 能够稳定执行。
