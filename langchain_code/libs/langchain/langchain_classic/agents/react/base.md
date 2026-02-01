# ReActDocstoreAgent

`ReActDocstoreAgent` 是 [ReAct 论文](https://arxiv.org/pdf/2210.03629.pdf) 的直接实现。它专门设计用于与 **Docstore (文档库)** 交互，通常只有两个固定的工具：`Search` 和 `Lookup`。

> **注意**: 该代理已弃用。现代实现通常使用更通用的 RAG (Retrieval-Augmented Generation) 流程或 LangGraph 代理。

## 核心工具集

该代理强制要求且仅允许两个工具：
- **Search**: 在文档库中搜索相关的页面或文档。
- **Lookup**: 在当前打开的文档中查找特定的术语或关键词。

## 运行逻辑

1. **Search**: 当代理需要新信息时，它会调用 `Search`。
2. **Observation**: `Search` 返回页面的摘要或第一段内容。
3. **Lookup**: 如果摘要中提到了一些关键词，代理可以使用 `Lookup` 在该页面内进行深度搜索。
4. **Thought**: 代理根据观察到的信息更新其内部状态，并决定是继续搜索还是给出最终答案。

## 提示词模版

默认使用 `WIKI_PROMPT`，其结构模拟了人类在维基百科上查阅资料解决复杂问题的过程：
```text
Question: [用户问题]
Thought: I need to search for [关键词].
Action: Search[关键词]
Observation: [搜索结果]
Thought: [根据结果进一步推理]
...
Final Answer: [最终答案]
```

## 迁移方案

现代应用通常不再使用这种受限的固定工具代理，而是采用以下方案：
- **通用 ReAct 代理**: 使用 `create_react_agent` 并传入更灵活的检索工具（如 `WikipediaQueryRun`）。
- **LangGraph RAG**: 构建一个包含检索节点和生成节点的有向图，支持多轮检索和反思。
