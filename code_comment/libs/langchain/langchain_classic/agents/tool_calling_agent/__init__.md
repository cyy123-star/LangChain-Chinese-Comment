# libs\langchain\langchain_classic\agents\tool_calling_agent\__init__.py

此文档提供了 `libs\langchain\langchain_classic\agents\tool_calling_agent\__init__.py` 文件的详细中文注释。

## 功能描述

该模块提供了一种创建支持通用“工具调用”（Tool Calling）能力的代理的方法。这种代理利用现代 LLM（如 GPT-4, Claude 3, Gemini 等）原生支持的工具调用接口，而不是依赖于复杂的提示工程或特定的解析逻辑。

## 主要函数

- `create_tool_calling_agent`: 创建一个工具调用代理。它返回一个可运行对象（Runnable），该对象接受输入并产生 `AgentAction` 或 `AgentFinish`。

## 核心优势

1. **原生支持**: 使用模型厂商提供的 API（如 OpenAI 的 `tools` 参数），比 `structured-chat` 或 `openai-functions` 更通用。
2. **结构化思维**: 模型能更稳定地生成正确的工具调用参数。
3. **LCEL 兼容**: 生成的代理是一个 Runnable，可以方便地与其他组件组合。

## 注意事项

- 提示模板（Prompt）必须包含 `agent_scratchpad` 变量（通常作为 `MessagesPlaceholder`），用于存放中间步骤和工具返回的消息。
- 建议优先使用此代理类型，因为它代表了现代 LLM 与工具交互的标准方式。

