# libs\langchain\langchain_classic\agents\xml\prompt.py

此文档提供了 `libs\langchain\langchain_classic\agents\xml\prompt.py` 文件的详细中文注释。该文件定义了 XML 代理使用的默认系统指令。

## 核心常量：`agent_instructions`

这是 XML 代理的基础指令字符串，它指导模型如何以 XML 格式进行交互。

### 1. 结构化指令内容

指令包含了以下关键部分：
- **角色定义**: "You are a helpful assistant. Help the user answer any questions."
- **工具描述 (`{tools}`)**: 一个占位符，用于插入代理可调用的工具列表及其描述。
- **标签使用指南**: 明确告知模型使用以下标签：
  - `<tool>`: 指定要调用的工具名称。
  - `<tool_input>`: 提供工具所需的输入参数。
  - `<observation>`: 模型将在此标签中收到工具的执行结果（由代理执行器注入）。
  - `<final_answer>`: 任务完成时，模型应将最终答案包裹在此标签中。

### 2. 少样本示例 (Few-shot Example)

提示词中包含了一个内嵌的例子，展示了正确的交互流程：
```xml
<tool>search</tool><tool_input>weather in SF</tool_input>
<observation>64 degrees</observation>
<final_answer>The weather in SF is 64 degrees</final_answer>
```

## 技术意义与设计意图

- **明确边界**: 通过使用 XML 标签，大模型能够更清晰地界定其内部推理、工具调用动作和最终结论的边界。相比于 JSON，XML 在某些模型（如 Claude）中更具有天然的边界感，减少了输出时的转义困扰。
- **减少幻觉**: 强制要求将最终答案放在 `<final_answer>` 标签内，可以有效防止模型在得出结论前进行无意义的漫谈。
- **停止词协同**: `XMLAgent` 通常会配合停止词 `</tool_input>` 使用，这意味着模型输出完输入参数后会立即暂停，等待工具结果被插入。

## 关联文件

- [base.py](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/xml/base.md): `XMLAgent` 的 `get_default_prompt` 方法会使用此指令。
