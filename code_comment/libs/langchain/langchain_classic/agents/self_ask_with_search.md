# Self-Ask With Search Agent

`SelfAskWithSearchAgent` 实现了一种特殊的推理策略，灵感来自 "Self-Ask" 论文。它通过将复杂问题拆分为一系列简单的中间问题，并利用搜索工具（如 Google Search）来回答这些中间问题。

## 核心逻辑

该 Agent 并不遵循标准的 ReAct 范式，而是专注于“自问自答”：
1. **自问**: 模型提出一个中间问题（Follow up question）。
2. **搜索**: 调用唯一的搜索工具（必须命名为 "Intermediate Answer"）。
3. **回答**: 得到搜索结果（Intermediate answer）。
4. **最终回答**: 当模型认为已经收集到足够信息时，给出最终答案。

## 限制与约束

- **单一工具**: 必须提供且只能提供一个工具。
- **工具名称**: 该工具的名称必须固定为 `Intermediate Answer`。

## 核心实现 (Verbatim Snippet)

### 1. 工具校验
```python
@classmethod
def _validate_tools(cls, tools: Sequence[BaseTool]) -> None:
    validate_tools_single_input(cls.__name__, tools)
    if len(tools) != 1:
        msg = f"Exactly one tool must be specified, but got {tools}"
        raise ValueError(msg)
    tool_names = {tool.name for tool in tools}
    if tool_names != {"Intermediate Answer"}:
        msg = f"Tool name should be Intermediate Answer, got {tool_names}"
        raise ValueError(msg)
```

### 2. 专用 Chain (SelfAskWithSearchChain)
为了方便使用，LangChain 提供了一个封装好的 Chain 类，只需传入 LLM 和搜索组件即可。
```python
class SelfAskWithSearchChain(AgentExecutor):
    def __init__(
        self,
        llm: BaseLanguageModel,
        search_chain: GoogleSerperAPIWrapper | SearchApiAPIWrapper | SerpAPIWrapper,
        **kwargs: Any,
    ):
        search_tool = Tool(
            name="Intermediate Answer",
            func=search_chain.run,
            description="Search",
        )
        agent = SelfAskWithSearchAgent.from_llm_and_tools(llm, [search_tool])
        super().__init__(agent=agent, tools=[search_tool], **kwargs)
```

## 迁移指南 (Migration)

这种特定的逻辑现在可以通过 **LangGraph** 以更显式的方式实现。

### 现代实现思路
在 LangGraph 中，可以创建一个循环：
1. **思考节点**: 模型决定是继续提问还是直接回答。
2. **搜索节点**: 如果是提问，则调用搜索 API。
3. **反馈节点**: 将搜索结果写回状态，并返回思考节点。

**优势**:
- **透明度**: 你可以清晰地看到每一步拆解出的中间问题。
- **灵活性**: 不再受限于单一工具和固定名称。
