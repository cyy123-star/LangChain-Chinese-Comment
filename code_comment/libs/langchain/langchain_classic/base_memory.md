# libs\langchain\langchain_classic\base_memory.py

此文档提供了 `libs\langchain\langchain_classic\base_memory.py` 文件的详细中文注释。该文件定义了经典 Chain 架构中用于管理状态的内存基类。

## 文件概述

在 LangChain 的经典设计中，`Memory` 组件负责维护链的状态，将过去运行的上下文（如对话历史）整合到当前的输入中。该模块包含了 v0.0.x 版本的内存抽象，目前已标记为弃用。

## 核心类：`BaseMemory` (抽象基类)

这是所有内存实现的基类，定义了内存如何与 Chain 交互的标准。

### 1. 核心方法

| 方法 | 类型 | 描述 |
| :--- | :--- | :--- |
| `memory_variables` | 属性 (抽象) | 返回该内存类将添加到链输入中的字符串键列表（例如 `["history"]`）。 |
| `load_memory_variables(inputs)` | 抽象方法 | 根据当前输入，返回需要注入到链中的键值对字典。 |
| `save_context(inputs, outputs)` | 抽象方法 | 将本次链运行的输入和输出保存到内存中（例如存储对话轮次）。 |
| `clear()` | 抽象方法 | 清空内存内容。 |

### 2. 异步支持

该类为上述所有核心方法提供了对应的异步版本（如 `aload_memory_variables`、`asave_context` 等），默认实现在执行器中运行同步版本。

---

## 迁移指南

`BaseMemory` 及其子类（如 `ConversationBufferMemory`）在 LangChain 0.3.3 中已标记为弃用，并计划在 1.0.0 版本中移除。

**官方建议迁移方向**：
- **持久化状态**：使用 [LangGraph](https://langchain-ai.github.io/langgraph/) 的 Checkpointer 机制。
- **对话历史**：使用 `langchain_core.chat_history` 中的 `BaseChatMessageHistory`。

---

## 注意事项

1. **弃用状态**: 仅为了兼容旧的 `Chain` 架构而保留。
2. **状态注入**: 内存注入的变量名必须与提示词模板（Prompt Template）中的变量名匹配。
3. **线程安全**: 默认的异步实现是简单的包装，在高并发场景下需注意具体实现的线程安全性。

