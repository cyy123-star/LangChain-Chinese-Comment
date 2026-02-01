# libs\langchain\langchain_classic\chains\conversation\memory.py

## 文件概述

`memory.py` 在 `conversation` 模块中主要充当一个**导出层**和**兼容层**。它通过 `create_importer` 动态导入定义在 `langchain_classic.memory` 中的各种对话记忆组件。

## 导出的记忆组件

该文件集中导出了 LangChain Classic 中最常用的对话记忆类：

| 类名 | 描述 |
| :--- | :--- |
| `ConversationBufferMemory` | 基础内存缓存，存储完整的聊天记录。 |
| `ConversationBufferWindowMemory` | 窗口缓存，只保留最近 $K$ 轮对话。 |
| `ConversationSummaryMemory` | 摘要记忆，使用 LLM 对历史对话进行实时摘要。 |
| `ConversationSummaryBufferMemory` | 混合记忆，保留最近对话的缓存，同时对旧对话进行摘要。 |
| `ConversationEntityMemory` | 实体记忆，从对话中提取特定实体的信息并存储。 |
| `ConversationKGMemory` | 知识图谱记忆，将对话转化为图结构存储关系。 |
| `CombinedMemory` | 组合记忆，允许同时使用多种记忆策略。 |

## 动态导入机制

文件使用 `create_importer` 来处理弃用警告和按需导入。例如，`ConversationKGMemory` 被标记为从 `langchain_community` 导入。

```python
DEPRECATED_LOOKUP = {
    "ConversationKGMemory": "langchain_community.memory.kg",
}
```

## 注意事项

1. **导入路径**：虽然可以从 `langchain.chains.conversation.memory` 导入这些类，但更现代的做法是直接从 `langchain.memory`（或 classic 版本的对应路径）导入。
2. **状态管理**：这些记忆组件都是有状态的，在多用户环境下，必须为每个 `session_id` 创建独立的 Memory 实例。

