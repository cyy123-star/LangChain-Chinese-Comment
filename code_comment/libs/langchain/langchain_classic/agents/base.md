# 代理基础模块 (Agents Base)

`agents` 模块是 LangChain 中实现“代理”模式的核心。代理不遵循预定义的调用序列（如 Chain），而是利用大语言模型（LLM）作为推理引擎，根据任务需求动态决定调用哪些工具（Tools）以及调用的顺序。

> **注意**：LangChain 官方已将传统的代理实现标记为过时（Deprecated），建议在新项目中使用 **LangGraph** 或 **LCEL** 构建代理。

## 核心类

### 1. BaseSingleActionAgent (单步操作代理基类)

这是所有返回单个操作（AgentAction）或结束（AgentFinish）的代理的抽象基类。

#### 核心方法：
- `plan(intermediate_steps, callbacks, **kwargs)`: 根据历史步骤和当前输入决定下一步。
    - `intermediate_steps`: 包含之前执行的操作及其观察结果（Observation）的列表。
    - 返回：`AgentAction`（执行工具）或 `AgentFinish`（返回最终答案）。
- `aplan(...)`: `plan` 方法的异步版本。

### 2. BaseMultiActionAgent (多步操作代理基类)

与单步代理类似，但允许在一步中返回多个操作（例如同时并行调用多个工具）。

### 3. AgentExecutor (代理执行器)

`AgentExecutor` 是代理的运行时环境。它负责循环调用代理的 `plan` 方法，执行选定的工具，获取观察结果，并将其反馈给代理，直到代理返回 `AgentFinish`。

#### 核心参数：
- `agent`: 具体的代理对象（如 `ZeroShotAgent` 或 `RunnableAgent`）。
- `tools`: 代理可以使用的工具列表。
- `max_iterations`: 最大迭代次数，防止无限循环（默认 15）。
- `early_stopping_method`: 达到最大迭代次数时的停止策略（`force` 直接返回，`generate` 尝试生成最终答案）。
- `handle_parsing_errors`: 是否处理输出解析错误。如果为 `True`，解析错误将作为观察结果传回给 LLM。

### 4. RunnableAgent (Runnable 驱动的代理)

现代 LangChain 中推荐的代理包装方式，它允许将任何 `Runnable` 对象（通常是 LCEL 链）包装成代理。

---

## 辅助功能

### 1. initialize_agent (初始化代理 - 已过时)

这是一个便捷函数，用于根据给定的工具、LLM 和代理类型快速创建 `AgentExecutor`。

### 2. AgentType (代理类型枚举)

定义了 LangChain 支持的经典代理类型：
- `ZERO_SHOT_REACT_DESCRIPTION`: 经典的 ReAct 代理，根据工具描述决定使用哪个工具。
- `CHAT_CONVERSATIONAL_REACT_DESCRIPTION`: 专门为聊天模型优化的对话代理。
- `STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION`: 能够调用具有多个输入参数的复杂工具。
- `OPENAI_FUNCTIONS`: 利用 OpenAI 函数调用功能的专用代理。

---

## 代码示例

### 使用 AgentExecutor 和 RunnableAgent (推荐用法)

```python
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool

# 1. 定义工具
@tool
def get_weather(city: str) -> str:
    """获取指定城市的当前天气。"""
    return f"{city} 的天气是晴天，25度。"

tools = [get_weather]

# 2. 定义 Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个有用的助手。"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

# 3. 创建代理
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
agent = create_openai_functions_agent(llm, tools, prompt)

# 4. 创建执行器
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 5. 运行
response = agent_executor.invoke({"input": "北京天气怎么样？"})
print(response["output"])
```

### 使用 initialize_agent (经典用法)

```python
from langchain.agents import initialize_agent, AgentType
from langchain_openai import OpenAI

llm = OpenAI(temperature=0)
# initialize_agent 内部会自动创建 AgentExecutor
agent_executor = initialize_agent(
    tools, 
    llm, 
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
    verbose=True
)

res = agent_executor.run("北京天气怎么样？")
```

## 注意事项
1. **记忆（Memory）**：在 `AgentExecutor` 中使用记忆时，通常需要将 `memory` 对象传递给执行器，而不是代理本身。
2. **中间步骤**：如果需要查看代理的推理过程，可以将 `return_intermediate_steps` 设置为 `True`。
3. **解析错误**：在生产环境中，强烈建议设置 `handle_parsing_errors=True`，以增强代理的鲁棒性。
