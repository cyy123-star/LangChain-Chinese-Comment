# Structured Chat Agent (结构化对话代理)

`StructuredChatAgent` 是为了解决 `ZeroShotAgent` 只能处理单字符串输入工具的局限性而设计的。它允许 Agent 调用具有多个复杂参数（由 JSON Schema 定义）的工具。

## 核心特性

- **多参数支持**: 可以调用复杂的工具，例如 `tool.run({"param1": "val1", "param2": "val2"})`。
- **JSON 交互**: Agent 通过输出一个符合特定格式的 JSON 代码块来指定动作和参数。

## 核心机制 (Verbatim Snippet)

### 1. 停止符设置
为了防止模型生成多余内容，通常会设置 `Observation:` 作为停止符。
```python
@property
@override
def _stop(self) -> list[str]:
    return ["Observation:"]
```

### 2. Scratchpad 处理
它会在历史步骤前加上一段提示语，明确告知模型这是之前的思考过程。
```python
def _construct_scratchpad(
    self,
    intermediate_steps: list[tuple[AgentAction, str]],
) -> str:
    agent_scratchpad = super()._construct_scratchpad(intermediate_steps)
    if agent_scratchpad:
        return (
            f"This was your previous work "
            f"(but I haven't seen any of it! I only see what "
            f"you return as final answer):\n{agent_scratchpad}"
        )
    return agent_scratchpad
```

## 迁移指南 (Migration)

现代模型（GPT-4, Claude 3, Gemini）原生支持 **Tool Calling**，这比依赖 Prompt 解析 JSON 的 `StructuredChatAgent` 更加可靠。

### 现代替代方案：Tool Calling Agent
```python
from langchain.agents import create_tool_calling_agent
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4-turbo")
agent = create_tool_calling_agent(llm, tools, prompt)
```

**为什么迁移？**
1. **更低的出错率**: 现代模型经过专门训练，可以生成高度准确的工具参数，不再需要复杂的 Regex 或 JSON 解析。
2. **支持并行调用**: Tool Calling Agent 可以单次返回多个工具调用请求。
