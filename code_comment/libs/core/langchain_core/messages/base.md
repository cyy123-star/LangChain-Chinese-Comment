# libs\core\langchain_core\messages\base.py

## 文件概述

`base.py` 定义了 LangChain 中消息（Message）的基础抽象类。消息是聊天模型（Chat Model）输入和输出的核心数据结构。与简单的字符串不同，消息对象携带了丰富的元数据，如消息类型（System, Human, AI）、角色名称、响应元数据以及用于流式处理的区块（Chunk）信息。

主要职责：
1. 定义所有消息类型的基类 `BaseMessage`。
2. 实现支持流式增量合并的消息区块基类 `BaseMessageChunk`。
3. 提供消息内容的合并逻辑 (`merge_content`)。
4. 提供向后兼容的文本访问机制 (`TextAccessor`)。

## 导入依赖

| 模块/类 | 作用 |
| :--- | :--- |
| `pydantic.BaseModel`, `Field` | 用于定义消息的数据结构、默认值及验证规则。 |
| `langchain_core.load.serializable.Serializable` | 使消息对象支持序列化，便于在网络传输或持久化存储。 |
| `langchain_core.utils._merge` | 提供字典和列表的合并工具函数，用于消息区块的合并。 |
| `langchain_core._api.deprecation` | 用于标记和处理已弃用的功能。 |

## 类与函数详解

### 1. BaseMessage

#### 功能描述
所有消息对象的抽象基类。它定义了消息的核心字段，如内容 (`content`)、类型 (`type`) 和元数据。

#### 核心属性
| 属性名 | 类型 | 默认值 | 详细用途 |
| :--- | :--- | :--- | :--- |
| `content` | `str \| list[str \| dict]` | - | 消息的具体内容。可以是纯文本，也可以是多模态内容列表（如文本+图片）。 |
| `additional_kwargs` | `dict` | `{}` | 存储模型特定的额外信息（如 OpenAI 的 tool_calls）。 |
| `response_metadata` | `dict` | `{}` | 存储响应层面的元数据（如 token 计数、模型名称、logprobs 等）。 |
| `type` | `str` | - | 消息类型的唯一标识（如 "human", "ai", "system"）。 |
| `name` | `str \| None` | `None` | 消息发送者的名称，可选。 |
| `id` | `str \| None` | `None` | 消息的唯一标识符。 |

#### 核心方法
- **`text` (Property)**: 以字符串形式返回消息的文本内容。它智能地处理纯文本和复杂的内容块列表。
- **`pretty_print()`**: 在控制台以易读的格式打印消息内容。
- **`__add__(other)`**: 支持使用 `+` 运算符将消息与另一个消息连接，返回一个 `ChatPromptTemplate`。

---

### 2. BaseMessageChunk

#### 功能描述
代表流式输出中的一个消息片段。它继承自 `BaseMessage`，并重载了 `__add__` 运算符，支持将多个片段增量合并成一个完整的消息。

- **核心逻辑**：
  使用 `merge_content` 合并内容字段，并使用 `merge_dicts` 合并 `additional_kwargs` 和 `response_metadata`。

---

### 3. merge_content (函数)

#### 功能描述
一个通用的内容合并工具函数，支持合并字符串、列表及其混合类型。

- **参数说明**
| 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `first_content` | `str \| list` | - | 是 | 第一个内容块。 |
| `*contents` | `str \| list` | - | 否 | 其他待合并的内容块。 |

---

### 4. TextAccessor

#### 功能描述
一个特殊的字符串类，旨在平滑过渡从方法调用 (`.text()`) 到属性访问 (`.text`) 的 API 变更。调用该对象会触发弃用警告。

## 核心逻辑解读

### 1. 内容块解析 (`content_blocks`)
`BaseMessage` 能够将 `content` 字段（可能是字符串或字典列表）标准化为一组 `ContentBlock` 对象。这为处理不同模型供应商（OpenAI, Anthropic, Google 等）的多模态格式提供了统一的内部表示。

### 2. 消息合并 (`Chunking`)
在流式传输中，模型会分多次返回 `BaseMessageChunk`。通过 `chunk1 + chunk2`，LangChain 能够自动处理文本拼接、字典合并等复杂操作，最终还原成完整的响应。

## 使用示例

```python
from langchain_core.messages import HumanMessage, AIMessage

# 创建消息
msg = HumanMessage(content="你好", name="Alice")

# 访问文本
print(msg.text)  # 输出: 你好

# 消息组合
ai_msg = AIMessage(content="你好！有什么我可以帮你的吗？")
combined = msg + ai_msg
# combined 现在是一个包含两条消息的 ChatPromptTemplate
```

## 注意事项

1. **内容类型**：`content` 字段可能不只是字符串。在编写处理逻辑时，建议使用 `.text` 属性或检查是否为列表。
2. **序列化**：由于继承自 `Serializable`，消息对象可以通过 `.dict()` 或 `.json()` 进行序列化，但需注意 `additional_kwargs` 中的复杂对象。
3. **弃用警告**：避免使用 `message.text()` 这种函数调用方式，应直接使用 `message.text` 属性。

## 内部调用关系

- `BaseMessage` 被 `HumanMessage`, `AIMessage`, `SystemMessage` 等具体类继承。
- `BaseMessageChunk` 被对应的 Chunk 类（如 `AIMessageChunk`）继承。
- `ChatPromptTemplate` 在执行消息加法时被引入。

## 相关链接

- [LangChain 官方文档 - Messages](https://python.langchain.com/docs/modules/model_io/chat/messages/)
- [源码文件: langchain_core/messages/base.py](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/core/langchain_core/messages/base.py)
- [术语表: TERMINOLOGY.md](file:///d:/TraeProjects/langchain_code_comment/TERMINOLOGY.md)

---
最后更新时间: 2026-01-29
对应源码版本: LangChain Core v1.2.7
