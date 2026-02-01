# base.py

- **最后更新时间**: 2026-01-29
- **对应源码版本**: LangChain Core v1.2.7

## 文件概述
`base.py` 定义了追踪器（Tracers）的基础接口 `BaseTracer`。它是所有追踪器（如 `LangChainTracer`, `ConsoleCallbackHandler`）的直接父类。它结合了 `_TracerCore` 的运行管理能力和 `BaseCallbackHandler` 的事件驱动接口，实现了将执行过程中的各种事件自动转化为结构化的追踪数据。

## 导入依赖
| 模块 | 作用 |
| :--- | :--- |
| `abc` | 用于定义抽象基类和抽象方法。 |
| `langchain_core.callbacks.base` | 继承 `BaseCallbackHandler` 以支持回调机制。 |
| `langchain_core.tracers.core` | 继承 `_TracerCore` 以获取追踪核心逻辑。 |
| `langchain_core.tracers.schemas.Run` | 运行数据模型。 |

## 类与函数详解
### 1. BaseTracer (抽象基类)
- **功能描述**: 将回调事件映射到追踪运行（Run）的生命周期。每当发生一个 `on_..._start` 事件时，它会创建一个新的 `Run` 对象并开始追踪；当发生 `on_..._end` 或 `on_..._error` 事件时，它会更新并结束对应的 `Run`。
- **核心方法**:
  - **_persist_run(run: Run)**: **抽象方法**。子类必须实现此方法以决定如何处理完成后的运行数据（例如打印到控制台或异步发送到后端服务器）。
  - **_start_trace(run: Run)**: 调用父类逻辑初始化追踪，并触发 `_on_run_create` 钩子。
  - **_end_trace(run: Run)**: 结束追踪。如果是根运行（没有父运行），则调用 `_persist_run`。
  - **on_chat_model_start(...)**: 处理聊天模型开始事件，创建并启动 `chat_model` 类型的追踪。
  - **on_llm_start(...)**: 处理 LLM 开始事件，创建并启动 `llm` 类型的追踪。
  - **on_chain_start(...)**: 处理 Chain 开始事件，创建并启动 `chain` 类型的追踪。
  - **on_tool_start(...)**: 处理工具开始事件，创建并启动 `tool` 类型的追踪。

## 核心逻辑解读
- **事件驱动的追踪**: `BaseTracer` 监听 LangChain 的回调系统。它利用 `run_id` 在并发执行的环境中准确地定位和更新对应的 `Run` 对象。
- **自动级联**: 通过在 `on_..._start` 中自动关联 `parent_run_id`，`BaseTracer` 能够自动构建出完整的调用树。

## 注意事项
- 追踪器是线程安全的，因为它通过 `run_id`（通常是 UUID）来隔离不同的并发运行。
- 大多数 `on_...` 方法返回的是 `Run` 对象，这允许调用者获取当前的追踪上下文。

## 相关链接
- [langchain_core.tracers.core](core.md)
- [langchain_core.callbacks.base](../callbacks/base.md)
