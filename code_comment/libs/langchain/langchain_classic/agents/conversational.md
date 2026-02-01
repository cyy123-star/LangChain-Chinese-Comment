# Conversational Agent

`ConversationalAgent` 是专为对话场景设计的 Agent。它在 ReAct 范式的基础上，通过引入 `chat_history`（对话历史）来保持上下文连贯性。

## 核心功能

与标准的 `ZeroShotAgent` 不同，`ConversationalAgent` 的提示词模板包含一个专门用于存储历史对话的变量。这使得 Agent 能够记住之前的交互，而不仅仅是处理单一的请求。

- **chat_history**: 存储 Human 和 AI 之间之前的对话内容。
- **ai_prefix / human_prefix**: 用于在 Prompt 中标识不同说话者的前缀（默认为 "AI" 和 "Human"）。

## 执行逻辑 (Verbatim Snippet)

### 提示词结构 (`ConversationalAgent.create_prompt`)
```python
@classmethod
def create_prompt(
    cls,
    tools: Sequence[BaseTool],
    prefix: str = PREFIX,
    suffix: str = SUFFIX,
    format_instructions: str = FORMAT_INSTRUCTIONS,
    ai_prefix: str = "AI",
    human_prefix: str = "Human",
    input_variables: list[str] | None = None,
) -> PromptTemplate:
    # 1. 渲染工具描述
    tool_strings = "\n".join(
        [f"> {tool.name}: {tool.description}" for tool in tools],
    )
    # 2. 注入对话相关的变量名
    if input_variables is None:
        input_variables = ["input", "chat_history", "agent_scratchpad"]
    
    # 3. 构造模板
    template = f"{prefix}\n\n{tool_strings}\n\n{format_instructions}\n\n{suffix}"
    return PromptTemplate(template=template, input_variables=input_variables)
```

### 提示词模板内容
```text
{prefix}
{tool_strings}
{format_instructions}

{chat_history}
Human: {input}
Thought: {agent_scratchpad}
```

## 迁移指南 (LangGraph)

在现代 LangChain 中，对话能力通常由 LangGraph 的 **State**（状态）管理，而不是硬编码在 Prompt 模板中。

### 经典方式 (initialize_agent)
```python
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType

memory = ConversationBufferMemory(memory_key="chat_history")
agent = initialize_agent(
    tools, 
    llm, 
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True
)
```

### 现代方式 (LangGraph)
```python
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

# 使用内存检查点来自动保存对话历史
memory = MemorySaver()
app = create_react_agent(model, tools, checkpointer=memory)

# 运行时提供 thread_id 以识别不同会话
config = {"configurable": {"thread_id": "user-123"}}
app.invoke({"messages": [("user", "My name is Bob")]}, config)
app.invoke({"messages": [("user", "What is my name?")]}, config)
```

**为什么迁移？**
1. **多端持久化**: LangGraph 的检查点机制支持将对话历史保存到外部数据库（如 Redis, Postgres）。
2. **状态剪裁**: 现代方案更容易实现历史消息的总结或窗口裁剪，防止 Token 溢出。
3. **更自然的对话**: 基于消息列表（List of Messages）而非单一字符串拼接，更符合 Chat 模型的交互习惯。
