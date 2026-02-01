# libs\langchain\langchain_classic\agents\output_parsers\react_json_single_input.py

此文档提供了 `libs\langchain\langchain_classic\agents\output_parsers\react_json_single_input.py` 文件的详细中文注释。该解析器用于处理结合了 ReAct 思维链与 JSON 格式指令的输出。

## 核心类：`ReActJsonSingleInputOutputParser`

该解析器主要用于 `ChatAgent` 这种需要模型先输出 "Thought" 然后输出 JSON "Action" 的场景。

### 1. 预期格式
模型输出应包含思维过程，并以 Markdown 代码块形式包裹 JSON：
```text
Thought: I need to check the price.
Action:
```json
{
    "action": "search",
    "action_input": "price of gold"
}
```
```

或者给出最终回答：
```text
Thought: I have the answer.
Final Answer: Gold is $2000 per ounce.
```

### 2. 工作原理
- **正则表达式匹配**: 使用 `r"^.*?`{3}(?:json)?\n?(.*?)`{3}.*?$"` 提取 Markdown 中的 JSON 字符串。
- **分流逻辑**:
  - **优先检查 Action**: 如果成功提取出 JSON 且包含 `action` 字段，则返回 `AgentAction`。
  - **备选检查 Final Answer**: 如果没有找到 JSON，或者在解析过程中失败，解析器会检查文本中是否包含 `"Final Answer:"` 字符串。
  - **冲突处理**: 如果文本中既有可解析的 Action 也有 Final Answer，会抛出异常。

## 注意事项

- **容错性**: 该解析器设计了“快速失败”机制，即如果找不到 Action 标签，会尝试回退到解析最终答案。
- **指令一致性**: `get_format_instructions` 方法会返回预定义的 JSON 格式指令，确保模型输出符合预期。
- **单输入限制**: 顾名思义，它仅支持单步单工具调用（Single Input）。
