# libs\langchain\langchain_classic\agents\conversational_chat\base.py

此文档提供了 `libs\langchain\langchain_classic\agents\conversational_chat\base.py` 文件的详细中文注释。该模块实现了专门为聊天场景设计的对话代理（Conversational Chat Agent）。

## 文件概述

`ConversationalChatAgent` 是对经典 `ConversationalAgent` 的升级，专门适配聊天模型（Chat Models）。它不再依赖于文本补全模型的推理格式，而是通过 `ChatPromptTemplate` 组织 System/Human/AI 消息，并强制模型以 JSON 格式输出。

## 核心类：`ConversationalChatAgent`

该代理继承自 `Agent` 类，旨在聊天过程中灵活使用工具。

### 1. 核心属性
- **`observation_prefix`**: `"Observation: "`。
- **`llm_prefix`**: `"Thought:"`。
- **`template_tool_response`**: 定义了如何将工具的执行结果（Observation）反馈给模型。
- **`output_parser`**: 默认使用 `ConvoOutputParser`。

### 2. 设计特点
- **纯 JSON 交互**: 与其他使用正则表达式提取 Action 的代理不同，该代理要求模型输出一个完整的 JSON 代码块。
- **记忆集成**: 提示词中包含 `chat_history` 占位符，通过 `MessagesPlaceholder` 能够完美处理多轮对话的上下文。
- **工具描述**: 工具的名称和描述被渲染到系统消息中，引导模型了解何时以及如何调用它们。

### 3. `create_prompt` 方法 (类方法)

构建适配聊天模型的提示模板。

**函数签名**:
```python
@classmethod
def create_prompt(
    cls,
    tools: Sequence[BaseTool],
    system_message: str = PREFIX,
    human_message: str = SUFFIX,
    input_variables: list[str] | None = None,
    output_parser: BaseOutputParser | None = None,
) -> BasePromptTemplate
```

**参数说明**:
| 参数 | 类型 | 描述 | 默认值 |
| :--- | :--- | :--- | :--- |
| `tools` | `Sequence[BaseTool]` | 代理可调用的工具列表。 | - |
| `system_message` | `str` | 系统提示词前缀，定义角色和工具使用规则。 | `PREFIX` |
| `human_message` | `str` | 人类消息后缀，包含格式指令和工具名称。 | `SUFFIX` |
| `input_variables` | `list[str] \| None` | 提示模板中的变量列表。 | `None` |
| `output_parser` | `BaseOutputParser \| None` | 用于解析 LLM 输出的解析器。 | `None` |

**返回**:
- `BasePromptTemplate`: 组装好的 `ChatPromptTemplate`，通常包含 `[SystemMessage, MessagesPlaceholder(variable_name='chat_history'), HumanMessage]`。

## 核心方法实现细节

### 1. `_validate_tools`
除了基类的验证外，还会调用 `validate_tools_single_input` 确保所有工具都只接受单一输入，因为 `ConvoOutputParser` 仅支持单一输入的 JSON 格式。

### 2. `observation_prefix` & `llm_prefix`
- `observation_prefix` 为 `"Observation: "`，用于在提示词中标记工具返回的结果。
- `llm_prefix` 为 `"Thought:"`，用于引导模型进行推理思考。

## 注意事项

1. **弃用说明**: 该类自 0.1.0 版本起已被弃用。
2. **现代替代方案**: 强烈建议迁移到 `create_json_chat_agent` 函数，它提供了基于 LCEL 的更灵活的实现。
3. **输出限制**: 该代理在提示词中明确要求模型“除了 JSON 代码块之外不要输出任何其他内容”。如果模型输出了一些解释性文字，解析器可能会抛出 `OutputParserException`。
4. **单输入限制**: 该代理及其解析器目前主要针对单输入的工具进行了优化。
