# libs\langchain\langchain_classic\agents\json_chat\base.py

此文档提供了 `libs\langchain\langchain_classic\agents\json_chat\base.py` 文件的详细中文注释。该模块定义了创建 JSON 聊天代理的核心函数。

## 文件概述

`create_json_chat_agent` 是 LangChain v0.1 之后推荐的创建代理的方式之一。它不再依赖复杂的类继承，而是基于 **LCEL (LangChain Expression Language)** 构建，使得代理的逻辑更加透明且易于自定义。

## 核心函数：`create_json_chat_agent`

该函数构建了一个 `Runnable` 序列，代表一个能够以 JSON 格式进行推理和决策的代理。

### 1. 函数签名

```python
def create_json_chat_agent(
    llm: BaseLanguageModel,
    tools: Sequence[BaseTool],
    prompt: ChatPromptTemplate,
    stop_sequence: bool | list[str] = True,
    tools_renderer: ToolsRenderer = render_text_description,
    template_tool_response: str = TEMPLATE_TOOL_RESPONSE,
) -> Runnable
```

### 2. 参数说明

| 参数 | 类型 | 描述 |
| :--- | :--- | :--- |
| `llm` | `BaseLanguageModel` | 用作代理的语言模型。 |
| `tools` | `Sequence[BaseTool]` | 代理可以访问的工具列表。 |
| `prompt` | `ChatPromptTemplate` | 提示词模板（需包含特定变量，见下文）。 |
| `stop_sequence` | `bool \| list[str]` | 是否添加停止序列。默认为 `True`（添加 `"Observation:"`）。 |
| `tools_renderer` | `ToolsRenderer` | 将工具列表渲染为字符串的函数，默认为文本描述渲染。 |
| `template_tool_response` | `str` | 工具执行结果回传给 LLM 时的模板。 |

### 3. 提示词要求

传入的 `prompt` 必须包含以下变量：
- `tools`: 自动注入的所有工具的描述和参数说明。
- `tool_names`: 所有工具的名称列表。
- `agent_scratchpad`: 必须是一个 `MessagesPlaceholder`，用于存储之前的行动和观察结果。

## 内部工作流程 (LCEL 序列)

1. **处理中间步骤**: 通过 `format_log_to_messages` 将 `intermediate_steps`（历史行动和观察）格式化为消息列表，并赋值给 `agent_scratchpad`。
2. **填充提示词**: 将工具信息、用户输入和草稿本内容填入 `prompt`。
3. **调用 LLM**: 将填充后的提示词发送给 LLM。如果启用了 `stop_sequence`，会为模型绑定停止词。
4. **解析输出**: 使用 `JSONAgentOutputParser` 解析 LLM 返回的内容，将其转化为 `AgentAction` 或 `AgentFinish`。

## 使用示例

```python
from langchain_openai import ChatOpenAI
from langchain_classic.agents import AgentExecutor, create_json_chat_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 定义提示词
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个得力助手。"),
    MessagesPlaceholder("chat_history", optional=True),
    ("human", "{input}\n\n{tools}\n\n{tool_names}"),
    MessagesPlaceholder("agent_scratchpad"),
])

# 创建代理
agent = create_json_chat_agent(model, tools, prompt)

# 创建执行器
agent_executor = AgentExecutor(agent=agent, tools=tools)
```

## 设计意图

- **结构化稳定性**: JSON 格式比纯文本更易于解析，减少了代理因为输出格式微调而崩溃的风险。
- **可组合性**: 作为一个 `Runnable` 对象，它可以轻松地与其他组件（如 Memory、Callbacks）集成。
- **防止幻觉**: 通过 `stop_sequence` 机制，在模型尝试伪造工具返回结果（即生成 "Observation:" 之后的内容）时强制停止。

## 关联文件

- [prompt.py](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/json_chat/prompt.md): 定义了 `TEMPLATE_TOOL_RESPONSE`。
- [output_parsers](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/output_parsers/json.md): 该代理使用的 `JSONAgentOutputParser` 实现。
