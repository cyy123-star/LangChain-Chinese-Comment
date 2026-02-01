# Agent Toolkits

Agent Toolkits 是为特定任务或领域（如 SQL 数据库、CSV 文件、OpenAPI 规范等）预配置的一组工具和 Agent 初始化逻辑。

## 核心概念

Toolkit 的目标是简化特定场景下 Agent 的创建过程。它通常包含：
- **Toolkit 类**: 封装了一组相关的 `BaseTool`。
- **工厂函数**: 如 `create_sql_agent`，自动配置 Prompt 并创建 `AgentExecutor`。

## 常用工具包 (Classic & Community)

在 LangChain Classic 中，许多工具包已迁移至 `langchain_community` 或 `langchain_experimental`。

### 1. SQL Agent
用于与 SQL 数据库交互。它包含查询数据库、检查模式、检查查询语句等工具。
- **状态**: 已迁移至 `langchain_community.agent_toolkits.sql`。
- **核心函数**: `create_sql_agent`。
- **迁移建议**: 使用 `langchain_community` 中的版本。

### 2. CSV Agent
用于分析 CSV 文件。它底层使用 Python REPL 来执行数据分析。
- **状态**: 已迁移至 `langchain_experimental.agents.agent_toolkits.csv`。
- **安全警告**: 该 Agent 会执行任意 Python 代码，必须在沙箱环境中运行。

### 3. OpenAPI Agent
用于根据 OpenAPI 规范与 RESTful API 交互。它包含一个分阶段的规划器（Planner），负责将复杂请求分解为多个 API 调用。
- **状态**: 已迁移至 `langchain_community.agent_toolkits.openapi`。
- **核心组件**: `OpenAPIToolkit`, `create_openapi_agent`。

## 执行逻辑示例 (Verbatim Snippet)

### SQL Agent 的创建逻辑 (概念性)
```python
def create_sql_agent(
    llm: BaseLanguageModel,
    toolkit: SQLDatabaseToolkit,
    callback_manager: Optional[BaseCallbackManager] = None,
    prefix: str = SQL_PREFIX,
    suffix: str = SQL_SUFFIX,
    format_instructions: str = FORMAT_INSTRUCTIONS,
    input_variables: Optional[List[str]] = None,
    top_k: int = 10,
    **kwargs: Any,
) -> AgentExecutor:
    # 1. 获取工具列表
    tools = toolkit.get_tools()
    # 2. 构造 Prompt
    prompt = ZeroShotAgent.create_prompt(
        tools,
        prefix=prefix,
        suffix=suffix,
        format_instructions=format_instructions,
        input_variables=input_variables,
    )
    # 3. 初始化 Agent
    llm_chain = LLMChain(llm=llm, prompt=prompt, callback_manager=callback_manager)
    agent = ZeroShotAgent(llm_chain=llm_chain, allowed_tools=[t.name for t in tools])
    # 4. 返回 Executor
    return AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, **kwargs)
```

## 迁移指南 (LangGraph)

现代做法是使用 LangGraph 构建更可控的领域特定 Agent。

### SQL Agent 迁移 (LangGraph)
不再使用黑盒的 `create_sql_agent`，而是显式定义图逻辑：
1. **Node 1 (Query Gen)**: 生成 SQL。
2. **Node 2 (Execute)**: 执行 SQL。
3. **Node 3 (Refine)**: 如果出错，修正 SQL；否则返回结果。

```python
from langgraph.prebuilt import create_react_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit

# 虽然 Toolkit 仍可使用，但运行环境建议切换到 LangGraph
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
tools = toolkit.get_tools()

# 使用 LangGraph 的 ReAct Agent 来替代经典的 AgentExecutor
app = create_react_agent(llm, tools)
```

**为什么迁移？**
1. **错误处理**: 经典的 `AgentExecutor` 很难自定义 SQL 语法错误后的具体重试策略，而 LangGraph 可以通过显式节点轻松实现。
2. **安全性**: 在 LangGraph 中可以更容易地插入审核节点（Human-in-the-loop），在执行写操作前请求人工批准。
