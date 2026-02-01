# agents.py - Agent 架构定义

- **最后更新时间**: 2026-01-29
- **对应源码版本**: LangChain Core v1.2.7

## 文件概述

`agents.py` 定义了 LangChain 中 Agent 相关的核心架构和数据模型。它包含了代表 Agent 动作（Action）、观察结果（Observation）和最终结果（Finish）的类。

> **警告**: 该文件中的架构定义主要用于向后兼容。对于新的 Agent 开发，建议使用 `langchain` 库中的相关组件。

## 导入依赖

| 模块 | 作用 |
| :--- | :--- |
| `langchain_core.load.serializable.Serializable` | 使 Agent 相关对象支持序列化。 |
| `langchain_core.messages` | 包含 `AIMessage`, `HumanMessage`, `FunctionMessage` 等消息类型，用于在 Agent 执行过程中转换状态。 |

## 类与函数详解

### 1. AgentAction
- **功能描述**: 代表 Agent 请求执行的一个具体动作。它包含要执行的工具名称及其输入参数。
- **参数说明**:
  | 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
  | :--- | :--- | :--- | :--- | :--- |
  | `tool` | `str` | - | 是 | 要执行的工具（Tool）的名称。 |
  | `tool_input` | `str | dict` | - | 是 | 传递给工具的输入参数。 |
  | `log` | `str` | - | 是 | 关于该动作的额外日志信息（通常是 LLM 的原始预测文本）。 |

### 2. AgentActionMessageLog (继承自 AgentAction)
- **功能描述**: 与 `AgentAction` 类似，但额外包含了一个消息日志（`message_log`）。这在与 `ChatModels` 配合使用时非常有用，可以完整保留对话历史。

### 3. AgentStep
- **功能描述**: 代表执行一个 `AgentAction` 后得到的结果，包含原始动作和对应的观察结果（Observation）。

### 4. AgentFinish
- **功能描述**: 代表 Agent 的最终返回结果。当 Agent 达到停止条件（如找到答案）时返回此类。
- **参数说明**:
  | 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
  | :--- | :--- | :--- | :--- | :--- |
  | `return_values` | `dict` | - | 是 | 包含最终结果的字典。 |
  | `log` | `str` | - | 是 | 关于最终结果的日志或 LLM 的原始预测。 |

## 核心逻辑

Agent 的基本工作流程如下：
1. **预测动作**: 根据 Prompt，Agent 使用 LLM 预测下一步要采取的动作（`AgentAction`）。
2. **执行并观察**: 执行该动作（调用工具），获得观察结果（Observation）。
3. **循环**: 将观察结果返回给 LLM，重复步骤 1。
4. **完成**: 当 LLM 决定不再需要执行动作时，返回 `AgentFinish`。

## 相关链接
- [langchain.agents.agent](https://docs.langchain.com/oss/python/langchain/agents) (推荐的新版 Agent 实现)
- [langchain_core.messages](file:///d%3A/TraeProjects/langchain_code_comment/code_comment/libs/core/langchain_core/messages/base.md)
