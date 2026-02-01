# libs\langchain\langchain_classic\agents\chat\prompt.py

此文档提供了 `libs\langchain\langchain_classic\agents\chat\prompt.py` 文件的详细中文注释。该模块定义了 `ChatAgent` 使用的提示词模板常量。

## 文件概述

为了让聊天模型能够稳定地以 ReAct 模式工作，需要非常精确的指令引导。该模块集中管理了这些指令模板，包括系统消息的前缀、格式化指南、后缀以及人类消息的结构。

## 核心常量

### 1. `SYSTEM_MESSAGE_PREFIX`
- **内容**: "Answer the following questions as best you can. You have access to the following tools:"
- **作用**: 设定代理的角色，并告知其拥有的工具能力。

### 2. `FORMAT_INSTRUCTIONS`
- **内容**: 详细定义了 JSON 交互的协议。
- **关键约束**:
    - **JSON 结构**: 必须包含 `action`（工具名）和 `action_input`（工具输入）。
    - **单一动作**: 明确告知 `$JSON_BLOB` 只能包含一个动作，不能是列表。
    - **示例引导**: 提供了一个 JSON 示例块。
    - **流程规范**: 强制要求遵循 `Question` -> `Thought` -> `Action (JSON)` -> `Observation` -> ... -> `Final Answer` 的固定顺序。

### 3. `SYSTEM_MESSAGE_SUFFIX`
- **内容**: "Begin! Reminder to always use the exact characters `Final Answer` when responding."
- **作用**: 触发模型开始执行，并最后一次提醒必须使用 `Final Answer` 关键字来结束任务。

### 4. `HUMAN_MESSAGE`
- **内容**: `"{input}\n\n{agent_scratchpad}"`
- **变量**:
    - `{input}`: 用户输入的原始问题。
    - `{agent_scratchpad}`: 代理的思考历史和工具调用结果。

## 设计意图

- **结构化对话**: 聊天模型通常在结构化消息（System/Human/AI）中表现更好。该模块将 ReAct 逻辑嵌入到这些消息类型中。
- **减少解析错误**: 通过显式的 JSON 示例和格式约束，降低了 LLM 生成非法格式的可能性。
- **强化关键字**: 重复强调 `Final Answer`，确保 `ChatOutputParser` 能够准确识别任务何时完成。

## 关联文件
- [base.py](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/chat/base.md): `ChatAgent` 类加载并使用这些常量。
- [output_parser.py](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/chat/output_parser.md): 解析器根据 `FORMAT_INSTRUCTIONS` 定义的规则进行文本提取。

