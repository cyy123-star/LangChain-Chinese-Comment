# libs\langchain\langchain_classic\agents\format_scratchpad\openai_functions.py

此文档提供了 `libs\langchain\langchain_classic\agents\format_scratchpad\openai_functions.py` 文件的详细中文注释。该模块专门用于为 OpenAI 的函数调用（Function Calling）接口格式化草稿纸。

## 核心函数：`format_to_openai_function_messages`

该函数将中间步骤转换为 OpenAI 特有的 `FunctionMessage` 序列，使得模型能够识别先前的函数调用结果。

### 1. 工作原理
该函数通过 `_convert_agent_action_to_messages` 处理每个步骤：
1. **重构 AI 消息**: 如果 `AgentAction` 包含消息日志（`AgentActionMessageLog`），则直接还原原始的 `AIMessage`；否则，根据 `action.log` 创建一个新的 `AIMessage`。
2. **创建函数消息**: 使用 `_create_function_message` 将工具输出转换为 `FunctionMessage`。
   - **名称匹配**: `FunctionMessage` 的 `name` 字段必须与发起调用的 `agent_action.tool` 名称完全一致。
   - **内容序列化**: 如果观测结果（Observation）不是字符串，函数会尝试使用 `json.dumps` 对其进行序列化。

### 2. 输出示例
```python
[
    AIMessage(content="", additional_kwargs={"function_call": {"name": "get_weather", "arguments": "..."}}),
    FunctionMessage(name="get_weather", content="{\"temp\": 25}")
]
```

## 内部辅助函数

- **`_create_function_message`**: 处理观测结果到字符串的转换，包含异常处理逻辑。
- **`_convert_agent_action_to_messages`**: 确保 `message_log` 中的所有上下文（如模型的思考过程）都能被正确保留。

## 注意事项

- **OpenAI 专用**: 该格式化方式严格遵循 OpenAI 旧版的 Functions API 规范。
- **兼容性别名**: 模块提供了 `format_to_openai_functions` 作为后向兼容的别名。
- **现代迁移**: 对于使用 OpenAI "Tools"（支持并行调用）的模型，应改用 `openai_tools.py` 中的格式化函数。
