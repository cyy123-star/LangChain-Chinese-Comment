# libs\langchain\langchain_classic\agents\react\__init__.py

此文档提供了 `libs\langchain\langchain_classic\agents\react\__init__.py` 文件的详细中文注释。ReAct 模块实现了基于 "Reasoning and Acting" 论文（Synergizing Reasoning and Acting in Language Models）的代理架构。

## 模块概述

ReAct 是一种经典的代理设计模式，它要求模型在执行每一步行动之前先进行“思考”（Thought）。这种循环（Thought -> Action -> Observation）使得模型能够更好地处理复杂任务并减少幻觉。

### 核心入口

- **`create_react_agent`**: (推荐) 用于创建基于 LCEL 的 ReAct 代理。
- **`ReActChain`**: (已弃用) 传统的 ReAct 实现，主要用于 Docstore 探索。

## 弃用说明与迁移指南

!!! warning "弃用警告"
    此目录下的许多类（如 `ReActChain`, `ReActDocstoreAgent`）已被标记为弃用。

### 迁移建议

1. **从 `ReActChain` 迁移**:
   - 现代推荐做法是使用 `create_react_agent` 工厂函数配合 `AgentExecutor`。
   - 对于更高级的生产环境应用，强烈建议使用 **LangGraph** 的 `create_react_agent`。

2. **从 legacy 提示词迁移**:
   - 现代版本通常从 `langchain_classic.hub` 拉取经过验证的提示词（如 `hwchase17/react`）。

## 技术特性

- **结构化思维**: 强制模型输出 `Thought:` 字段。
- **停止序列 (Stop Sequences)**: 默认使用 `\nObservation:` 作为停止词，防止模型自我模拟工具的返回结果。
- **单输入限制**: 大多数经典的 ReAct 解析器（如 `ReActSingleInputOutputParser`）设计为仅接受单个字符串作为工具输入。

## 关联组件

- [agent.py](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/react/agent.md): `create_react_agent` 的具体实现。
- [output_parser.py](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/react/output_parser.md): 处理模型输出的逻辑。
- [wiki_prompt.py](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/react/wiki_prompt.md): 经典的维基百科探索提示词。

