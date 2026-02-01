# BaseMemory (存储基类)

`BaseMemory` 是 LangChain Classic 中所有记忆组件的抽象基类。记忆组件的主要职责是**维护 Chain 的状态**，使得应用能够“记住”之前的交互信息。

## 核心职责

1. **读取上下文**: 在 Chain 运行前，从存储中提取历史信息并注入到输入变量中。
2. **保存上下文**: 在 Chain 运行后，将本次的输入和输出保存到存储中。
3. **状态清理**: 提供重置或清除历史记录的能力。

## 关键方法

| 方法 | 说明 |
| :--- | :--- |
| `load_memory_variables(inputs)` | **必须实现**。根据当前输入，返回需要注入到提示词中的历史变量。 |
| `save_context(inputs, outputs)` | **必须实现**。将当前的输入和输出持久化。 |
| `clear()` | 清除所有存储的内容。 |
| `memory_variables` | 属性。定义该 Memory 会向提示词中注入哪些键名（如 `chat_history`）。 |

## 工作流 (在 Chain 中)

1. **准备阶段**: Chain 调用 `load_memory_variables`。
2. **混合阶段**: 将返回的变量（如历史对话）与用户当前的输入合并。
3. **执行阶段**: LLM 根据完整的上下文生成响应。
4. **保存阶段**: Chain 调用 `save_context`，将本次对话存入 Memory。

## 常见子类

- `ConversationBufferMemory`: 简单地存储所有原始对话文本。
- `ConversationSummaryMemory`: 使用 LLM 对历史对话进行定期总结。
- `ConversationTokenBufferMemory`: 根据 Token 限制保留最近的对话。
- `VectorStoreRetrieverMemory`: 将对话存入向量数据库，通过语义检索相关历史。

## 迁移指南

现代 LangChain (v0.2+) 推荐使用以下方案替代传统的 `BaseMemory`：
1. **`RunnableWithMessageHistory`**: 配合 LCEL 使用，支持更灵活的持久化后端。
2. **LangGraph State**: 在图中显式管理状态，支持更复杂的“多轮对话”和“分支逻辑”。
3. **外部数据库**: 直接将消息持久化到 Redis, MongoDB 或 Postgres 中。
