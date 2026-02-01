# libs\langchain\langchain_classic\agents\self_ask_with_search\__init__.py

此文档提供了 `libs\langchain\langchain_classic\agents\self_ask_with_search\__init__.py` 文件的详细中文注释。

## 功能描述

该模块实现了基于 "Self-Ask with Search" 论文的代理逻辑。这种代理专门用于处理复杂的多步查询，通过将问题拆分为多个子问题，并利用搜索引擎获取中间答案来得出最终结论。

## 主要组件

- `SelfAskWithSearchAgent`: 实现自我提问逻辑的代理类。
- `create_self_ask_with_search_agent`: 用于创建该类型代理的工厂函数（推荐使用）。
- `SelfAskWithSearchChain`: [已弃用] 用于执行自我提问逻辑的链。

## 核心逻辑

1. **问题拆分**: 模型接收到一个复杂问题。
2. **中间问题**: 模型产生一个子问题，需要通过搜索工具回答。
3. **中间答案**: 搜索工具提供答案。
4. **循环**: 重复步骤 2 和 3，直到模型获得足够信息。
5. **最终答案**: 模型提供问题的最终答案。

## 注意事项

- **工具限制**: 该代理通常只接受一个名为 `Intermediate Answer` 的工具，通常是一个搜索引擎（如 Google Search 或 SerpAPI）。
- **提示词**: 该代理使用特定的提示词模板，引导模型进行子问题的拆分和回答。

