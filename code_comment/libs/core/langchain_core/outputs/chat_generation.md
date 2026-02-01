# libs\core\langchain_core\outputs\chat_generation.py

## 文件概述

`chat_generation.py` 定义了聊天模型（Chat Model）生成的输出结构。它是 `Generation` 的子类，专门用于处理结构化的聊天消息（`BaseMessage`），支持多模态内容提取和流式分片合并。

## 导入依赖

- `langchain_core.messages.BaseMessage`: 聊天消息的基础类。
- `langchain_core.messages.BaseMessageChunk`: 聊天消息分片的基础类。
- `langchain_core.outputs.generation.Generation`: 基础生成类。
- `langchain_core.utils._merge.merge_dicts`: 字典合并工具。

## 类与函数详解

### 1. ChatGeneration
- **功能描述**: 表示聊天模型的单次生成输出。
- **参数说明**:
| 参数名 | 类型 | 默认值 | 是否必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `text` | `str` | `""` | 否 | 消息的文本内容（由 `message` 自动提取，不应直接设置）。 |
| `message` | `BaseMessage` | - | 是 | 聊天模型生成的完整消息对象（如 `AIMessage`）。 |
| `type` | `Literal["ChatGeneration"]` | `"ChatGeneration"` | 否 | 序列化类型标识。 |

- **核心逻辑**:
  - `set_text` (Validator): 在初始化后运行，从 `message.content` 中提取文本。支持字符串内容和列表形式的多模态内容（提取第一个文本块）。

### 2. ChatGenerationChunk
- **功能描述**: `ChatGeneration` 的分片版本，用于流式响应。支持与其他分片或分片列表进行拼接。
- **核心逻辑**:
  - `__add__`: 实现分片拼接。如果 `other` 是列表，则批量合并；如果是单个对象，则直接合并消息和元数据。

### 3. merge_chat_generation_chunks
- **功能描述**: 将 `ChatGenerationChunk` 列表合并为单个 `ChatGenerationChunk`。
- **参数说明**:
| 参数名 | 类型 | 默认值 | 是否必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `chunks` | `list[ChatGenerationChunk]` | - | 是 | 待合并的分片列表。 |
- **返回值**: 合并后的单个 `ChatGenerationChunk`，若列表为空则返回 `None`。

## 使用示例

```python
from langchain_core.messages import AIMessage, AIMessageChunk
from langchain_core.outputs import ChatGeneration, ChatGenerationChunk

# 创建聊天生成结果
msg = AIMessage(content="Hello!")
chat_gen = ChatGeneration(message=msg)
print(chat_gen.text)  # 输出: "Hello!"

# 流式分片合并
chunk1 = ChatGenerationChunk(message=AIMessageChunk(content="Hello"))
chunk2 = ChatGenerationChunk(message=AIMessageChunk(content=" world"))
merged = chunk1 + chunk2
print(merged.message.content)  # 输出: "Hello world"
```

## 注意事项

- **禁止直接设置 `text`**: `text` 属性由 `set_text` 验证器根据 `message` 自动计算，直接设置可能会被覆盖。
- **多模态支持**: `set_text` 能够智能识别内容列表中的文本块，跳过思考（thinking）或推理（reasoning）等非文本块。

---
最后更新时间: 2026-01-29
对应源码版本: LangChain Core v1.2.7
