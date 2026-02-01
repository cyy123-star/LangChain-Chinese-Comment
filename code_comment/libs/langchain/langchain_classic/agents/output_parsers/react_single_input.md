# libs\langchain\langchain_classic\agents\output_parsers\react_single_input.py

此文档提供了 `libs\langchain\langchain_classic\agents\output_parsers\react_single_input.py` 文件的详细中文注释。该解析器用于处理传统的 ReAct 风格文本输出（非 JSON 格式）。

## 1. 核心类：`ReActSingleInputOutputParser`

该解析器通过正则表达式从 LLM 生成的纯文本中提取工具名称和输入。

### 解析逻辑

1. **关键词识别**:
   - `Final Answer:` -> 识别为最终答案（`AgentFinish`）。
   - `Action:` 和 `Action Input:` -> 识别为工具调用（`AgentAction`）。
2. **正则匹配**:
   - 使用正则表达式 `Action\s*\d*\s*:[\s]*(.*?)[\s]*Action\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)` 提取工具和输入。
   - 这种正则设计允许 `Action` 后面带有数字（例如 `Action 1:`），具有较强的鲁棒性。
3. **分流逻辑**:
   - **优先 Action**: 如果匹配到 Action 且包含 `Final Answer:`，抛出异常。
   - **备选 Final Answer**: 如果没有 Action 但有 `Final Answer:`，返回最终结果。
   - **错误重试 (Self-Correction)**:
     - 如果只有 `Thought:` 而没有 `Action:` -> 抛出异常，并设置 `send_to_llm=True`，将错误提示发回 LLM 要求修正。
     - 如果只有 `Action:` 而没有 `Action Input:` -> 同样触发 Self-Correction。

---

## 2. 期望的输出格式

```text
Thought: 我需要查一下天气。
Action: search
Action Input: 北京今天天气
```

## 技术细节

- **格式指令**: 通过 `get_format_instructions()` 返回 MRKL 风格的交互规范。
- **Self-Correction**: 它是 LangChain 早期实现“自修复解析”的典型例子，通过特定的错误消息引导模型重新生成正确格式。
- **类型标识**: `_type` 为 `"react-single-input"`。

## 关联组件

- [mrkl/prompt.py](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/mrkl/prompt.md): 提供默认的 `FORMAT_INSTRUCTIONS`。
