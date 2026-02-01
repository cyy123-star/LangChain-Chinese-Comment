# Memory (记忆组件实现)

`memory` 模块实现了多种用于在对话中保持状态的策略。它不仅定义了如何处理历史记录，还提供了与各种数据库集成的后端实现。

## 记忆策略 (Memory Strategies)

| 策略 | 说明 |
| :--- | :--- |
| `ConversationBufferMemory` | 简单地将所有原始对话历史存储在内存中。 |
| `ConversationBufferWindowMemory` | 仅保留最近的 K 轮对话，防止上下文窗口溢出。 |
| `ConversationSummaryMemory` | 使用 LLM 实时对对话进行摘要，适合极长对话。 |
| `ConversationSummaryBufferMemory` | 结合了 Buffer 和 Summary，保留最近的原始对话并摘要更早的历史。 |
| `ConversationTokenBufferMemory` | 根据 Token 数量限制保留最近的对话。 |
| `VectorStoreRetrieverMemory` | 将历史对话存入向量数据库，按语义检索最相关的片段。 |
| `ConversationKGMemory` | 基于知识图谱提取实体及其关系来存储记忆。 |

## 消息历史后端 (Chat Message Histories)

`chat_message_histories` 子模块提供了将消息持久化到各种数据库的能力：
- **内存**: `ChatMessageHistory` (默认)。
- **关系型数据库**: `PostgresChatMessageHistory`, `SQLChatMessageHistory`。
- **NoSQL**: `RedisChatMessageHistory`, `MongoDBChatMessageHistory`, `DynamoDBChatMessageHistory`。
- **云原生**: `CosmosDBChatMessageHistory`, `FirestoreChatMessageHistory`。

## 使用示例

```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(memory_key="chat_history")
memory.save_context({"input": "hi"}, {"output": "whats up"})

# 加载变量
vars = memory.load_memory_variables({})
# {'chat_history': 'Human: hi\nAI: whats up'}
```

## 迁移指南

- **集成分离**: 绝大多数具体的数据库后端实现现在都位于 `langchain-community` 中。
- **现代方案**: 推荐使用 `RunnableWithMessageHistory` 配合 LCEL 进行状态管理。
- **LangGraph**: 对于复杂的代理应用，建议使用 LangGraph 的 `checkpointer` 机制实现生产级的状态持久化和“时间旅行”功能。
