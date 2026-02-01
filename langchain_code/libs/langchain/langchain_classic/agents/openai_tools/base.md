# OpenAI Tools Agent

`OpenAI Tools Agent` 是现代 LangChain 中最常用的代理类型之一。它直接利用了 OpenAI 模型原生的 **Tool Calling**（工具调用）能力，而不是通过提示词工程去模拟 ReAct 循环。

## 核心优势

1. **准确性**: 由模型厂商在训练阶段优化的能力，比通过提示词要求的 JSON 格式更稳定。
2. **多工具调用**: 支持在单次响应中同时调用多个工具（Parallel Tool Calling）。
3. **结构化参数**: 原生支持复杂的 JSON Schema 参数。

## 工作原理

- **工具转换**: 使用 `convert_to_openai_tool` 将 LangChain 工具转换为 OpenAI 预期的 API 格式。
- **消息交互**:
  - `AIMessage`: 包含 `tool_calls` 字段，描述要调用的工具。
  - `ToolMessage`: 存储工具执行的结果，通过 `tool_call_id` 与 AI 消息关联。
- **Scratchpad**: 使用 `format_to_openai_tool_messages` 将中间步骤转换为符合 OpenAI API 规范的消息序列。

## 提示词要求

提示词中必须包含 `agent_scratchpad` 变量，且类型必须为 `MessagesPlaceholder`。

```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant"),
    MessagesPlaceholder("chat_history", optional=True),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad"),
])
```

## 迁移建议

如果你正在使用旧版的 `OPENAI_FUNCTIONS` 代理，建议尽快迁移到 `OPENAI_TOOLS`。
- **旧版**: `create_openai_functions_agent`
- **新版**: `create_openai_tools_agent`

> **注意**: 并非所有模型都支持 Tools。对于开源模型，可能需要使用 `create_tool_calling_agent`，它是 `create_openai_tools_agent` 的通用版本。
