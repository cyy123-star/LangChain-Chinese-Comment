# libs\langchain\langchain_classic\agents\mrkl\output_parser.py

此文档提供了 `libs\langchain\langchain_classic\agents\mrkl\output_parser.py` 文件的详细中文注释。该文件定义了用于解析 MRKL (ZeroShot) 代理输出的解析器。

## 核心类：`MRKLOutputParser`

该解析器负责将 LLM 生成的原始文本解析为结构化的指令对象：`AgentAction`（继续执行工具）或 `AgentFinish`（得出最终结论）。

### 1. 解析逻辑流程

1. **检查最终答案**: 查找文本中是否包含 `"Final Answer:"`。
2. **正则匹配行动**: 使用正则表达式提取 `Action:` 和 `Action Input:` 后的内容。
   - **正则模式**: `Action\s*\d*\s*:[\s]*(.*?)[\s]*Action\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)`
   - 该模式支持带有数字编号的行动标签（如 `Action 1:`）。
3. **冲突处理**: 
   - 如果同时出现了“行动指令”和“最终答案”，解析器会判断它们的先后顺序。
   - 如果“最终答案”出现在“行动指令”之前，解析器会认为模型已经得出结论，忽略后续可能的幻觉内容。
   - 否则，将抛出 `OutputParserException`，因为输出格式存在歧义。
4. **特殊处理 (SQL)**: 针对 SQL 查询，解析器会避免移除尾部的引号，以保持查询语句的完整性。

### 2. 异常处理

解析器通过抛出 `OutputParserException` 来实现自修复循环：
- **缺失行动**: 如果只有 `Thought:` 而没有 `Action:`，会返回错误消息引导模型补全。
- **缺失输入**: 如果有 `Action:` 但没有 `Action Input:`，同样会要求模型补全。
- **设置 `send_to_llm=True`**: 这意味着错误消息会被反馈给模型，让模型根据错误提示重新生成符合格式的输出。

## 关键变量

- `FINAL_ANSWER_ACTION`: `"Final Answer:"`。
- `MISSING_ACTION_AFTER_THOUGHT_ERROR_MESSAGE`: 提示模型在思考后必须给出行动指令。

## 设计意图

- **容错性**: 能够处理模型在得出结论后可能产生的“幻觉”（即模型在 `Final Answer` 之后又开始模拟工具调用）。
- **交互式修复**: 通过将解析错误回传给 LLM，利用模型自身的纠错能力来维持代理系统的稳定性。

## 关联文件

- [base.py](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/mrkl/base.md): `ZeroShotAgent` 默认使用此解析器。
- [prompt.py](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/mrkl/prompt.md): 定义了引导模型输出该格式的 `FORMAT_INSTRUCTIONS`。

