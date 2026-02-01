# libs\langchain\langchain_classic\agents\format_scratchpad\tools.py

此文档提供了 `libs\langchain\langchain_classic\agents\format_scratchpad\tools.py` 文件的详细中文注释。该模块定义了将代理动作和观测结果转换为现代 `ToolMessage` 的逻辑。

## 核心函数：`format_to_tool_messages`

该函数旨在支持所有实现了标准 Tool Calling 接口的模型（如 Anthropic, Google, 以及 OpenAI 的新版 Tools API）。

### 1. 工作原理
该函数通过识别 `ToolAgentAction`（包含 `tool_call_id`）来精确关联请求与响应：
1. **识别动作**: 遍历中间步骤，检查 `agent_action` 是否为 `ToolAgentAction`。
2. **重构 AI 消息**: 如果是 `ToolAgentAction`，它会包含模型发出的原始 `tool_calls` 信息（存储在 `message_log` 中）。
3. **创建工具消息**: 调用 `_create_tool_message` 创建 `ToolMessage`。
   - **ID 关联**: 关键在于 `tool_call_id`。模型需要通过这个 ID 来匹配哪个结果对应哪个调用请求。
   - **内容处理**: 自动处理非字符串观测结果的 JSON 序列化。
4. **去重逻辑**: 确保同一个消息不会被重复添加到列表中。

### 2. 输出示例
```python
[
    AIMessage(content="", tool_calls=[{"id": "call_123", "name": "calculator", "args": {...}}]),
    ToolMessage(tool_call_id="call_123", content="42")
]
```

## 内部辅助函数

- **`_create_tool_message`**: 负责将工具输出封装进 `ToolMessage`，并自动处理 JSON 序列化。

## 注意事项

- **通用性**: 这是构建现代代理最推荐的草稿纸格式化方式，因为它符合 LangChain 最新的工具消息规范。
- **ID 缺失处理**: 如果 `agent_action` 不是 `ToolAgentAction`，函数会退而求其次，将其格式化为普通的 `AIMessage(content=action.log)`。
- **OpenAI 别名**: `openai_tools.py` 模块通过别名 `format_to_openai_tool_messages` 重新导出了此函数。
