# libs\langchain\langchain_classic\agents\mrkl\__init__.py

此文档提供了 `libs\langchain\langchain_classic\agents\mrkl\__init__.py` 文件的详细中文注释。该模块实现了 MRKL (Modular Reasoning, Knowledge and Language) 系统，即经典的 **Zero Shot ReAct** 代理。

## 功能描述

MRKL 模块是 LangChain 中最早也是最著名的代理实现之一。它遵循 ReAct (Reasoning and Acting) 框架，使语言模型能够结合思维链（Chain of Thought）和外部工具的使用来回答问题。

## 核心组件

- **ZeroShotAgent**: 核心代理类，通过分析工具描述来决定下一步行动。
- **MRKLChain**: `AgentExecutor` 的一个封装，用于运行 MRKL 系统。
- **MRKLOutputParser**: 负责解析模型生成的“思考-行动-输入”序列。

## 技术特点

- **零样本学习 (Zero-Shot)**: 代理仅依靠工具的文本描述来学习如何使用它们，无需额外的示例。
- **ReAct 循环**: 严格遵循 `Thought -> Action -> Action Input -> Observation` 的迭代循环。
- **通用性强**: 适用于任何具有基本逻辑推理能力的 LLM，是理解 LangChain 代理机制的基石。

## 关联文件

- [base.py](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/mrkl/base.md): 包含 `ZeroShotAgent` 和 `MRKLChain` 的核心实现。
- [output_parser.py](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/mrkl/output_parser.md): 详细介绍了 ReAct 格式的解析逻辑。
- [prompt.py](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/mrkl/prompt.md): 定义了经典的 ReAct 提示词模板。

