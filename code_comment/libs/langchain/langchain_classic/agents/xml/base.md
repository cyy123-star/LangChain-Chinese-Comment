# libs\langchain\langchain_classic\agents\xml\base.py

此文档提供了 `libs\langchain\langchain_classic\agents\xml\base.py` 文件的详细中文注释。该文件包含了创建 XML 代理的核心逻辑 and 工厂函数。

## 1. 核心函数：`create_xml_agent`

该函数构建了一个基于 LCEL (LangChain Expression Language) 的 XML 代理 `Runnable`。

**函数签名**:
```python
def create_xml_agent(
    llm: BaseLanguageModel,
    tools: Sequence[BaseTool],
    prompt: BasePromptTemplate,
    tools_renderer: ToolsRenderer = render_text_description,
    *,
    stop_sequence: bool | list[str] = True,
) -> Runnable
```

### 参数说明

| 参数 | 类型 | 描述 | 默认值 |
| :--- | :--- | :--- | :--- |
| `llm` | `BaseLanguageModel` | 作为代理大脑的模型。 | - |
| `tools` | `Sequence[BaseTool]` | 代理可以访问的工具。 | - |
| `prompt` | `BasePromptTemplate` | 提示词模板。必须包含 `tools` 和 `agent_scratchpad` 变量。 | - |
| `tools_renderer` | `ToolsRenderer` | 控制如何将工具列表转换为字符串。 | `render_text_description` |
| `stop_sequence` | `bool \| list[str]` | 是否添加停止词。如果为 `True`，添加 `</tool_input>`。 | `True` |

### 运行机制 (LCEL 链)

```python
return (
    RunnablePassthrough.assign(
        agent_scratchpad=lambda x: format_xml(x["intermediate_steps"]),
    )
    | prompt
    | llm_with_stop
    | XMLAgentOutputParser()
)
```

1. **`RunnablePassthrough.assign`**: 将 `intermediate_steps`（中间步骤）通过 `format_xml` 格式化为 XML 字符串，并赋值给 `agent_scratchpad`。
2. **`prompt`**: 填充模板，注入工具描述和中间步骤。
3. **`llm_with_stop`**: 调用模型，并根据 `stop_sequence` 设置停止词。
4. **`XMLAgentOutputParser`**: 解析 XML 标签，返回 `AgentAction` 或 `AgentFinish`。

---

## 2. 核心类：`XMLAgent` (Legacy)

基于 `LLMChain` 的传统代理实现。已被标记为弃用。

### 关键方法

- **`plan`**: 核心执行逻辑。它手动拼接 `<tool>`、`<tool_input>` 和 `<observation>` 标签，构建 `intermediate_steps` 字符串。
- **`get_default_prompt`**: 返回基于 `agent_instructions` 的默认 `ChatPromptTemplate`。
- **`get_default_output_parser`**: 默认使用 `XMLAgentOutputParser`。

## 使用示例

```python
from langchain_classic.agents import create_xml_agent, AgentExecutor
from langchain_anthropic import ChatAnthropic
from langchain_classic import hub

# 1. 初始化模型和工具
llm = ChatAnthropic(model="claude-3-opus-20240229")
tools = [...] # 定义你的工具

# 2. 拉取提示词
prompt = hub.pull("hwchase17/xml-agent-convo")

# 3. 创建代理并运行
agent = create_xml_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)
agent_executor.invoke({"input": "帮我查询天气"})
```

## 注意事项

- **中间步骤格式**: XML 代理的 `agent_scratchpad` 使用特定的 XML 结构，不同于 ReAct 代理的文本日志。
- **停止词策略**: `</tool_input>` 停止词至关重要。它能确保模型在请求工具输入后停止，等待代理执行工具并返回 `<observation>`。
