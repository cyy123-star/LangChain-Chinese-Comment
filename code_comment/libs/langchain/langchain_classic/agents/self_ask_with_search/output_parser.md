# libs\langchain\langchain_classic\agents\self_ask_with_search\output_parser.py

此文档提供了 `libs\langchain\langchain_classic\agents\self_ask_with_search\output_parser.py` 文件的详细中文注释。该文件主要用于向后兼容。

## 核心组件

- **`SelfAskOutputParser`**: 该模块实际上是对 `langchain_classic.agents.output_parsers.self_ask.SelfAskOutputParser` 的重新导出（Re-export）。

## 功能说明

该解析器的核心逻辑定义在通用的输出解析器目录中，其主要职责是：
1. 识别模型输出末尾的 `"Follow up:"` 标签以触发子问题搜索。
2. 识别 `"So the final answer is: "` 标签以提取任务的最终结论。

## 关联文档

- [通用的 SelfAskOutputParser 实现](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/output_parsers/self_ask.md): 详细记录了具体的正则匹配和解析逻辑。

