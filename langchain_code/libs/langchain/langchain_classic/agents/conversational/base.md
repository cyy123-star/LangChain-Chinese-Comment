# ConversationalAgent

`ConversationalAgent` 是专为对话场景设计的代理。它在标准的 ReAct 逻辑基础上增加了对对话历史（Chat History）的支持，使得代理能够记住之前的交互。

> **注意**: 该代理已弃用。建议使用 `create_react_agent` (配合包含 `MessagesPlaceholder` 的提示词) 或 LangGraph。

## 核心职责

1. **上下文感知**: 通过 `chat_history` 变量，代理可以引用用户之前提到的信息。
2. **工具调用**: 依然支持通过推理来决定何时使用工具。
3. **对话维持**: 如果不需要调用工具，代理可以直接生成对话响应。

## 关键变量

| 变量名 | 说明 |
| :--- | :--- |
| `input` | 用户当前的问题。 |
| `chat_history` | 之前的对话记录列表（通常由 Memory 组件自动注入）。 |
| `agent_scratchpad` | 代理当前的推理过程和工具执行记录。 |

## 提示词组件

- **PREFIX**: 设定代理作为一个能够进行多轮对话且拥有工具权限的 AI 助手。
- **FORMAT_INSTRUCTIONS**: 规定如何使用工具，并明确指出如果不需要工具，应该直接给出 `Final Answer`。
- **SUFFIX**: 将对话历史和当前输入组合在一起。

## 迁移指南

现代实现不再区分“对话代理”和“非对话代理”，而是通过提示词中的 `MessagesPlaceholder` 来统一处理：

```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_react_agent

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant with access to tools."),
    MessagesPlaceholder("chat_history", optional=True),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad"),
])

# 配合 AgentExecutor 使用，并配置 memory
```
