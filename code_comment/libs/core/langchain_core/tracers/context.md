# libs\core\langchain_core\tracers\context.py

## 文件概述

`context.py` 模块负责 LangChain Tracer 的上下文管理。它利用 Python 的 `contextvars` 机制，允许开发者通过上下文管理器（Context Manager）轻松启用或禁用追踪功能（如 LangSmith 追踪），并在并发环境下保持追踪状态的隔离。

## 导入依赖

- `contextlib.contextmanager`: 用于创建上下文管理器。
- `contextvars.ContextVar`: 提供并发安全的上下文变量存储。
- `langchain_core.tracers.langchain.LangChainTracer`: 核心追踪处理器，用于与 LangSmith 交互。
- `langchain_core.tracers.run_collector.RunCollectorCallbackHandler`: 用于收集运行轨迹的处理器。

## 关键变量

- `tracing_v2_callback_var`: 存储当前上下文中的 `LangChainTracer` 实例。
- `run_collector_var`: 存储当前上下文中的 `RunCollectorCallbackHandler` 实例。

## 类与函数详解

### 1. tracing_v2_enabled
- **功能描述**: 上下文管理器，用于在当前上下文中启用 LangSmith 追踪（V2 版本）。进入上下文时会自动创建一个 `LangChainTracer` 并设为当前上下文的追踪器。
- **参数说明**:
| 参数名 | 类型 | 默认值 | 是否必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `project_name` | `str \| None` | `None` | 否 | LangSmith 项目名称。默认为 `'default'`。 |
| `example_id` | `str \| UUID \| None` | `None` | 否 | 关联的示例 ID。 |
| `tags` | `list[str] \| None` | `None` | 否 | 为此次运行添加的标签列表。 |
| `client` | `LangSmithClient \| None` | `None` | 否 | LangSmith 客户端实例。 |

### 2. collect_runs
- **功能描述**: 上下文管理器，用于收集上下文内所有的运行轨迹。常用于单元测试或需要获取中间运行 ID 的场景。
- **返回值**: 产生一个 `RunCollectorCallbackHandler` 实例。

## 使用示例

### 启用追踪并获取 URL
```python
from langchain_core.tracers.context import tracing_v2_enabled

with tracing_v2_enabled(project_name="my-project") as cb:
    # 这里的所有 LangChain 调用都会被记录到 LangSmith
    chain.invoke("hello")
    run_url = cb.get_run_url()
    print(f"追踪地址: {run_url}")
```

### 收集运行 ID
```python
from langchain_core.tracers.context import collect_runs

with collect_runs() as runs_cb:
    chain.invoke("hello")
    # 获取第一个运行的 ID
    run_id = runs_cb.traced_runs[0].id
    print(f"Run ID: {run_id}")
```

## 注意事项

- **并发安全**: 使用 `ContextVar` 确保在多线程或异步（asyncio）环境下，追踪状态是相互隔离的，不会互相干扰。
- **作用域**: 追踪仅在 `with` 语句块内有效，离开块后会自动重置追踪状态。

---
最后更新时间: 2026-01-29
对应源码版本: LangChain Core v1.2.7
