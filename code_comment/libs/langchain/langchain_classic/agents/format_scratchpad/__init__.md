# libs\langchain\langchain_classic\agents\format_scratchpad\__init__.py

此文档提供了 `libs\langchain\langchain_classic\agents\format_scratchpad\__init__.py` 文件的详细中文注释。

## 功能描述

该模块包含将代理执行过程中的“中间步骤”（Intermediate Steps）格式化为“草稿本”（Scratchpad）的逻辑。中间步骤是 `(AgentAction, observation)` 元组的列表，记录了代理之前的思考、行动和观察结果。

## 格式化函数

根据不同的提示策略，该模块提供了多种格式化方式：

1. **字符串格式化**:
   - `format_log_to_str`: 将步骤转换为单一的文本字符串，常用于传统的 ReAct 代理。
2. **消息列表格式化**:
   - `format_log_to_messages`: 将步骤转换为 `AIMessage` 和 `HumanMessage` 序列，常用于聊天模型。
3. **特定模型/格式支持**:
   - `format_to_openai_function_messages`: 转换为 OpenAI 函数调用所需的消息格式。
   - `format_to_tool_messages`: 转换为现代工具调用（Tool Calling）的消息格式。
   - `format_xml`: 转换为 XML 代理所需的 XML 标签格式。

## 核心作用

草稿本（Scratchpad）是代理能够“记住”之前发生了什么的关键。通过将这些信息以模型能理解的方式传回，模型才能决定下一步是继续尝试新方法还是给出最终答案。

