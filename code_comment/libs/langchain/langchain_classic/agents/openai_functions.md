# OpenAI Functions Agent

`OpenAIFunctionsAgent` 是一种专门为支持 **Function Calling**（函数调用）能力的模型（如 OpenAI GPT-4）设计的 Agent。与依赖 Prompt 解析的 ReAct Agent 不同，它直接利用模型的 API 能力来决定调用哪个工具。

## 核心机制：Function Calling

该 Agent 不再通过 "Thought/Action" 的文本解析来工作，而是：
1. **定义函数**: 将工具（Tools）转换为 JSON Schema 格式的函数定义。
2. **发送请求**: 将用户输入和函数定义发送给模型。
3. **模型响应**: 模型直接返回一个结构化的函数调用请求（Function Call），包括函数名和参数。
4. **执行与反馈**: 执行对应工具，并将结果作为 "Function Message" 反馈给模型。

## 核心组件

### 1. OpenAIFunctionsAgent
经典实现类，封装了与 OpenAI 函数调用接口交互的逻辑。
- **functions**: 动态生成的函数定义列表。
- **agent_scratchpad**: 使用 `MessagesPlaceholder` 存储中间步骤，并转换为 OpenAI 特有的消息格式。

### 2. create_openai_functions_agent
基于 LCEL 的现代工厂函数。它构建了一个 Runnable 序列，内部使用 `llm.bind` 来绑定函数。

## 执行逻辑 (Verbatim Snippet)

### 格式化中间步骤 (`format_to_openai_function_messages`)
Agent 需要将之前的行动和观察结果转换为模型理解的消息历史：
```python
def format_to_openai_function_messages(
    intermediate_steps: list[tuple[AgentAction, str]],
) -> list[BaseMessage]:
    messages = []
    for action, observation in intermediate_steps:
        # 将 AgentAction 转换为 AIMessage (含 function_call)
        messages.append(AIMessage(content="", additional_kwargs={"function_call": ...}))
        # 将观察结果转换为 FunctionMessage
        messages.append(FunctionMessage(name=action.tool, content=observation))
    return messages
```

### LCEL 构造逻辑 (`create_openai_functions_agent`)
```python
llm_with_tools = llm.bind(functions=[convert_to_openai_function(t) for t in tools])

agent = (
    RunnablePassthrough.assign(
        agent_scratchpad=lambda x: format_to_openai_function_messages(
            x["intermediate_steps"],
        ),
    )
    | prompt
    | llm_with_tools
    | OpenAIFunctionsAgentOutputParser()
)
```

## 迁移指南 (Tool Calling)

虽然 OpenAI Functions Agent 已经很高效，但现代 LangChain 推荐使用更通用的 **Tool Calling Agent**，它可以同时支持 OpenAI、Anthropic 和 Google 等多种模型。

### 经典方式 (initialize_agent)
```python
agent = initialize_agent(
    tools, 
    llm, 
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True
)
```

### 现代方式 (create_tool_calling_agent)
```python
from langchain.agents import create_tool_calling_agent
from langchain import hub

prompt = hub.pull("hwchase17/openai-tools-agent")
# 这里的 model 可以是任何支持 Tool Calling 的模型
agent = create_tool_calling_agent(model, tools, prompt)

# 配合 AgentExecutor 使用
from langchain.agents import AgentExecutor
agent_executor = AgentExecutor(agent=agent, tools=tools)
```

**为什么迁移？**
1. **跨模型支持**: 同样的逻辑可以运行在 Claude 或 Gemini 上。
2. **多工具调用**: 支持模型在单次响应中请求调用多个工具（Parallel Tool Calling）。
3. **标准化**: 使用 `tools` 而不是 `functions`，符合最新的行业标准。
