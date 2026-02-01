# libs\langchain\langchain_classic\agents\structured_chat\__init__.py

此文档提供了 `libs\langchain\langchain_classic\agents\structured_chat\__init__.py` 文件的详细中文注释。结构化对话（Structured Chat）代理旨在支持具有多输入（Multiple Inputs）参数的工具。

## 模块概述

传统的 ReAct 代理通常只支持单个字符串输入。而结构化对话代理通过要求模型输出符合特定模式的 JSON 块，能够同时传递多个复杂的工具参数。这使得它非常适合调用 API、数据库查询或其他需要精确参数定义的任务。

### 核心入口

- **`create_structured_chat_agent`**: (推荐) 用于创建基于 LCEL 的现代结构化对话代理。
- **`StructuredChatAgent`**: (已弃用) 传统的基于 `LLMChain` 的结构化对话代理实现。

## 迁移指南

`StructuredChatAgent` 类已被标记为弃用，建议迁移到基于 LCEL 的现代实现。

| 弃用组件 | 现代替代方案 | 迁移说明 |
| :--- | :--- | :--- |
| `StructuredChatAgent` | [create_structured_chat_agent](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/structured_chat/base.md) | 使用 `create_structured_chat_agent` 配合 `ChatPromptTemplate` 和 `AgentExecutor`。 |

## 技术特性

- **多参数支持**: 能够解析复杂的 JSON 结构，并将其映射到工具的多个参数上。
- **JSON 块通信**: 强制模型在 Markdown 代码块（```json ... ```）中输出动作指令，提高了在对话模型中的稳定性。
- **自修复机制**: 配合 `StructuredChatOutputParserWithRetries`，当 JSON 解析失败时，可以尝试通过 LLM 自动修复格式。

## 关联组件

- [base.py](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/structured_chat/base.md): 包含代理的核心实现和 `create_structured_chat_agent` 函数。
- [output_parser.py](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/structured_chat/output_parser.md): 处理复杂的 JSON 解析逻辑和重试机制。
- [prompt.py](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/structured_chat/prompt.md): 定义了引导模型输出多输入 JSON 的指令模板。

