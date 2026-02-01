# libs\core\langchain_core\prompts\chat.py

## 文件概述
`chat.py` 定义了专门用于聊天模型的提示词模板类。与传统的单一字符串模板不同，聊天模板由一系列消息（Messages）组成，每条消息都有明确的角色（如系统、人类、AI）。该模块提供了 `ChatPromptTemplate` 及其相关的消息模板类，支持灵活的消息组合、占位符处理以及多模态内容渲染。

## 导入依赖
- `langchain_core.messages`: 导入基础消息类（`BaseMessage`, `HumanMessage`, `AIMessage` 等）及其转换工具。
- `langchain_core.prompts.base`: 导入 `BasePromptTemplate`。
- `langchain_core.prompts.prompt`: 导入 `PromptTemplate` 用于处理消息内容中的字符串格式化。
- `langchain_core.prompts.image`: 支持图像内容的提示词模板。

## 类与函数详解

### MessagesPlaceholder
`MessagesPlaceholder` 是一个特殊的占位符，用于在模板中动态插入一个消息列表（通常用于对话历史）。

- **属性**:
  - `variable_name`: 变量名，用于在 `format` 时从输入字典中查找消息列表。
  - `optional`: 是否可选。如果为 `True`，未提供该变量时将返回空列表，而不是抛出错误。
  - `n_messages`: 限制包含的消息数量（仅保留最后 N 条）。

### ChatPromptTemplate
`ChatPromptTemplate` 是用于聊天模型的主要提示词模板类。它维护一个消息模板列表，并负责将输入变量分发到各个模板中。

#### 核心方法

##### from_messages (classmethod)
- **功能描述**: 从多种格式的消息表示中创建聊天模板。这是最常用的实例化方法。
- **参数说明**:
  - `messages`: 消息序列。支持元组 `(role, template)`、`BaseMessage` 对象、字符串（默认为 human）等。
  - `template_format`: 模板语法（默认 `"f-string"`）。
- **返回值**: `ChatPromptTemplate` 实例。

##### format_messages
- **功能描述**: 将输入变量填充到所有内部消息模板中，生成最终的 `BaseMessage` 列表。
- **参数说明**:
  - `**kwargs`: 模板变量键值对。
- **返回值**: `list[BaseMessage]`。

##### __add__ (operator override)
- **功能描述**: 允许通过 `+` 运算符组合两个聊天模板，或向聊天模板添加新消息。

### 具体的各种消息模板类
- `HumanMessagePromptTemplate`: 生成 `HumanMessage` 的模板。
- `AIMessagePromptTemplate`: 生成 `AIMessage` 的模板。
- `SystemMessagePromptTemplate`: 生成 `SystemMessage` 的模板。
- `ChatMessagePromptTemplate`: 生成带有自定义角色（Role）的 `ChatMessage` 的模板。

## 核心逻辑
1. **消息转换**: 在初始化阶段，使用 `_convert_to_message_template` 内部函数将用户提供的元组或字符串统一转换为 `BaseMessagePromptTemplate` 对象。
2. **变量推断**: 自动从所有内部消息模板中推断出总的 `input_variables`，并处理 `optional_variables`（如 `MessagesPlaceholder`）。
3. **内容渲染**: 消息模板支持纯文本和多模态内容（如图像）。如果是列表形式的内容，会逐个处理并生成符合模型要求的结构化数据。

## 使用示例

```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 1. 使用元组定义聊天结构
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个名叫 {name} 的 AI 助手。"),
    MessagesPlaceholder("history"),
    ("human", "{question}")
])

# 2. 格式化生成消息列表
messages = prompt.format_messages(
    name="小智",
    history=[("human", "你好"), ("ai", "你好！有什么我可以帮你的？")],
    question="今天天气如何？"
)

# 3. 模板拼接
full_prompt = prompt + ("ai", "我会尽力回答你的问题。")
```

## 注意事项
- **单变量调用**: 如果模板仅包含一个变量，可以直接传入该变量的值（非字典对象），系统会自动映射。
- **多模态支持**: `HumanMessagePromptTemplate` 支持包含 `image_url` 的列表格式模板，用于视觉模型。
- **类型安全**: `ChatPromptTemplate` 会根据 `MessagesPlaceholder` 自动更新 `input_types`，以便在链式调用中进行类型检查。

## 内部调用关系
- **继承体系**: 继承自 `BaseChatPromptTemplate` -> `BasePromptTemplate` -> `RunnableSerializable`。
- **组合关系**: `ChatPromptTemplate` 内部持有一个 `BaseMessagePromptTemplate` 列表。
- **格式化**: 依赖 `PromptTemplate` 处理具体消息内容中的占位符填充。

## 相关链接
- [LangChain 官方文档 - Chat Prompt Templates](https://python.langchain.com/docs/concepts/prompt_templates/#chatprompttemplate)
- [LangChain 核心概念 - Messages](https://python.langchain.com/docs/concepts/messages/)

---
最后更新时间: 2026-01-29
对应源码版本: LangChain Core v1.2.7