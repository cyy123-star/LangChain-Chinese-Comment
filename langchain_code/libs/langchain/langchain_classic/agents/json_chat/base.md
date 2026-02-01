# JSON Chat Agent

`JSON Chat Agent`（通常对应 `create_json_chat_agent`）是一种专门为对话模型设计的代理，它要求模型以 **JSON 格式** 输出其思考和行动。这种代理特别擅长处理需要**多个输入参数**的复杂工具。

## 核心设计理念

- **强类型约束**: 通过要求 JSON 输出，可以更可靠地解析复杂的工具参数。
- **消息流**: 代理的推理过程（Scratchpad）被格式化为 AI 消息和工具消息的交替流，而不是一段纯文本。
- **对话模型友好**: 充分利用了现代对话模型对 JSON 格式的遵循能力。

## 提示词要求

该代理的提示词必须包含以下变量：
- `tools`: 工具的详细描述和参数 Schema。
- `tool_names`: 所有可用工具的名称列表。
- `agent_scratchpad`: 必须是一个 `MessagesPlaceholder`，用于存放之前的消息历史。

## 运行流程

1. **输入**: 用户问题 + 对话历史。
2. **推理**: LLM 生成一个包含 `action` 和 `action_input` 的 JSON 块。
3. **执行**: 代理执行指定的工具。
4. **反馈**: 工具结果作为一条新消息（Observation）反馈给 LLM。
5. **循环**: 直到 LLM 给出 `final_answer`。

## 示例代码

```python
from langchain_classic.agents import create_json_chat_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain import hub

model = ChatOpenAI()
tools = [...]
prompt = hub.pull("hwchase17/react-chat-json")

agent = create_json_chat_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)
```

## 迁移与对比

- **与 OpenAI Tools 相比**: JSON Agent 更通用，可以在不支持原生 Function Calling 的模型上运行。
- **与 ReAct 相比**: JSON 格式比 `Action: ...\nAction Input: ...` 这种文本标记更健壮。
- **推荐方案**: 如果模型支持，优先使用 `create_openai_tools_agent`；否则使用 `create_json_chat_agent`。
