# libs\langchain\langchain_classic\agents\conversational\prompt.py

此文档提供了 `libs\langchain\langchain_classic\agents\conversational\prompt.py` 文件的详细中文注释。该模块定义了 `ConversationalAgent` 使用的提示词模板常量。

## 文件概述

对话式代理需要处理复杂的上下文。该模块提供的模板旨在引导 LLM 在对话环境中平衡“使用工具”和“直接回复”这两种行为。它通过清晰的结构（PREFIX, FORMAT_INSTRUCTIONS, SUFFIX）来定义代理的行为准则。

## 核心常量

### 1. `PREFIX`
- **内容**: 详细描述了助理（Assistant）的角色定位。
- **作用**: 设定助理为一个由 OpenAI 训练的大型语言模型，具备广泛的任务处理能力、深入的解释能力和自然的对话风格。强调其能够不断学习和提供准确信息的特质。

### 2. `FORMAT_INSTRUCTIONS`
- **内容**: 规定了决策逻辑。
- **关键逻辑**:
    - **工具调用模式**: 如果需要使用工具，必须遵循 `Thought` -> `Action` -> `Action Input` -> `Observation` 的格式。
    - **直接回复模式**: 如果不需要工具或准备好回答人类，必须使用 `{ai_prefix}: [回答内容]` 的格式。
- **变量**: 包含 `{tool_names}` 和 `{ai_prefix}` 的占位符，以便动态注入。

### 3. `SUFFIX`
- **内容**: 拼接当前任务的上下文。
- **结构**:
    1. **Previous conversation history**: 注入 `{chat_history}`。
    2. **New input**: 注入当前的 `{input}`。
    3. **Scratchpad**: 注入 `{agent_scratchpad}`。
- **作用**: 将长期记忆（历史记录）与短期记忆（当前思考过程）整合在一起。

## 设计意图

- **拟人化引导**: 通过 `PREFIX` 中的长篇描述，赋予代理一个专业且友好的“人格”，有助于提升回复的质量。
- **强规则约束**: 在 `FORMAT_INSTRUCTIONS` 中使用 "MUST"（必须）等强语气词，确保模型在“思考”和“行动”之间有明确的界限。
- **无缝集成历史**: 通过 `SUFFIX` 中的结构化布局，使得代理在处理新输入时能够自然地回溯之前的对话，从而实现多轮对话的连贯性。

## 关联文件

- [base.py](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/conversational/base.md): `ConversationalAgent` 加载这些常量并进行变量填充。
- [output_parser.py](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/conversational/output_parser.md): 解析器根据这里定义的格式规则进行文本拆分。

