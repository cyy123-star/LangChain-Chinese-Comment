# langchain_core/runnables/config.py

`RunnableConfig` 是 LangChain 中用于配置 `Runnable` 对象执行行为的核心数据结构。它定义了诸如追踪（Tracing）、元数据（Metadata）、并发控制（Concurrency）和回调（Callbacks）等关键参数。

## 文件概述

该文件定义了 `RunnableConfig` 类型（基于 `TypedDict`）以及一系列用于处理、合并和传播配置的工具函数。它通过 `ContextVar` 实现了配置在调用栈中的自动传播，减少了显式传递参数的需求。

## 导入依赖

| 依赖模块 | 作用 |
| :--- | :--- |
| `contextvars` | 使用 `ContextVar` 实现配置在异步和多线程环境下的自动传播。 |
| `langchain_core.callbacks.manager` | 处理回调管理器（CallbackManager）。 |
| `langsmith.run_helpers` | 与 LangSmith 追踪系统集成。 |

## 类与函数详解

### RunnableConfig (TypedDict)

`Runnable` 的配置字典。

#### 字段说明
| 字段名 | 类型 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- |
| `tags` | `list[str]` | `[]` | 用于过滤和分类调用的标签。 |
| `metadata` | `dict[str, Any]` | `{}` | 与调用关联的结构化元数据（JSON 可序列化）。 |
| `callbacks` | `Callbacks` | `None` | 自定义回调处理器列表或管理器。 |
| `run_name` | `str` | 类名 | 追踪运行的显示名称。 |
| `max_concurrency` | `int \| None` | `None` | 并行执行时的最大并发数。 |
| `recursion_limit` | `int` | `25` | 递归调用的最大深度。 |
| `configurable` | `dict[str, Any]` | `{}` | 运行时可动态调整的字段值。 |
| `run_id` | `UUID \| None` | `None` | 当前运行的唯一标识符。 |

### 核心工具函数

#### `ensure_config`
确保输入是一个有效的 `RunnableConfig` 对象。如果输入为 `None`，则返回一个包含默认值的空字典。它还会处理从 `ContextVar` 中提取当前上下文中的配置。

#### `merge_configs`
合并多个配置对象。子配置中的 `tags` 和 `metadata` 会与父配置合并，而不是简单的覆盖。

#### `patch_config`
在现有配置的基础上修改特定字段，返回一个新的配置对象。

#### `call_func_with_variable_args`
辅助函数，用于调用可能接受也可能不接受 `config` 或 `run_manager` 参数的函数。它会自动检测函数签名并传入正确的参数。

## 使用示例

### 1. 显式传递配置
```python
from langchain_core.runnables import RunnableConfig

config: RunnableConfig = {
    "tags": ["production", "test-run"],
    "metadata": {"user_id": "123"},
    "max_concurrency": 5
}

# 在调用链时传入
# chain.invoke(input, config=config)
```

### 2. 使用 `configurable` 动态调整
```python
# 假设模型已经配置了可调参数
configurable_config = {
    "configurable": {"model_name": "gpt-4"}
}
# chain.invoke(input, config=configurable_config)
```

## 注意事项

1. **自动传播**：LangChain 内部使用 `ContextVar` 传播配置。这意味着如果你在 `RunnableLambda` 内部调用另一个 `Runnable`，通常不需要手动传递 `config`。
2. **总是不为 None**：在编写自定义 `Runnable` 的 `_invoke` 等方法时，务必先调用 `ensure_config(config)`。
3. **不可变性**：虽然 `RunnableConfig` 是一个字典，但在传递过程中建议通过 `merge_configs` 或 `patch_config` 创建新对象，以避免意想不到的副作用。

## 内部调用关系

- 被几乎所有的 `Runnable` 子类（在 [base.py](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/core/langchain_core/runnables/base.py) 中定义）引用。
- 与 `CallbackManager`（在 [manager.py](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/core/langchain_core/callbacks/manager.py) 中定义）紧密集成。

## 相关链接

- [LangChain 官方文档 - Configuration](https://python.langchain.com/docs/how_to/configure/)
- [源码文件: langchain_core/runnables/config.py](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/core/langchain_core/runnables/config.py)
- [术语表: TERMINOLOGY.md](file:///d:/TraeProjects/langchain_code_comment/TERMINOLOGY.md)

---
最后更新时间: 2026-01-29
对应源码版本: LangChain Core v1.2.7
