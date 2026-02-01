# MRKL & ReAct Agent

MRKL (Modular Reasoning, Knowledge and Language) 系统是 LangChain 中最早实现的 Agent 模式之一，主要通过 `ZeroShotAgent` 实现。它遵循经典的 **ReAct** (Reasoning and Acting) 范式。

## 核心机制：ReAct 范式

Agent 会在执行过程中交替进行推理（Thought）和行动（Action）：
1. **Thought**: Agent 思考当前情况。
2. **Action**: Agent 决定调用哪个工具。
3. **Action Input**: Agent 提供工具所需的输入。
4. **Observation**: 工具执行后的结果。
5. 重复上述步骤，直到得出 **Final Answer**。

## 核心组件

### 1. ZeroShotAgent
这是 MRKL 系统的核心实现类。它被称为 "Zero-shot"，是因为它仅依赖于工具的名称和描述来决定如何使用它们，而不需要额外的示例。

- **Prompt**: 包含工具列表、格式说明（Thought/Action...）和用户问题。
- **OutputParser**: `MRKLOutputParser` 负责将 LLM 的文本输出解析为 `AgentAction` 或 `AgentFinish`。

## 执行逻辑 (Verbatim Snippet)

### 提示词模板 (`mrkl/prompt.py`)
```text
Question: {input}
Thought: {agent_scratchpad}
Action: 一定是工具列表中的一个 [{tool_names}]
Action Input: 工具的输入参数
Observation: 工具的执行结果
... (上述步骤循环)
Thought: 我现在知道最终答案了
Final Answer: 最终回答
```

### 创建提示词 (`ZeroShotAgent.create_prompt`)
```python
@classmethod
def create_prompt(
    cls,
    tools: Sequence[BaseTool],
    prefix: str = PREFIX,
    suffix: str = SUFFIX,
    format_instructions: str = FORMAT_INSTRUCTIONS,
    input_variables: list[str] | None = None,
) -> PromptTemplate:
    # 1. 渲染工具描述
    tool_strings = render_text_description(list(tools))
    tool_names = ", ".join([tool.name for tool in tools])
    # 2. 格式化说明
    format_instructions = format_instructions.format(tool_names=tool_names)
    # 3. 拼接最终模板
    template = f"{prefix}\n\n{tool_strings}\n\n{format_instructions}\n\n{suffix}"
    return PromptTemplate.from_template(template)
```

## 迁移指南 (LangGraph)

现代 LangChain 推荐使用 LangGraph 的 `create_react_agent` 预置函数，它更健壮且易于扩展。

### 经典方式 (initialize_agent)
```python
from langchain.agents import initialize_agent, AgentType

agent = initialize_agent(
    tools, 
    llm, 
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)
```

### 现代方式 (LangGraph)
```python
from langgraph.prebuilt import create_react_agent

# LangGraph 的 ReAct Agent 内置了对 Tool Calling 的支持
app = create_react_agent(model, tools)

# 运行
final_state = app.invoke({"messages": [("user", "Who is the CEO of LangChain?")]})
print(final_state["messages"][-1].content)
```

**为什么迁移？**
1. **结构化输出**: 现代模型原生支持 Tool Calling，不再需要解析复杂的文本格式。
2. **状态保留**: LangGraph 自动管理消息历史和中间步骤。
3. **循环控制**: 可以轻松添加最大迭代次数、审核节点等逻辑。
