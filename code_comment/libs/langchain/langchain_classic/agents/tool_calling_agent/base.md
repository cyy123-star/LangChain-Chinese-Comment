# libs\langchain\langchain_classic\agents\tool_calling_agent\base.py

此文档提供了 `libs\langchain\langchain_classic\agents\tool_calling_agent\base.py` 文件的详细中文注释。该模块实现了通用的工具调用代理，旨在支持各种提供商（如 Anthropic, Google, Mistral 等）的工具调用能力。

## 核心函数：`create_tool_calling_agent`

这是一个高层工厂函数，用于创建利用模型原生工具调用（Tool Calling）能力的代理。

**函数签名**:
```python
def create_tool_calling_agent(
    llm: BaseLanguageModel,
    tools: Sequence[BaseTool],
    prompt: ChatPromptTemplate,
    *,
    message_formatter: MessageFormatter = format_to_tool_messages,
) -> Runnable
```

### 1. 参数说明

| 参数 | 类型 | 描述 | 默认值 |
| :--- | :--- | :--- | :--- |
| `llm` | `BaseLanguageModel` | 必须是实现了 `bind_tools` 的聊天模型。 | - |
| `tools` | `Sequence[BaseTool]` | 代理可调用的工具列表。 | - |
| `prompt` | `ChatPromptTemplate` | 提示词模板。必须包含 `agent_scratchpad` 变量。 | - |
| `message_formatter` | `MessageFormatter` | 负责将中间步骤转换为消息序列。 | `format_to_tool_messages` |

### 2. 设计目标
- **跨平台支持**: 与 `OpenAIToolsAgent` 不同，该代理设计更为通用，旨在适配所有支持 `bind_tools` 方法的现代聊天模型。
- **标准化流程**: 统一了不同模型提供商在工具调用上的差异，提供一致的开发体验。
- **LCEL 驱动**: 产生的代理是一个 `Runnable` 序列，可以无缝集成到 LangChain 的各种链式操作中。

### 2. 函数参数说明
- **`llm`**: 必须是实现了 `bind_tools` 的聊天模型（如 `ChatAnthropic`, `ChatGoogleGenerativeAI` 等）。
- **`tools`**: 代理可用的工具列表。
- **`prompt`**: `ChatPromptTemplate` 类型的提示词模板。
- **`message_formatter`**: 消息格式化函数。默认为 `format_to_tool_messages`，负责将代理的中间步骤转换为模型能理解的消息历史。

### 3. 提示词要求
传入的 `prompt` 必须包含一个 `agent_scratchpad` 占位符（通常使用 `MessagesPlaceholder`）。该占位符在运行时会被填充为工具调用的中间记录。

### 4. 工作原理
1. **绑定工具**: 调用 `llm.bind_tools(tools)`，将工具定义告知模型。
2. **构建序列**:
   - 准备输入变量（包括用户输入和渲染后的工具信息）。
   - 将中间步骤（`intermediate_steps`）通过 `message_formatter` 转换为消息序列。
   - 传递给提示词模板。
   - 调用模型获取响应。
   - 使用 `ToolsAgentOutputParser` 解析模型输出。

## 使用示例

```python
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant"),
    ("placeholder", "{chat_history}"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

model = ChatAnthropic(model="claude-3-opus-20240229")
agent = create_tool_calling_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)
```

## 注意事项

1. **推荐性**: 这是目前在非 OpenAI 模型（以及 OpenAI 模型）上实现工具调用最通用、最推荐的方式。
2. **序列化**: 确保工具的输出是可序列化的，否则可能会在格式化消息时出错。
3. **灵活性**: 相比于特定供应商的代理，它更易于在不同模型之间切换。
