# libs\langchain\langchain_classic\agents\xml\__init__.py

此文档提供了 `libs\langchain\langchain_classic\agents\xml\__init__.py` 文件的详细中文注释。该模块实现了基于 XML 标签的代理架构，常用于对 XML 格式支持较好的模型（如 Anthropic Claude 系列）。

## 模块概述

XML 代理是一种结构化思考的代理模式。与传统的 ReAct 模式（使用 Thought/Action 文本标签）不同，它使用标准的 XML 标签（如 `<tool>`、`<tool_input>`、`<final_answer>`）来封装思考和行动逻辑。

### 核心入口

- **`create_xml_agent`**: (推荐) 用于创建基于 LCEL 的现代 XML 代理。
- **`XMLAgent`**: (已弃用) 传统的基于 `LLMChain` 的 XML 代理实现。

## 迁移指南

`XMLAgent` 类已被标记为弃用，建议迁移到基于 LCEL 的现代实现。

| 弃用组件 | 现代替代方案 | 迁移说明 |
| :--- | :--- | :--- |
| `XMLAgent` | [create_xml_agent](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/xml/base.md) | 使用 `create_xml_agent` 配合 `ChatPromptTemplate` 和 `AgentExecutor`。 |

## 技术特性

- **标签化通信**: 强制模型输出结构化的 XML，这大大降低了解析失败的概率。
- **停止序列 (Stop Sequences)**: 默认将 `</tool_input>` 作为停止序列，防止模型在未获得工具结果前继续预测。
- **跨平台兼容**: 虽然最初为 Anthropic 模型优化，但许多现代大模型（如 GPT-4, Llama 3）也能很好地遵循 XML 标签指令。

## 关联组件

- [base.py](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/xml/base.md): 包含代理的核心实现逻辑。
- [prompt.py](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/xml/prompt.md): 定义了默认的 XML 指令模板。

