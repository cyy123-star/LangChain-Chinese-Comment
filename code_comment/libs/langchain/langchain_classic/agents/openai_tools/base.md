# libs\langchain\langchain_classic\agents\openai_tools\base.py

此文档提供了 `libs\langchain\langchain_classic\agents\openai_tools\base.py` 文件的详细中文注释。该模块定义了利用 OpenAI 原生工具调用能力创建代理的核心逻辑。

## 函数：`create_openai_tools_agent`

此函数用于创建一个 `Runnable` 对象，代表一个专门针对 OpenAI 工具接口优化的代理。相比于旧的 `openai-functions` 代理，它具有更强的能力和更好的稳定性。

### 1. 函数签名

```python
def create_openai_tools_agent(
    llm: BaseLanguageModel,
    tools: Sequence[BaseTool],
    prompt: ChatPromptTemplate,
    strict: bool | None = None,
) -> Runnable
```

### 2. 参数说明

| 参数 | 类型 | 描述 |
| :--- | :--- | :--- |
| `llm` | `BaseLanguageModel` | 支持 OpenAI 工具调用接口的语言模型。 |
| `tools` | `Sequence[BaseTool]` | 代理可以访问的工具列表。 |
| `prompt` | `ChatPromptTemplate` | 提示词模板（需包含 `agent_scratchpad` 变量）。 |
| `strict` | `bool \| None` | [可选] 是否对 OpenAI 工具使用严格模式（确保模型输出严格符合 Schema）。 |

### 3. 提示词要求

传入的 `prompt` 必须包含以下关键变量：
- **`agent_scratchpad`**: 必须是一个 `MessagesPlaceholder`。它用于存储模型之前的 `tool_calls` 以及系统返回的 `ToolMessage`。

**示例提示词结构**:
```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个得力助手。"),
    MessagesPlaceholder("chat_history", optional=True),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad"),
])
```

## 核心工作流

1. **变量验证**: 确保提示词中包含必需的 `agent_scratchpad`。
2. **工具预处理**: 使用 `convert_to_openai_tool` 将 `BaseTool` 对象转换为 OpenAI API 所需的 JSON Schema。
3. **能力绑定**: 将工具定义绑定到 LLM 实例上。
4. **LCEL 链式构建**:
    - **分配草稿本**: 使用 `format_to_openai_tool_messages` 将 `intermediate_steps`（历史行动和观察）转化为 OpenAI 格式的消息列表。
    - **执行序列**: `RunnablePassthrough` -> `prompt` -> `llm_with_tools` -> `OpenAIToolsAgentOutputParser`。

## 与旧版 Functions Agent 的区别

- **多工具并发**: 支持在单次模型响应中请求调用多个工具。
- **并行执行能力**: 配合 `AgentExecutor`，可以显著提升处理多个独立子任务的效率。
- **严格模式**: 支持 OpenAI 最新的 `strict` 参数，进一步降低格式错误的风险。

## 使用示例

```python
from langchain_openai import ChatOpenAI
from langchain_classic.agents import AgentExecutor, create_openai_tools_agent

model = ChatOpenAI(model="gpt-4o")
tools = [...] # 你的工具列表
prompt = ...   # 见上方的提示词要求

# 创建代理
agent = create_openai_tools_agent(model, tools, prompt)

# 创建执行器并调用
agent_executor = AgentExecutor(agent=agent, tools=tools)
agent_executor.invoke({"input": "帮我对比一下北京和上海明天的天气"})
```

## 关联文件

- [output_parsers](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/output_parsers/openai_tools.md): 该代理使用的 `OpenAIToolsAgentOutputParser` 实现。
- [format_scratchpad](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/format_scratchpad/openai_tools.md): 负责消息格式转换的 `format_to_openai_tool_messages`。

