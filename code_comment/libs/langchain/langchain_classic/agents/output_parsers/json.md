# libs\langchain\langchain_classic\agents\output_parsers\json.py

此文档提供了 `libs\langchain\langchain_classic\agents\output_parsers\json.py` 文件的详细中文注释。该文件实现了专门用于解析 JSON 格式代理输出的解析器。

## 核心类：`JSONAgentOutputParser`

该解析器通过解析 JSON 代码块来决定代理的下一步操作。它被广泛应用于需要结构化推理的场景，如 `ChatAgent` 或 `JSONChatAgent`。

### 1. 期望的输出格式

解析器期望 LLM 返回以下两种 JSON 结构之一：

#### 场景 A：调用工具 (AgentAction)
```json
{
  "action": "工具名称",
  "action_input": "传递给工具的输入"
}
```

#### 场景 B：得出最终结论 (AgentFinish)
```json
{
  "action": "Final Answer",
  "action_input": "给用户的最终回答"
}
```

### 2. 解析逻辑

1. **Markdown 处理**: 使用 `parse_json_markdown` 工具函数，能够自动提取并解析包裹在 ```json ... ``` 中的 JSON 块。
2. **多 Action 处理**: 如果模型违反指令一次输出了多个 Action（以列表形式），解析器会记录警告并默认采用第一个 Action。
3. **容错处理**: 如果 `action_input` 缺失或为 `null`，解析器会将其默认为空字典 `{}`。
4. **异常处理**: 如果文本无法被解析为有效的 JSON，或者缺少必要的 `action` 字段，会抛出 `OutputParserException`。

## 技术细节

- **灵活性**: 虽然它叫 JSON 解析器，但由于底层使用了 `parse_json_markdown`，它对非 JSON 文本（如模型在 JSON 之外写的解释文字）具有一定的免疫力，只要 JSON 块本身是合法的。
- **Final Answer 约定**: 通过将 `"Final Answer"` 作为一种特殊的 `action` 名，统一了工具调用和结论输出的逻辑。

## 关联文件

- [json_chat/base.py](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/json_chat/base.md): `create_json_chat_agent` 默认使用此解析器。
