# libs\langchain\langchain_classic\agents\agent_toolkits\conversational_retrieval\openai_functions.py

该模块提供了一个基于 OpenAI 函数调用（Function Calling）功能的会话检索代理工厂函数。它专门优化了在对话中使用检索工具的流程。

## 核心函数

### `create_conversational_retrieval_agent`

创建一个配置好的 `AgentExecutor`，专门用于处理带检索功能的对话。

#### 参数说明

| 参数 | 类型 | 描述 |
| :--- | :--- | :--- |
| `llm` | `BaseLanguageModel` | 语言模型，通常应使用支持函数调用的 `ChatOpenAI`。 |
| `tools` | `list[BaseTool]` | 代理可以访问的工具列表，通常包含一个或多个检索工具。 |
| `remember_intermediate_steps` | `bool` | 是否让代理记住中间步骤（Action/Observation 对）。默认为 `True`。开启后有助于处理依赖先前信息的后续问题，但会消耗更多 Token。 |
| `memory_key` | `str` | Prompt 中用于存储对话历史的变量名。默认为 `"chat_history"`。 |
| `system_message` | `SystemMessage` | 初始系统提示词。如果未提供，将使用默认提示词。 |
| `verbose` | `bool` | 是否在终端输出代理的详细思考过程。默认为 `False`。 |
| `max_token_limit` | `int` | 内存中保留的最大 Token 数量。用于自动截断过长的历史记录。默认为 `2000`。 |
| `**kwargs` | `Any` | 传递给 `AgentExecutor` 的其他关键字参数。 |

#### 内部实现流程

1.  **内存管理逻辑**:
    - 系统会检查 `remember_intermediate_steps`。
    - 若为 `True`，则实例化 `AgentTokenBufferMemory`。该类不仅通过 `ChatMessageHistory` 保存对话，还会将代理的 `intermediate_steps`（中间思考和工具返回结果）格式化为 `FunctionMessage` 保存到上下文中。
    - 若为 `False`，则使用 `ConversationTokenBufferMemory`，仅保存用户和 AI 的对话。
2.  **提示词模板构建**:
    - 调用 `OpenAIFunctionsAgent.create_prompt`。
    - 自动在提示词末尾添加 `MessagesPlaceholder(variable_name=memory_key)`，用于动态注入历史消息。
3.  **代理初始化**:
    - 实例化 `OpenAIFunctionsAgent`。
    - 最终将代理、工具和内存封装进 `AgentExecutor` 返回。

## 默认系统提示词

```text
Do your best to answer the questions. Feel free to use any tools available to look up relevant information, only if necessary
```

## 使用示例

```python
from langchain_openai import ChatOpenAI
from langchain_classic.agents.agent_toolkits import create_conversational_retrieval_agent
from langchain_classic.tools.retriever import create_retriever_tool

# 初始化 LLM
llm = ChatOpenAI(model="gpt-4", temperature=0)

# 假设你已经有一个 retriever (例如来自 Chroma 或 Pinecone)
retriever = vectorstore.as_retriever()

# 创建检索工具
tool = create_retriever_tool(
    retriever,
    "search_docs",
    "搜索关于特定主题的文档内容。"
)
tools = [tool]

# 创建代理执行器
agent_executor = create_conversational_retrieval_agent(llm, tools)

# 执行对话
result = agent_executor.invoke({"input": "什么是 LangChain？"})
print(result["output"])
```

## 注意事项

- **Token 消耗**: `remember_intermediate_steps=True` 会显著增加 Token 消耗，因为它将之前的思考过程和工具输出都放进了上下文。
- **模型限制**: 该方法硬编码使用了 `OpenAIFunctionsAgent`，因此只适用于支持 OpenAI 函数调用格式的模型。
- **并发建议**: 如果在生产环境使用，建议通过 `max_concurrency` 限制并发请求。
