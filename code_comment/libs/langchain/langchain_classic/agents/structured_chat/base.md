# libs\langchain\langchain_classic\agents\structured_chat\base.py

此文档提供了 `libs\langchain\langchain_classic\agents\structured_chat\base.py` 文件的详细中文注释。该文件包含了创建能够处理多输入工具的结构化对话代理的逻辑。

## 1. 核心函数：`create_structured_chat_agent`

该函数构建了一个基于 LCEL 的结构化对话代理 `Runnable`。

**函数签名**:
```python
def create_structured_chat_agent(
    llm: BaseLanguageModel,
    tools: Sequence[BaseTool],
    prompt: ChatPromptTemplate,
    tools_renderer: ToolsRenderer = render_text_description_and_args,
    *,
    stop_sequence: bool | list[str] = True,
) -> Runnable
```

### 参数说明

| 参数 | 类型 | 描述 | 默认值 |
| :--- | :--- | :--- | :--- |
| `llm` | `BaseLanguageModel` | 作为代理大脑的模型。 | - |
| `tools` | `Sequence[BaseTool]` | 代理可以访问的工具。支持多参数工具。 | - |
| `prompt` | `ChatPromptTemplate` | 提示词模板。必须包含 `tools`、`tool_names` 和 `agent_scratchpad`。 | - |
| `tools_renderer` | `ToolsRenderer` | 渲染器，负责将工具及其参数 Schema 转换为字符串。 | `render_text_description_and_args` |
| `stop_sequence` | `bool \| list[str]` | 是否添加停止词。如果为 `True`，添加 `\nObservation`。 | `True` |

### 运行机制 (LCEL 链)

```python
return (
    RunnablePassthrough.assign(
        agent_scratchpad=lambda x: format_log_to_str(x["intermediate_steps"]),
    )
    | prompt
    | llm_with_stop
    | JSONAgentOutputParser()
)
```

1. **`RunnablePassthrough.assign`**: 使用 `format_log_to_str` 将中间步骤格式化为文本字符串。
2. **`prompt`**: 注入工具描述、名称以及中间步骤。
3. **`llm_with_stop`**: 调用模型，并设置停止序列以防止幻觉。
4. **`JSONAgentOutputParser`**: 从 Markdown 代码块中解析 JSON 动作。

---

## 2. 核心类：`StructuredChatAgent` (Legacy)

基于 `LLMChain` 的传统代理实现。已被标记为弃用。

### 关键方法

- **`create_prompt`**: 核心逻辑在于将工具的 `args` (参数 Schema) 进行转义（双大括号 `{{}}`）并拼接到提示词中。
- **`_construct_scratchpad`**: 在 scratchpad 前增加提示信息，强调模型只能看到最终返回的内容。
- **`_get_default_output_parser`**: 默认使用 `StructuredChatOutputParserWithRetries`，支持解析失败时的自动修复。

## 使用示例

```python
from langchain_classic.agents import create_structured_chat_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain_classic import hub

# 1. 准备多输入工具
def complex_tool(arg1: str, arg2: int):
    """一个需要两个参数的复杂工具"""
    return f"Result: {arg1} - {arg2}"

tools = [StructuredTool.from_function(complex_tool)]

# 2. 拉取标准结构化提示词
prompt = hub.pull("hwchase17/structured-chat-agent")

# 3. 创建并执行
agent = create_structured_chat_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)
agent_executor.invoke({"input": "调用复杂工具并传入 'test' 和 123"})
```

## 注意事项

- **JSON 严格性**: 模型必须输出合法的 JSON 块。如果模型输出了多个 Action（常见于 GPT-3.5-Turbo），解析器会记录警告并取第一个。
- **渲染器选择**: 必须使用能显示参数细节的渲染器（如 `render_text_description_and_args`），否则模型不知道如何填充多参数。

