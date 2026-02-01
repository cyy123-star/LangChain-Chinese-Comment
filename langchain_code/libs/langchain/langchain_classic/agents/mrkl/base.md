# ZeroShotAgent (MRKL)

`ZeroShotAgent` 是 LangChain 中最经典的代理实现，基于 [MRKL (Modular Reasoning, Knowledge and Language)](https://arxiv.org/pdf/2205.00445.pdf) 系统。它使用 **ReAct** (Reasoning and Acting) 框架，在执行每个操作之前都会进行推理。

> **注意**: 该代理已弃用。建议使用 `create_react_agent` (LCEL) 或更强大的 [LangGraph ReAct Agent](https://langchain-ai.github.io/langgraph/how-tos/create-react-agent/)。

## 核心机制 (ReAct)

代理遵循一个循环：**Thought (思考)** -> **Action (行动)** -> **Observation (观察)**。
- **Thought**: 代理根据当前状态推理下一步该做什么。
- **Action**: 代理决定调用哪个工具以及输入参数。
- **Observation**: 工具执行后的结果。

## 参数说明

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `llm_chain` | `LLMChain` | 负责推理的核心链。 |
| `output_parser` | `AgentOutputParser` | 解析 LLM 输出，识别 Action 或 Final Answer。默认使用 `MRKLOutputParser`。 |
| `allowed_tools` | `Sequence[str]` | 代理允许调用的工具名称列表。 |

## 提示词结构

`ZeroShotAgent` 的提示词通常包含三个部分：
1. **Prefix**: 描述助手的角色和目标。
2. **Tools**: 自动生成的工具列表及其描述。
3. **Format Instructions**: 规定 LLM 必须遵循的 `Thought/Action/Action Input/Observation` 格式。
4. **Suffix**: 包含用户的输入和 `agent_scratchpad`（用于记录之前的思考和观察）。

## 迁移指南

### 1. 使用 LCEL 替代
```python
from langchain import hub
from langchain.agents import create_react_agent
from langchain_openai import ChatOpenAI

prompt = hub.pull("hwchase17/react")
model = ChatOpenAI()
tools = [...]

agent = create_react_agent(model, tools, prompt)
```

### 2. 使用 LangGraph 替代 (推荐)
对于复杂的代理逻辑，LangGraph 提供了更好的状态管理和循环控制。
```python
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

model = ChatOpenAI()
tools = [...]
app = create_react_agent(model, tools)
```
