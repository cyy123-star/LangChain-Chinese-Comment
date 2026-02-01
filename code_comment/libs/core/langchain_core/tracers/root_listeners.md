# root_listeners.py - 根运行监听器 Tracer

`root_listeners.py` 模块提供了一种简便的机制，专门用于监听 LangChain 运行树中**根运行**（Root Run）的状态变化。

## 文件概述

该模块定义了 `RootListenersTracer`（同步）和 `AsyncRootListenersTracer`（异步）。与监听所有子运行的普通 Tracer 不同，这些处理器仅在整个链路的最顶层任务开始、结束或报错时触发用户定义的回调函数。

## 导入依赖

| 依赖模块 | 作用 |
| :--- | :--- |
| `langchain_core.runnables.config` | 提供调用带动态参数函数的工具（`call_func_with_variable_args`）。 |
| `langchain_core.tracers.base` | 继承 `BaseTracer` 或 `AsyncBaseTracer`。 |

## 类详解

### `RootListenersTracer`

#### 功能描述
同步版本的根监听器。它通过检查 `run.id` 是否等于 `root_id` 来确保只对顶层运行生效。

#### 构造参数
| 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `config` | `RunnableConfig` | - | 是 | 运行配置，会传递给监听器。 |
| `on_start` | `Listener` | `None` | 否 | 根运行启动时的回调。 |
| `on_end` | `Listener` | `None` | 否 | 根运行成功结束时的回调。 |
| `on_error` | `Listener` | `None` | 否 | 根运行发生异常时的回调。 |

#### 核心逻辑
- **`_on_run_create`**: 记录第一个到达的 `run_id` 作为 `root_id`，并触发 `on_start`。
- **`_on_run_update`**: 仅当更新的运行 ID 等于 `root_id` 时，根据运行结果（是否有 error）触发 `on_end` 或 `on_error`。

---

### `AsyncRootListenersTracer`

#### 功能描述
异步版本的监听器。其逻辑与同步版本完全一致，但所有的回调触发都是异步等待（`await`）的。

---

## 监听器函数签名

监听器函数（`Listener` / `AsyncListener`）支持灵活的参数定义，可以接收以下一种或两种参数：
1. `run: Run`: 当前运行的详细信息（包含输入、输出、元数据等）。
2. `config: RunnableConfig`: 运行时的配置信息。

示例签名：
```python
def my_listener(run: Run, config: RunnableConfig):
    print(f"Root run {run.name} finished!")
```

---

## 使用示例

通常通过 `Runnable.with_listeners()` 快捷方法使用，而不需要手动实例化这些 Tracer：

```python
chain = my_runnable.with_listeners(
    on_start=lambda run: print("Start!"),
    on_end=lambda run: print("End!"),
    on_error=lambda run: print("Error!")
)

chain.invoke({"input": "hello"})
```

## 注意事项
- **唯一性**：一个 Tracer 实例生命周期内只锁定一个 `root_id`。
- **参数解耦**：底层使用 `call_func_with_variable_args`，这意味着你的监听器可以只定义 `run` 参数，也可以同时定义 `run` 和 `config`，甚至不定义参数，系统会自动适配。

## 相关链接
- [RunnableConfig 结构说明](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/core/langchain_core/runnables/config.md)
- [BaseTracer 源码](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/core/langchain_core/tracers/base.md)

---
**最后更新时间**: 2026-01-29
**对应源码版本**: LangChain Core v1.2.7
