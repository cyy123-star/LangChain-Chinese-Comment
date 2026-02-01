# LangChain Classic Agents

本目录包含了 LangChain 传统的 **Agent (代理)** 架构实现。代理是使用 LLM 作为推理引擎来决定采取哪些行动以及行动顺序的系统。

## 核心架构

所有代理都围绕以下几个核心组件构建：
- **AgentExecutor**: 负责运行代理的运行时（Runtime），处理循环逻辑、工具调用、错误处理和 Memory。
- **Agent**: 负责根据当前状态（Prompt + Scratchpad）决定下一步。
- **Tools**: 代理可以调用的功能集合。
- **Output Parser**: 将 LLM 的文本输出解析为结构化的 `AgentAction` 或 `AgentFinish`。

## 主要代理类型

| 代理类型 | 说明 | 适用模型 |
| :--- | :--- | :--- |
| [ZeroShot (MRKL)](./mrkl/base.md) | 最基础的 ReAct 代理。 | 几乎所有 LLM |
| [Chat Agent](./chat/base.md) | 针对对话模型优化的 ReAct 代理。 | Chat Models |
| [Conversational](./conversational/base.md) | 增加对话历史支持的代理。 | Chat Models |
| [OpenAI Tools](./openai_tools/base.md) | 使用 OpenAI 原生工具调用能力。 | OpenAI Models |
| [JSON Chat](./json_chat/base.md) | 使用 JSON 格式进行多输入工具调用。 | 遵循 JSON 好的模型 |
| [XML Agent](./xml/base.md) | 使用 XML 标签进行推理和行动。 | Claude 等特定模型 |
| [ReAct Docstore](./react/base.md) | 专门用于文档库检索的代理。 | 几乎所有 LLM |

## 辅助功能

- [Agent Types](./agent_types.py): 定义了所有支持的代理枚举类型。
- [Initialize](./initialize.py): 提供了便捷的代理初始化函数 `initialize_agent`（已弃用）。
- [Load Tools](./load_tools.py): 预置了大量常用的社区工具（如 Google Search, Wikipedia）。

## 弃用与迁移指南

Classic Agents 的 `AgentExecutor` 正在逐渐被 **LangGraph** 所取代。

| 弃用组件 | 现代替代方案 |
| :--- | :--- |
| `initialize_agent` | `create_react_agent`, `create_openai_tools_agent` 等 |
| `AgentExecutor` | [LangGraph ReAct Agent](https://langchain-ai.github.io/langgraph/how-tos/create-react-agent/) |
| `StructuredChatAgent` | `create_structured_chat_agent` |

### 为什么选择 LangGraph？
1. **控制力**: 可以精细控制循环逻辑，而不是被动等待 `AgentExecutor` 的默认行为。
2. **状态管理**: 支持复杂的持久化状态和检查点（Checkpoints）。
3. **多代理协作**: 原生支持多个代理之间的交互。

## 设计哲学

Classic Agents 旨在提供一种“开箱即用”的自主性。虽然配置简单，但随着任务复杂度的增加，调试和定制 `AgentExecutor` 会变得非常困难。这也是为什么 LangChain 转向了更具显式控制权的 LangGraph。
