# LangChain 消息工具库 (Message Utils) 规范

## 文件概述

`utils.py` 是 LangChain 消息处理的核心工具库。它提供了大量用于处理、转换、过滤和修剪消息的实用函数。无论是将消息序列化为字符串、从字典转换回消息对象，还是根据复杂的规则（如令牌数量、消息类型等）对对话历史进行修剪和过滤，该模块都提供了标准的实现。

该文件是构建鲁棒的聊天应用、代理（Agents）和复杂链（Chains）的基石。

---

## 导入依赖

该文件依赖较多，主要包括：
- `typing`: 丰富的类型注解支持。
- `pydantic`: 用于数据校验和判别式（Discriminator）定义。
- `langchain_core.messages`: 导入所有核心消息类型（`AIMessage`, `HumanMessage`, `SystemMessage`, `ToolMessage` 等）。
- `langchain_core.runnables`: 提供 `_runnable_support` 装饰器，使工具函数可以直接作为 Runnable 使用。

---

## 类与函数详解

### 1. 核心转换函数

#### `get_buffer_string`
**功能描述**: 将消息序列（`Sequence[BaseMessage]`）转换为一个连续的字符串，常用于将对话历史喂给仅支持字符串输入的旧版 LLM。

| 参数 | 类型 | 默认值 | 详细用途 |
| :--- | :--- | :--- | :--- |
| `messages` | `Sequence[BaseMessage]` | - | 要转换的消息列表。 |
| `human_prefix` | `str` | "Human" | 人类消息的前缀。 |
| `ai_prefix` | `str` | "AI" | AI 消息的前缀。 |
| `format` | `Literal["prefix", "xml"]` | "prefix" | 输出格式。`xml` 格式能更好地处理包含特殊字符或角色伪造的内容。 |

#### `convert_to_messages`
**功能描述**: 万能转换器。可以将字符串、字典、元组或 `PromptValue` 转换为标准的 `BaseMessage` 列表。

#### `messages_from_dict` / `_message_from_dict`
**功能描述**: 从序列化后的字典结构中恢复消息对象（反序列化）。

---

### 2. 消息操作函数 (支持 Runnable)

这些函数被 `@_runnable_support` 装饰，意味着它们既可以作为普通函数调用，也可以在 LCEL 链中通过 `|` 组合。

#### `filter_messages`
**功能描述**: 根据名称、类型、ID 或是否包含工具调用来过滤消息列表。支持 `include` 和 `exclude` 两种模式。

#### `merge_message_runs`
**功能描述**: 合并连续的同类型消息。例如，如果历史中有连续两条 `HumanMessage`，它们会被合并成一条，内容以换行符分隔。

#### `trim_messages`
**功能描述**: **（极重要）** 根据 Token 计数器修剪对话历史。用于确保发送给模型的上下文不会超出其窗口限制。支持从开头（`first`）或末尾（`last`）开始修剪，并能保证修剪后的历史以特定类型的消息（如 `HumanMessage`）开始。

---

### 3. 类型定义

- **`AnyMessage`**: 使用 Pydantic 的 `Discriminator` 定义的联合类型，涵盖了所有已知消息及其块变体。
- **`MessageLikeRepresentation`**: 定义了消息的各种表现形式（字符串、字典、元组等），用于函数参数的灵活适配。

---

## 核心逻辑

1. **LCEL 集成**: 通过 `_runnable_support`，所有主要的工具函数都可以无缝集成到 LangChain 表达式语言中。
2. **多模态支持**: `_format_content_block_xml` 展示了如何处理多模态内容块（图像、音频等），将其安全地转换为 XML 表示。
3. **鲁棒性**: 在处理消息合并和转换时，考虑了 `tool_calls` 的特殊性（如 `ToolMessage` 不可合并以保持 ID 关联）。

---

## 使用示例

### 1. 过滤消息
```python
from langchain_core.messages import filter_messages, HumanMessage, AIMessage

messages = [
    HumanMessage("你好", name="user_1"),
    AIMessage("你好！有什么可以帮你的？", name="bot_1")
]

# 仅保留 AI 的回复
ai_only = filter_messages(messages, include_types=["ai"])
```

### 2. 修剪对话历史 (LCEL)
```python
from langchain_core.messages import trim_messages
from langchain_openai import ChatOpenAI

# 创建一个修剪器，保留最后 1000 个 token
trimmer = trim_messages(
    max_tokens=1000,
    strategy="last",
    token_counter=ChatOpenAI(model="gpt-4o"),
    start_on="human",
    include_system=True
)

# 在链中使用
chain = trimmer | model
```

---

## 注意事项

- **Token 计数**: `trim_messages` 的准确性高度依赖于传入的 `token_counter`。建议使用目标模型的 `get_num_tokens_from_messages` 方法。
- **XML 转义**: 使用 `format="xml"` 时，内容会自动进行转义，这对于防止“提示词注入”或处理包含代码的内容非常有效。
- **不可变性**: 大多数操作返回的是消息的新拷贝或新列表，不会修改原始输入。

---

## 内部调用关系

- **`BaseMessage` 子类**: `utils.py` 是这些子类的汇集点，负责它们之间的转换和协调。
- **`LangChain Runnables`**: 工具函数通过装饰器与 Runnable 框架深度集成。
- **`Prompt Templates`**: 提示词模板在生成最终消息列表时，常调用 `convert_to_messages`。

---

## 相关链接

- [LangChain 官方文档 - 消息处理](https://python.langchain.com/docs/how_to/trim_messages/)
- [LangChain 概念指南 - 消息](https://python.langchain.com/docs/concepts/messages/)

---

**最后更新时间**: 2026-01-29
**对应源码版本**: LangChain Core v1.2.7
