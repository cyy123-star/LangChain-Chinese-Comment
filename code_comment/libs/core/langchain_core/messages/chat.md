# libs\core\langchain_core\messages\chat.py

该模块定义了通用的聊天消息类 `ChatMessage` 及其分片版本 `ChatMessageChunk`。

## 文件概述

`chat.py` 提供了灵活性更高的消息类型。与 `HumanMessage` 或 `AIMessage` 等固定角色的消息不同，`ChatMessage` 允许用户通过 `role` 参数指定任意的角色名称。这在需要支持非标准角色（如自定义 Agent 角色）或某些特定模型的特殊角色要求时非常有用。

## 导入依赖

| 依赖模块 | 作用 |
| :--- | :--- |
| `typing` | 提供类型注解支持。 |
| `langchain_core.messages.base` | 导入基础消息类 `BaseMessage`、分片基类 `BaseMessageChunk` 以及内容合并工具 `merge_content`。 |
| `langchain_core.utils._merge` | 导入字典合并工具 `merge_dicts`。 |

## 类与函数详解

### ChatMessage 类

继承自 `BaseMessage`，代表一个带有自定义角色的消息。

- **role**: `str`，定义消息的说话者或角色（例如 "user", "assistant", "system", "moderator" 等）。
- **type**: 默认为 `"chat"`，用于序列化时的类型识别。

### ChatMessageChunk 类

继承自 `ChatMessage` 和 `BaseMessageChunk`，代表 `ChatMessage` 的增量片段，用于流式传输。

- **type**: 默认为 `"ChatMessageChunk"`。
- **__add__ 方法**:
    - **功能描述**: 实现两个消息片段的合并逻辑。
    - **核心逻辑**: 
        1. 检查 `other` 是否也是 `ChatMessageChunk`。如果是，则必须确保两者的 `role` 相同，否则抛出 `ValueError`。
        2. 使用 `merge_content` 合并 `content`。
        3. 使用 `merge_dicts` 合并 `additional_kwargs` 和 `response_metadata`。
        4. 保持原始消息的 `id`。

## 使用示例

```python
from langchain_core.messages import ChatMessage

# 创建一个带有自定义角色的消息
message = ChatMessage(role="admin", content="Hello, this is a message from admin.")

print(message.role)    # 输出: admin
print(message.content) # 输出: Hello, this is a message from admin.
```

## 注意事项

- **角色一致性**: 在进行流式数据聚合（即使用 `+` 运算符）时，系统会严格校验 `role` 是否一致。如果尝试合并两个角色不同的 `ChatMessageChunk`，会触发异常。
- **序列化**: 该类主要用于需要高度灵活性的场景。对于标准的对话流程，建议优先使用 `HumanMessage` 和 `AIMessage` 以获得更好的语义支持和模型适配。

## 内部调用关系

- `ChatMessage` 继承自 `BaseMessage`，遵循统一的消息协议。
- `ChatMessageChunk` 结合了 `ChatMessage` 的属性和 `BaseMessageChunk` 的合并能力，是流式响应处理的关键组件。

## 相关链接

- [BaseMessage 接口规范](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/core/langchain_core/messages/base.md)
- [消息类型概念指南](https://python.langchain.com/docs/concepts/messages/)

***

**最后更新时间**: 2026-01-29
**对应源码版本**: LangChain Core v1.2.7
