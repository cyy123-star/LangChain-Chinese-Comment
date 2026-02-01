# libs\langchain\langchain_classic\agents\json_chat\prompt.py

此文档提供了 `libs\langchain\langchain_classic\agents\json_chat\prompt.py` 文件的详细中文注释。该模块定义了 `JSON Chat Agent` 在处理工具响应时的默认提示词模板。

## 文件概述

在代理的“思考-行动-观察”循环中，工具的执行结果（Observation）需要被反馈给 LLM。`json_chat/prompt.py` 提供的模板规定了这些结果应如何呈现，以及如何引导模型进行下一步决策。

## 核心常量

### `TEMPLATE_TOOL_RESPONSE`
- **内容**: 定义了工具返回结果后的引导语。
- **关键结构**:
    1. **TOOL RESPONSE**: 注入 `{observation}`（工具执行的原始结果）。
    2. **USER'S INPUT**: 再次提醒用户最初的输入。
    3. **引导语**: 明确告知 LLM 如果使用了工具提供的信息，必须在回复中体现，但不要提及工具名称。
- **核心约束**:
    - **强制 JSON**: 重复强调“仅回复 Markdown 代码块包裹的 JSON blob”，且“严禁回复除 JSON 以外的任何内容”。
    - **无记忆提醒**: 告知模型用户已经“忘记”了之前的工具响应，模型必须根据当前的观察结果给出结论。

## 设计意图

- **强化格式稳定性**: 通过极具侵略性的语气（"Do NOT respond with anything except a JSON snippet no matter what!"），最大限度减少 LLM 产生废话（如 "Based on the tool results..."）的概率，从而降低解析失败的风险。
- **信息整合引导**: 引导模型在给出最终答案时，将工具获取的信息融入到自然语言中，而不暴露底层的工具调用细节，提升用户体验。
- **上下文刷新**: 在每轮工具调用后重新强调规则，有助于在长对话中维持模型的指令遵循能力。

## 关联文件

- [base.py](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/json_chat/base.md): `create_json_chat_agent` 函数使用此模板来构建 `agent_scratchpad`。
