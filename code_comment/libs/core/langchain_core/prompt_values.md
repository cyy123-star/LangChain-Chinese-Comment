# prompt_values.py - 提示词对象

- **最后更新时间**: 2026-01-29
- **对应源码版本**: LangChain Core v1.2.7

## 文件概述

`prompt_values.py` 定义了所有语言模型输入的统一抽象接口。它允许在纯文本模型（LLMs）和聊天模型（Chat Models）之间无缝转换提示词。

## 导入依赖

| 模块 | 作用 |
| :--- | :--- |
| `abc.ABC, abstractmethod` | 提供抽象基类支持。 |
| `langchain_core.load.serializable.Serializable` | 使提示词对象支持序列化。 |
| `langchain_core.messages` | 包含基础消息类及转换工具（如 `get_buffer_string`）。 |

## 类与函数详解

### 1. PromptValue (抽象基类)
- **功能描述**: 所有语言模型输入的基类。它定义了将提示词转换为不同格式的契约。
- **核心方法**:
  - `to_string()`: **抽象方法**。将提示词转换为单条字符串。
  - `to_messages()`: **抽象方法**。将提示词转换为 `BaseMessage` 对象列表。

### 2. StringPromptValue
- **功能描述**: 代表一个简单的字符串提示词。
- **参数说明**:
  | 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
  | :--- | :--- | :--- | :--- | :--- |
  | `text` | `str` | - | 是 | 提示词的原始文本。 |
- **核心逻辑**:
  - `to_string()`: 直接返回 `text`。
  - `to_messages()`: 返回包含单个 `HumanMessage` 的列表，内容为 `text`。

### 3. ChatPromptValue
- **功能描述**: 代表由一系列消息构成的聊天提示词。
- **参数说明**:
  | 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
  | :--- | :--- | :--- | :--- | :--- |
  | `messages` | `Sequence[BaseMessage]` | - | 是 | 消息序列。 |
- **核心逻辑**:
  - `to_string()`: 使用 `get_buffer_string` 将所有消息的内容拼接成一个长字符串（通常用于将聊天记录喂给非聊天模型）。
  - `to_messages()`: 直接返回 `messages` 列表。

## 核心逻辑

- **统一抽象**: `PromptValue` 的存在是 LangChain 能够兼容不同类型模型的核心。`PromptTemplate` 生成 `PromptValue` 后，下游组件（如 LLM 或 ChatModel）可以根据自身需求调用 `to_string()` 或 `to_messages()`，从而实现“一次定义，多处运行”。
- **序列化**: 所有 `PromptValue` 实现都标记为 `is_lc_serializable`，这意味着它们可以被序列化为 JSON 格式，方便在分布式系统中传输或持久化存储。

## 使用示例

```python
from langchain_core.prompt_values import StringPromptValue, ChatPromptValue
from langchain_core.messages import HumanMessage, SystemMessage

# 处理字符串提示词
spv = StringPromptValue(text="解释一下量子纠缠")
print(spv.to_string()) 
# 输出: "解释一下量子纠缠"

# 处理聊天提示词
cpv = ChatPromptValue(messages=[
    SystemMessage(content="你是一个物理学家"),
    HumanMessage(content="解释一下量子纠缠")
])
print(cpv.to_string()) 
# 输出: "System: 你是一个物理学家\nHuman: 解释一下量子纠缠"
```

## 注意事项

- **命名空间**: 该类在 LangChain 序列化系统中的命名空间被固定为 `["langchain", "schema", "prompt"]`，以确保跨版本的兼容性。

## 相关链接
- [LangChain 概念文档 - 提示词 (Prompts)](https://python.langchain.com/docs/concepts/#prompts)
- [langchain_core.messages](file:///d%3A/TraeProjects/langchain_code_comment/code_comment/libs/core/langchain_core/messages/base.md)
