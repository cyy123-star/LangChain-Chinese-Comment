# Chain 基类

`Chain` 是 LangChain Classic 中所有链式组件的抽象基类。它定义了组件之间如何组合、如何管理状态（Memory）以及如何处理回调（Callbacks）。

> **注意**: 现代 LangChain 推荐使用 **LCEL (LangChain Expression Language)**。`Chain` 类现在继承自 `RunnableSerializable`，这意味着所有的 Classic Chain 都可以像 LCEL 组件一样通过 `.invoke()`, `.batch()`, `.stream()` 调用。

## 核心职责

1. **有状态执行**: 通过集成的 `Memory` 对象，自动在执行前后加载和保存对话状态。
2. **可观察性**: 自动触发回调系统，支持日志记录、监控和调试。
3. **组合性**: 提供统一的接口，使得链可以嵌套调用（例如 `SequentialChain`）。

## 关键方法

| 方法 | 说明 |
| :--- | :--- |
| `invoke(input)` | 现代调用接口。内部会自动处理 `Memory` 和 `Callbacks`。 |
| `__call__(inputs)` | 传统调用接口（已弃用）。接收字典输入，返回字典输出。 |
| `run(*args, **kwargs)` | 便捷调用方法。返回单个输出值（通常是字符串），不支持多输出。 |
| `_call(inputs)` | **必须实现**。子类在此定义核心业务逻辑。 |

## 生命周期

一次 `invoke` 调用的简化流程如下：

1. **准备阶段**: 
   - 合并全局配置（Tags, Metadata, Callbacks）。
   - 如果有 `Memory`，调用 `memory.load_memory_variables` 将历史数据混入输入。
2. **执行阶段**:
   - 触发 `on_chain_start` 回调。
   - 调用子类实现的 `_call` 或 `_acall`。
3. **收尾阶段**:
   - 如果有 `Memory`，调用 `memory.save_context` 保存当前的输入和输出。
   - 触发 `on_chain_end` 或 `on_chain_error` 回调。

## 核心属性

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `memory` | `Optional[BaseMemory]` | 关联的存储对象。 |
| `callbacks` | `Callbacks` | 回调管理器或处理列表。 |
| `verbose` | `bool` | 是否开启详细日志模式（打印中间步骤）。 |

## 开发者指南

当实现自定义 Chain 时：
- 继承 `Chain` 类。
- 定义 `input_keys` 和 `output_keys` 属性。
- 实现 `_call`（同步）和 `_acall`（异步）方法。
