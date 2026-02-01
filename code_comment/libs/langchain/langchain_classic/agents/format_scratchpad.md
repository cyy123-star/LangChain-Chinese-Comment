# Agent Scratchpad Formatting (中间步骤格式化)

在 Agent 执行过程中，LLM 需要了解之前的思考过程和工具执行结果。`format_scratchpad` 模块包含了一系列工具函数，负责将 `intermediate_steps`（即 `(AgentAction, Observation)` 元组列表）转换为模型可理解的文本或消息列表。

## 常见格式化策略

不同的 Agent 类型（如 ReAct, OpenAI Functions, XML 等）需要不同格式的 Scratchpad。

### 1. 文本格式化 (format_log_to_str)
适用于标准的 ReAct 风格 Agent（如 `ZeroShotAgent`）。

#### 核心逻辑 (Verbatim Snippet)
```python
def format_log_to_str(
    intermediate_steps: list[tuple[AgentAction, str]],
    observation_prefix: str = "Observation: ",
    llm_prefix: str = "Thought: ",
) -> str:
    thoughts = ""
    for action, observation in intermediate_steps:
        # 将之前的 Action 日志拼接到 Thought 中
        thoughts += action.log
        # 拼接观察结果
        thoughts += f"\n{observation_prefix}{observation}\n{llm_prefix}"
    return thoughts
```

### 2. 消息格式化 (format_to_openai_function_messages)
适用于使用 OpenAI 函数调用的 Agent。它不生成单一字符串，而是生成一系列 `AIMessage` 和 `FunctionMessage`。

#### 核心逻辑 (Verbatim Snippet)
```python
def _create_function_message(
    agent_action: AgentAction,
    observation: Any,
) -> FunctionMessage:
    # 将工具执行结果转换为 FunctionMessage
    if not isinstance(observation, str):
        content = json.dumps(observation, ensure_ascii=False)
    else:
        content = observation
    return FunctionMessage(
        name=agent_action.tool,
        content=content,
    )
```

### 3. XML 格式化 (format_xml)
适用于需要 XML 标签结构的 Agent（如 Anthropic 模型）。

#### 核心逻辑 (Verbatim Snippet)
```python
def format_xml(
    intermediate_steps: list[tuple[AgentAction, str]],
    *,
    escape_format: Literal["minimal"] | None = "minimal",
) -> str:
    log = ""
    for action, observation in intermediate_steps:
        # 拼接 XML 标签
        log += (
            f"<tool>{tool}</tool><tool_input>{tool_input}"
            f"</tool_input><observation>{observation_}</observation>"
        )
    return log
```

## 格式化函数列表

| 函数名 | 适用 Agent 类型 | 输出类型 |
| :--- | :--- | :--- |
| `format_log_to_str` | ReAct / ZeroShot | `str` |
| `format_to_openai_function_messages` | OpenAI Functions | `List[BaseMessage]` |
| `format_to_openai_tool_messages` | OpenAI Tools | `List[BaseMessage]` |
| `format_xml` | XML Agent | `str` |
| `format_log_to_messages` | Chat Agents | `List[BaseMessage]` |

## 迁移到现代方案 (LCEL)

在 LCEL 中，这些格式化逻辑通常直接嵌入在 `Runnable` 管道中，作为数据转换的一步。

### 示例：LCEL 中的格式化
```python
from langchain_core.runnables import RunnablePassthrough
from langchain.agents.format_scratchpad import format_to_openai_function_messages

agent = (
    RunnablePassthrough.assign(
        agent_scratchpad=lambda x: format_to_openai_function_messages(
            x["intermediate_steps"]
        )
    )
    | prompt
    | llm
    | output_parser
)
```

**为什么迁移？**
1. **显式控制**: 用户可以轻松修改格式化逻辑，而不必继承复杂的 Agent 类。
2. **组合性**: 格式化函数可以作为普通 Python 函数在任何地方使用。
