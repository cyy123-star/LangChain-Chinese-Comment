# libs\langchain\langchain_classic\agents\react\base.py

此文档提供了 `libs\langchain\langchain_classic\agents\react\base.py` 文件的详细中文注释。该文件包含了 ReAct 框架的早期实现，特别是针对文档存储（Docstore）探索的代理。

## 核心类

### 1. `ReActDocstoreAgent` (已弃用)

专门为维基百科样式的文档存储搜索设计的代理。

- **工作方式**: 强制模型在 `Search`（搜索）和 `Lookup`（在找到的文档中查找）之间交替，直到找到答案。
- **默认提示词**: [WIKI_PROMPT](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/react/wiki_prompt.md)。
- **工具限制**: 必须恰好提供两个工具，名称分别为 `Search` 和 `Lookup`。

### 2. `DocstoreExplorer` (已弃用)

辅助代理进行文档存储探索的工具类。

- **`search(term)`**: 在文档存储中搜索词条。如果找到，保存该文档并返回摘要。
- **`lookup(term)`**: 在当前保存的文档中查找词条。支持通过重复调用来循环查找多个匹配项。

### 3. `ReActTextWorldAgent` (已弃用)

专门为 TextWorld（文本游戏）环境设计的 ReAct 代理。

- **默认提示词**: [TEXTWORLD_PROMPT](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/react/textworld_prompt.md)。
- **工具限制**: 必须恰好提供一个名为 `Play` 的工具。

### 4. `ReActChain` (已弃用)

将 `ReActDocstoreAgent` 和 `DocstoreExplorer` 封装在一起的链式实现。它是 ReAct 论文在 LangChain 中的最初落地形式。

## 弃用说明与迁移

!!! danger "已弃用"
    此文件中的所有主要组件均已标记为弃用（从 v0.1.0 开始），并计划在 v1.0 中移除。

### 迁移指南

- **通用任务**: 请迁移到 [agent.py](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/react/agent.md) 中的 `create_react_agent`。
- **生产环境**: 强烈建议使用 **LangGraph**。
- **Docstore 任务**: 现在的推荐做法是使用 RAG (Retrieval Augmented Generation) 架构，配合向量数据库和专门的检索链。

## 技术细节

- **停止序列**: 默认使用 `\nObservation:`，确保 LLM 在需要工具反馈时停止生成。
- **前缀**: 
    - `observation_prefix`: "Observation: "
    - `llm_prefix`: "Thought:"
- **验证**: 使用 `validate_tools_single_input` 确保所有工具都只接受单个字符串输入，这是早期 ReAct 解析器的局限性。

## 关联组件

- [wiki_prompt.py](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/react/wiki_prompt.md): 预定义的维基百科搜索示例。
- [textworld_prompt.py](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/react/textworld_prompt.md): 预定义的文本游戏示例。
- [output_parser.py](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/react/output_parser.md): 处理 `Action[input]` 格式的解析逻辑。
