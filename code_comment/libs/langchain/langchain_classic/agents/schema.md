# libs\langchain\langchain_classic\agents\schema.py

此文档提供了 `libs\langchain\langchain_classic\agents\schema.py` 文件的详细中文注释。该模块定义了用于处理代理“草稿本”（Scratchpad）的特定提示词模板类。

## 功能描述

在代理的推理循环中，模型需要看到自己之前的思考过程和工具执行结果。`schema.py` 提供了一个专门的 `ChatPromptTemplate` 子类，用于将这些中间步骤格式化并注入到提示词中。

## 核心类：`AgentScratchPadChatPromptTemplate`

该类继承自 `ChatPromptTemplate`，专门用于管理聊天代理的推理轨迹。

### 1. 核心方法

#### `_construct_agent_scratchpad(intermediate_steps)`
- **作用**: 将历史步骤列表转换为文本。
- **输入**: `list[tuple[AgentAction, str]]`（动作与观察结果的对）。
- **逻辑**: 遍历历史，将 `action.log`（包含思考和动作指令）与 `observation` 拼接。
- **ReAct 风格**: 它会在结尾添加 "Thought: "，引导 LLM 进行下一步思考。

#### `_merge_partial_and_user_variables(**kwargs)`
- **作用**: 变量预处理。
- **逻辑**: 从输入变量中提取 `intermediate_steps`，将其转换为 `agent_scratchpad` 字符串，从而使 Prompt 模板中的 `{agent_scratchpad}` 占位符能够被正确填充。

### 2. 序列化说明
- `is_lc_serializable`: 返回 `False`。这意味着该特定的模板类不支持标准的 LangChain 序列化流程。

## 设计模式与现状

- **草稿本模式**: 这是经典 ReAct 代理的核心设计。它通过在 Prompt 中不断追加“思考-行动-观察”的历史，来维持模型的上下文意识。
- **局限性**: 将所有历史转换为单一字符串在处理长对话或复杂工具输出时效率较低，且容易超出上下文窗口。
- **现代替代方案**: 
  - 现代 LangChain 代理（如 `OpenAIToolsAgent`）通常使用消息序列（`AIMessage` + `ToolMessage`）来替代这种文本拼接方式。
  - 格式化逻辑已解耦到独立函数中（如 `format_to_openai_tools`）。

