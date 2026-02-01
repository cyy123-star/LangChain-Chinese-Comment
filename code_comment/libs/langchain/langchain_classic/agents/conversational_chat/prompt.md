# libs\langchain\langchain_classic\agents\conversational_chat\prompt.py

此文档提供了 `libs\langchain\langchain_classic\agents\conversational_chat\prompt.py` 文件的详细中文注释。该模块定义了对话聊天代理使用的结构化提示词模板。

## 核心常量

### 1. `PREFIX`
系统消息的前缀。它将 Assistant 定义为一个由 OpenAI 训练的大型语言模型，强调其知识广泛、能够生成类人文本并进行自然对话。

### 2. `FORMAT_INSTRUCTIONS`
详细规定了模型必须遵守的 JSON 响应格式。
- **选项 1 (调用工具)**: 
  ```json
  {
    "action": "工具名称",
    "action_input": "输入内容"
  }
  ```
- **选项 2 (直接回答)**:
  ```json
  {
    "action": "Final Answer",
    "action_input": "回答内容"
  }
  ```

### 3. `SUFFIX`
系统消息的后缀。它列出了可用的工具列表，并包含 `USER'S INPUT` 引导。最关键的是，它再次强调：模型必须输出且仅输出一个 JSON 代码块，不能有其他多余文字。

### 4. `TEMPLATE_TOOL_RESPONSE`
当工具执行完毕并返回结果（Observation）时使用的模板。它会告知模型工具的响应内容，并再次提醒模型以 JSON 格式回复。

## 设计意图

该提示词的设计旨在消除模型在对话过程中的“幻觉”和格式不一致。通过强制所有输出都必须通过 JSON 结构化，它确保了 `AgentExecutor` 能够百分之百准确地捕获模型的意图，无论是继续对话还是调用外部工具。

## 注意事项

1. **JSON 闭环**: 该提示词不给模型留任何输出自然语言的空间，除非是在 JSON 的 `action_input` 字段内。这虽然增加了鲁棒性，但也可能限制了模型输出的一些自然感。
2. **工具名称占位符**: `{tool_names}` 会在运行时被替换为实际工具的名称。
3. **记忆引用**: 在 `TEMPLATE_TOOL_RESPONSE` 中，特别提醒模型“我已经忘记了所有工具响应”，强制模型在最终回答中显式引用之前获得的信息。
