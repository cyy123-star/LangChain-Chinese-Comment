# XML Agent

`XML Agent` 是一种使用 XML 标签来结构化推理过程和工具调用的代理。它特别适用于那些对标签（Tags）解析能力强、但对复杂 JSON 遵循度不高的模型（如早期版本的 Claude）。

## 核心机制

代理要求模型使用特定的 XML 标签来包裹其输出：
- `<tool>`: 要调用的工具名称。
- `<tool_input>`: 输入给工具的参数。
- `<observation>`: 工具返回的结果（由代理系统填入）。
- `<final_answer>`: 最终返回给用户的答案。

## 运行逻辑

1. **Plan**: `plan` 方法会将中间步骤格式化为 XML 字符串。
2. **Stop Sequences**: 代理会自动设置停止词 `</tool_input>` 和 `</final_answer>`，以防止模型产生冗余输出。
3. **Prompt**: 默认提示词 `agent_instructions` 定义了可用的工具列表和 XML 格式要求。

## 示例

**LLM 输出示例**:
```xml
I need to check the weather.
<tool>weather_search</tool><tool_input>San Francisco</tool_input>
```

**代理反馈**:
```xml
<observation>Sunny, 20°C</observation>
The weather is nice.
<final_answer>The weather in San Francisco is sunny and 20°C.</final_answer>
```

## 迁移方案

现代 LangChain 推荐使用更通用的 `create_xml_agent` 函数：

```python
from langchain.agents import create_xml_agent
from langchain_openai import ChatOpenAI
from langchain import hub

model = ChatOpenAI()
tools = [...]
prompt = hub.pull("hwchase17/xml-agent-convo")

agent = create_xml_agent(model, tools, prompt)
```

对于 Anthropic 模型，现在通常推荐使用其原生的 Tool Calling 能力（通过 `create_tool_calling_agent`）。
