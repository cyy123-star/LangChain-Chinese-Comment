# libs\langchain\langchain_classic\agents\agent_toolkits\vectorstore\base.py

此文档提供了 `libs\langchain\langchain_classic\agents\agent_toolkits\vectorstore\base.py` 文件的详细中文注释。该模块实现了用于与向量数据库（Vector Store）交互的代理创建函数。

## 核心功能

该模块提供了一种简便的方法来创建一个能够查询向量数据库并根据检索到的文档回答问题的代理。它支持单一向量库查询以及在多个向量库之间进行路由。

## 核心函数

### 1. `create_vectorstore_agent`
- **功能**: 构建一个向量数据库代理。
- **函数原型**:
    ```python
    def create_vectorstore_agent(
        llm: BaseLanguageModel,
        toolkit: VectorStoreToolkit,
        callback_manager: Optional[BaseCallbackManager] = None,
        prefix: str = PREFIX,
        verbose: bool = False,
        agent_executor_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> AgentExecutor:
    ```
- **参数**:
    - `llm`: 用于推理和回答问题的语言模型。
    - `toolkit`: `VectorStoreToolkit` 实例，包含了向量库的信息。
    - `prefix`: 提示词前缀，定义了代理的角色和行为。
- **实现原理**: 内部使用 `ZeroShotAgent` 和 `AgentExecutor`。它将向量库包装成两个工具：一个用于普通问答，一个用于带来源的问答。

### 2. `create_vectorstore_router_agent`
- **功能**: 创建一个能够在多个向量数据库之间选择最相关的一个进行查询的代理。
- **函数原型**:
    ```python
    def create_vectorstore_router_agent(
        llm: BaseLanguageModel,
        toolkit: VectorStoreRouterToolkit,
        callback_manager: Optional[BaseCallbackManager] = None,
        prefix: str = ROUTER_PREFIX,
        verbose: bool = False,
        agent_executor_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> AgentExecutor:
    ```
- **参数**:
    - `toolkit`: `VectorStoreRouterToolkit` 实例，包含多个向量库的信息。
- **设计思路**: 适用于知识库被切分为多个不同主题（如：财务文档、HR 文档、技术文档）的场景。

## 弃用说明与建议

**该类已标记为弃用 (since 0.2.13)**。

### 为什么弃用？
虽然该功能仍然可用，但 LangChain 官方现在更推荐使用 **LangGraph** 来构建此类代理。LangGraph 提供了更强大的灵活性、状态持久化以及“人在回路”（Human-in-the-loop）的工作流支持。

### 现代替代方案 (迁移到 LangGraph)
```python
from langchain_core.tools import create_retriever_tool
from langgraph.prebuilt import create_react_agent

# 1. 创建检索工具
tool = create_retriever_tool(
    vector_store.as_retriever(),
    "pet_info_retriever",
    "获取有关宠物的详细信息。"
)

# 2. 使用 LangGraph 创建 ReAct 代理
agent = create_react_agent(model, [tool])
```

## 注意事项

- **依赖**: 运行此模块需要安装 `langchain-community`，因为底层的问答工具定义在社区包中。
- **提示词定制**: 开发者可以通过覆盖 `prefix` 来调整代理的语气和约束条件。
