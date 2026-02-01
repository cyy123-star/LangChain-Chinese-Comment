# Agent Output Parsers (代理输出解析器)

代理输出解析器负责将大语言模型 (LLM) 的原始输出字符串或消息转换为结构化的指令：`AgentAction`（执行工具）或 `AgentFinish`（结束执行）。

## 核心组件

### 1. ReActSingleInputOutputParser
解析典型的 ReAct 风格（Thought/Action/Action Input）输出，适用于单输入工具。

#### 解析逻辑 (Verbatim Snippet)
```python
def parse(self, text: str) -> AgentAction | AgentFinish:
    includes_answer = FINAL_ANSWER_ACTION in text
    regex = (
        r"Action\s*\d*\s*:[\s]*(.*?)[\s]*Action\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)"
    )
    action_match = re.search(regex, text, re.DOTALL)
    if action_match:
        if includes_answer:
            msg = f"{FINAL_ANSWER_AND_PARSABLE_ACTION_ERROR_MESSAGE}: {text}"
            raise OutputParserException(msg)
        action = action_match.group(1).strip()
        action_input = action_match.group(2)
        tool_input = action_input.strip(" ")
        tool_input = tool_input.strip('"')

        return AgentAction(action, tool_input, text)

    if includes_answer:
        return AgentFinish(
            {"output": text.split(FINAL_ANSWER_ACTION)[-1].strip()},
            text,
        )
```

### 2. OpenAIFunctionsAgentOutputParser
解析 OpenAI 函数调用（Function Calling）生成的 `AIMessage`。

#### 解析逻辑 (Verbatim Snippet)
```python
@staticmethod
def parse_ai_message(message: BaseMessage) -> AgentAction | AgentFinish:
    if not isinstance(message, AIMessage):
        msg = f"Expected an AI message got {type(message)}"
        raise TypeError(msg)

    function_call = message.additional_kwargs.get("function_call", {})

    if function_call:
        function_name = function_call["name"]
        try:
            if len(function_call["arguments"].strip()) == 0:
                _tool_input = {}
            else:
                _tool_input = json.loads(function_call["arguments"], strict=False)
        except JSONDecodeError as e:
            msg = f"Could not parse tool input: {function_call} because the `arguments` is not valid JSON."
            raise OutputParserException(msg) from e

        # 处理旧版单字符串参数的特殊 key `__arg1`
        if "__arg1" in _tool_input:
            tool_input = _tool_input["__arg1"]
        else:
            tool_input = _tool_input

        return AgentActionMessageLog(
            tool=function_name,
            tool_input=tool_input,
            log=log,
            message_log=[message],
        )

    return AgentFinish(
        return_values={"output": message.content},
        log=str(message.content),
    )
```

### 3. XMLAgentOutputParser
解析带有 XML 标签的输出（常见于 Anthropic 模型），例如 `<tool>search</tool><tool_input>weather</tool_input>`。

### 4. JSONAgentOutputParser
解析包含 JSON 代码块的输出，通常用于支持复杂多参数输入的 Agent（如 `ChatAgent`）。

## 常见解析器列表

| 解析器名称 | 适用场景 | 关键特征 |
| :--- | :--- | :--- |
| `ReActSingleInputOutputParser` | 文本补全/对话模型 (ReAct) | 解析 `Action:` 和 `Action Input:` |
| `OpenAIFunctionsAgentOutputParser` | OpenAI 函数调用 | 解析 `additional_kwargs["function_call"]` |
| `ToolsAgentOutputParser` | 通用工具调用 (Tool Calling) | 解析 `message.tool_calls` (现代标准) |
| `XMLAgentOutputParser` | XML 格式输出 | 解析 `<tool>` 标签内容 |
| `SelfAskOutputParser` | Self-Ask 策略 | 解析 `Follow up:` 和 `Intermediate answer:` |

## 迁移指南 (Migration to LangGraph/LCEL)

在现代 LangChain 中，解析器通常直接集成在 `Runnable` 链中，或者由 `bind_tools` 自动处理。

### LCEL 风格迁移
以前手动指定解析器，现在通过管道符 `|` 连接：

```python
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI

# 以前
# agent = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools)

# 现在 (LCEL)
prompt = ChatPromptTemplate.from_messages([...])
model = ChatOpenAI().bind_tools(tools)
output_parser = ToolsAgentOutputParser() # 或使用新的工具解析器

chain = prompt | model | output_parser
```

### LangGraph 迁移
在 LangGraph 中，解析逻辑通常发生在 `call_model` 节点中，解析结果直接决定下一个图节点的流向。

```python
def call_model(state):
    messages = state["messages"]
    response = model.invoke(messages)
    # response 包含 tool_calls，由后续的 tools 节点处理
    return {"messages": [response]}
```
