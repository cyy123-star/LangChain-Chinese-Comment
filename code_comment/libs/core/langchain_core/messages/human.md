# langchain_core/messages/human.py

`HumanMessage` 是 LangChain 中代表用户输入的类。它继承自 `BaseMessage`，用于封装发送给模型的人类文本或多模态内容。

## 文件概述

该文件定义了 `HumanMessage` 类及其流式分块版本 `HumanMessageChunk`。在典型的对话场景中，`HumanMessage` 用于表示终端用户的提问或指令。

## 导入依赖

| 依赖模块 | 作用 |
| :--- | :--- |
| `typing` | 提供类型注解支持（Any, Literal, cast, overload）。 |
| `langchain_core.messages.content` | 导入消息内容相关的类型定义。 |
| `langchain_core.messages.base` | 导入基类 `BaseMessage` 和 `BaseMessageChunk`。 |

## 类与函数详解

### HumanMessage

代表来自人类用户的消息。

#### 功能描述
`HumanMessage` 用于封装用户发送给聊天模型的信息。它支持纯文本内容，也支持由多个部分（如文本和图像 URL）组成的复杂内容。

#### 参数说明
| 参数名 | 类型 | 默认值 | 是否必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `content` | `str \| list[str \| dict]` | `None` | 否 | 消息的具体内容。可以是字符串，也可以是包含文本和多模态数据的列表。 |
| `content_blocks` | `list[ContentBlock]` | `None` | 否 | 显式指定内容块列表，主要用于类型提示。 |
| `**kwargs` | `Any` | - | 否 | 传递给 `BaseMessage` 的其他参数（如 `name`, `id`, `additional_kwargs` 等）。 |

#### 核心逻辑
- **初始化**：支持通过 `content` 或 `content_blocks` 进行初始化。如果提供了 `content_blocks`，它会被转换为 `content` 传递给基类。
- **类型标识**：固定 `type` 为 `"human"`，用于序列化和反序列化时的类型识别。

### HumanMessageChunk

`HumanMessage` 的流式版本。

#### 功能描述
用于在流式输出中表示人类消息的一个片段。虽然人类消息通常不是由模型流式生成的，但在某些复杂的代理（Agent）交互或回放场景中，可能需要流式表示用户输入。

#### 核心逻辑
- **类型标识**：固定 `type` 为 `"HumanMessageChunk"`，以便与其他消息块区分。

## 使用示例

```python
from langchain_core.messages import HumanMessage

# 1. 简单的纯文本消息
message = HumanMessage(content="你好，请介绍一下你自己。")
print(message.content)

# 2. 带有名称的消息
message_with_name = HumanMessage(content="这是谁发送的消息？", name="User_A")

# 3. 多模态内容示例（伪代码）
multi_modal_message = HumanMessage(content=[
    {"type": "text", "text": "这张图片里有什么？"},
    {"type": "image_url", "image_url": "https://example.com/image.jpg"}
])
```

## 注意事项

1. **类型区别**：在处理模型响应时，请确保区分 `HumanMessage`（用户输入）和 `AIMessage`（模型输出）。
2. **多模态支持**：并非所有模型都支持 `list` 类型的内容，使用多模态输入前请查阅对应模型的文档。
3. **序列化**：`type` 字段对于将消息保存到数据库或通过 API 传输至关重要。

## 内部调用关系

- `HumanMessage` 继承自 [base.py](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/core/langchain_core/messages/base.py) 中的 `BaseMessage`。
- 与 `SystemMessage` 和 `AIMessage` 共同构成对话历史的基础单元。

## 相关链接

- [LangChain 官方文档 - Messages](https://python.langchain.com/docs/concepts/messages/)
- [源码文件: langchain_core/messages/human.py](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/core/langchain_core/messages/human.py)
- [术语表: TERMINOLOGY.md](file:///d:/TraeProjects/langchain_code_comment/TERMINOLOGY.md)

---
最后更新时间: 2026-01-29
对应源码版本: LangChain Core v1.2.7
