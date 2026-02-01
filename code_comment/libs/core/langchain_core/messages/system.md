# langchain_core/messages/system.py

`SystemMessage` 是 LangChain 中用于引导模型行为的类。它通常作为对话历史的第一条消息，向 AI 提供全局性的角色设定、任务描述或行为准则。

## 文件概述

该文件定义了 `SystemMessage` 类及其流式分块版本 `SystemMessageChunk`。它在构建聊天应用的提示词结构（Prompt Structure）中起着至关重要的作用。

## 导入依赖

| 依赖模块 | 作用 |
| :--- | :--- |
| `typing` | 提供类型注解支持（Any, Literal, cast, overload）。 |
| `langchain_core.messages.content` | 导入消息内容相关的类型定义。 |
| `langchain_core.messages.base` | 导入基类 `BaseMessage` 和 `BaseMessageChunk`。 |

## 类与函数详解

### SystemMessage

代表系统指令消息。

#### 功能描述
`SystemMessage` 用于在对话开始时“启动” AI 模型。通过系统消息，开发者可以定义 AI 的人格（如“你是一个资深的 Python 程序员”）、回答风格（如“请简洁地回答问题”）或安全约束。

#### 参数说明
| 参数名 | 类型 | 默认值 | 是否必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `content` | `str \| list[str \| dict]` | `None` | 否 | 系统指令的具体内容。 |
| `content_blocks` | `list[ContentBlock]` | `None` | 否 | 显式指定内容块列表，主要用于类型提示。 |
| `**kwargs` | `Any` | - | 否 | 其他元数据（如 `name`, `id`）。 |

#### 核心逻辑
- **初始化**：支持通过 `content` 或 `content_blocks` 进行初始化，逻辑与 `HumanMessage` 保持一致。
- **类型标识**：固定 `type` 为 `"system"`，以便模型驱动程序（Model Driver）将其正确映射为底层 API 的系统角色。

### SystemMessageChunk

`SystemMessage` 的流式版本。

#### 功能描述
用于在流式交互中表示系统消息的片段。虽然系统消息通常是一次性发送的，但该类的存在保证了 LangChain 消息体系结构的完整性和一致性。

## 使用示例

```python
from langchain_core.messages import SystemMessage, HumanMessage

# 1. 设置 AI 角色
system_msg = SystemMessage(content="你是一位专业的中英翻译官。请将用户输入的中文翻译成地道的英文。")

# 2. 与人类消息组合
messages = [
    system_msg,
    HumanMessage(content="人工智能将如何改变我们的工作方式？")
]

# 调用模型（示例）
# response = model.invoke(messages)
```

## 注意事项

1. **权重影响**：并非所有模型都对系统消息有相同的响应强度。有些模型（如早期版本）可能更倾向于遵循提示词末尾的指令。
2. **位置约定**：通常建议将 `SystemMessage` 放在对话列表的最前面。
3. **内容安全**：不要在系统消息中包含敏感的硬编码密钥，因为在某些特定的 Prompt 注入攻击下，系统消息的内容可能会被泄露给用户。

## 内部调用关系

- 继承自 [base.py](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/core/langchain_core/messages/base.py) 中的 `BaseMessage`。
- 与 `HumanMessage` 和 `AIMessage` 共同构成对话协议。

## 相关链接

- [LangChain 官方文档 - System Message](https://python.langchain.com/docs/concepts/messages/#systemmessage)
- [源码文件: langchain_core/messages/system.py](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/core/langchain_core/messages/system.py)
- [术语表: TERMINOLOGY.md](file:///d:/TraeProjects/langchain_code_comment/TERMINOLOGY.md)

---
最后更新时间: 2026-01-29
对应源码版本: LangChain Core v1.2.7
