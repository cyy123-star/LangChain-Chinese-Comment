# libs\langchain\langchain_classic\chains\base.py

此文档提供了 `libs\langchain\langchain_classic\chains\base.py` 文件的详细中文注释。该文件定义了 LangChain 经典链（Chain）的基础抽象接口。

## 文件概述

`Chain` 是 LangChain 早期架构的核心概念，用于将多个组件（如 LLM、提示词、内存、工具等）连接成一个执行序列。虽然现在推荐使用 LCEL (LangChain Expression Language)，但 `Chain` 类仍然广泛存在于旧代码库中。

## 核心类：`Chain`

所有链的抽象基类。它继承自 `RunnableSerializable`，因此也支持现代的 `invoke`, `stream`, `batch` 等方法。

### 1. 核心特性

- **有状态性 (Stateful)**: 支持集成 `BaseMemory` 来持久化对话状态。在链开始时加载变量，结束时保存变量。
- **可观察性 (Observable)**: 支持集成 `Callbacks` 来监控链的生命周期（开始、结束、错误等）。
- **详细模式 (Verbose)**: 开启 `verbose=True` 时，会输出执行过程中的中间日志。

### 2. 关键参数

| 参数 | 类型 | 描述 |
| :--- | :--- | :--- |
| `memory` | `BaseMemory \| None` | 可选的记忆对象。 |
| `callbacks` | `Callbacks` | 回调处理器或管理器，用于追踪执行。 |
| `verbose` | `bool` | 是否在控制台输出详细日志。默认为全局 `verbose` 设置。 |
| `tags` | `list[str] \| None` | 关联的标签，用于在追踪平台（如 LangSmith）中进行过滤。 |
| `metadata` | `dict[str, Any] \| None` | 关联的元数据。 |

### 3. 主要方法

- **`invoke(input, config, **kwargs)`**: 运行链的核心入口。它负责准备输入、启动回调、执行 `_call` 逻辑、记录错误以及准备输出。
- **`run(*args, **kwargs)`**: **[便捷方法]** 仅返回输出值（通常是字符串）。如果链有多个输出键，此方法可能会受限。
- **`prep_inputs(inputs)`**: 内部方法。将用户输入与内存中的变量合并。
- **`prep_outputs(inputs, outputs, return_only_outputs)`**: 内部方法。将结果保存回内存，并根据配置决定是否包含原始输入。

## 自定义链的实现

要实现一个自定义链，你需要：
1. 继承 `Chain` 类。
2. 定义 `input_keys` 属性（返回输入键名列表）。
3. 定义 `output_keys` 属性（返回输出键名列表）。
4. 实现 `_call` 方法（同步逻辑）。
5. 实现 `_acall` 方法（异步逻辑，可选）。

## 注意事项

1. **迁移建议**: 新项目应优先使用 LCEL。LCEL 提供了更好的流式支持、异步支持和并行执行能力。
2. **内存注入**: 注入的内存变量名必须与提示词模板中的占位符完全一致。
3. **Pydantic**: 这是一个 Pydantic 模型，所有参数都可以通过构造函数传递。
