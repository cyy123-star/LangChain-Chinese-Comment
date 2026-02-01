# libs\langchain\langchain_classic\agents\format_scratchpad\log_to_messages.py

此文档提供了 `libs\langchain\langchain_classic\agents\format_scratchpad\log_to_messages.py` 文件的详细中文注释。该模块用于将代理的中间步骤格式化为聊天消息序列（BaseMessage 列表）。

## 核心函数：`format_log_to_messages`

该函数适用于聊天模型（Chat Models），它将代理的推理过程转化为一连串的对话记录。

### 1. 函数参数说明
- **`intermediate_steps`**: 包含 `(AgentAction, Observation)` 元组的列表。
- **`template_tool_response`**: 用于格式化工具观测结果的模板字符串。默认为 `"{observation}"`。

### 2. 工作原理
该函数通过交替创建 `AIMessage` 和 `HumanMessage` 来重构对话流：
1. **`AIMessage`**: 使用 `action.log` 作为内容，代表模型之前的思考和发出的指令。
2. **`HumanMessage`**: 使用格式化后的观测结果作为内容，代表系统（以用户名义）将工具结果反馈给模型。

### 3. 输出结构
返回的是一个消息列表，例如：
```python
[
    AIMessage(content="Thought: I should use the calculator..."),
    HumanMessage(content="Result: 42")
]
```

## 注意事项

- **模拟对话**: 这种方法通过将工具输出伪装成“人类消息”或“系统消息”，使得不支持原生工具调用接口的聊天模型也能实现多步推理。
- **模板灵活性**: 通过 `template_tool_response` 参数，你可以自定义模型接收观测结果时的语气或指令（例如："Here is the tool output: {observation}"）。
- **现代替代**: 对于支持原生 Tool Calling 的模型，建议使用 `format_to_tool_messages` 或 `format_to_openai_tool_messages`。
