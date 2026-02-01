# globals.py - 全局配置管理

- **最后更新时间**: 2026-01-29
- **对应源码版本**: LangChain Core v1.2.7

## 文件概述

`globals.py` 用于设置和获取 LangChain 框架的全局配置。它提供了一种集中管理全局标志（如 verbose、debug）和全局缓存（llm_cache）的方法。

## 导入依赖

| 模块 | 作用 |
| :--- | :--- |
| `typing.Optional` | 用于类型提示。 |
| `langchain_core.caches.BaseCache` | 缓存接口定义（仅用于类型检查）。 |

## 函数详解

### 1. set_verbose
- **功能描述**: 设置全局的 `verbose`（详细）模式。
- **参数说明**:
  | 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
  | :--- | :--- | :--- | :--- | :--- |
  | `value` | `bool` | - | 是 | 是否开启详细模式。开启后，框架会打印更多中间运行信息。 |

### 2. get_verbose
- **功能描述**: 获取当前的全局 `verbose` 设置。
- **返回值**: `bool`，当前是否处于详细模式。

### 3. set_debug
- **功能描述**: 设置全局的 `debug`（调试）模式。
- **参数说明**:
  | 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
  | :--- | :--- | :--- | :--- | :--- |
  | `value` | `bool` | - | 是 | 是否开启调试模式。开启后，框架会进入最详细的日志记录状态，通常用于排查复杂问题。 |

### 4. get_debug
- **功能描述**: 获取当前的全局 `debug` 设置。
- **返回值**: `bool`，当前是否处于调试模式。

### 5. set_llm_cache
- **功能描述**: 设置全局的 LLM 缓存。
- **参数说明**:
  | 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
  | :--- | :--- | :--- | :--- | :--- |
  | `value` | `BaseCache | None` | - | 是 | 要使用的缓存实例。如果为 `None`，则禁用全局缓存。 |

### 6. get_llm_cache
- **功能描述**: 获取当前的全局 LLM 缓存实例。
- **返回值**: `BaseCache | None`，当前的缓存实例或 `None`。

## 核心逻辑

- **状态存储**: 模块内部使用私有全局变量（`_verbose`, `_debug`, `_llm_cache`）存储状态。
- **接口访问限制**: 官方强烈建议**不要直接访问**这些私有变量，而应始终通过 `get_<X>` 和 `set_<X>` 函数进行操作，以确保行为的预测性和与其他组件的兼容性。
- **影响范围**: 这些设置会影响整个 LangChain 框架中所有未显式指定相关参数的 `Runnable`、`Chain` 或 `Model` 对象。

## 使用示例

```python
from langchain_core.globals import set_verbose, set_llm_cache
from langchain_core.caches import InMemoryCache

# 开启详细模式，方便查看 Chain 的执行过程
set_verbose(True)

# 设置全局内存缓存，减少重复的 LLM API 调用
set_llm_cache(InMemoryCache())

# 此时运行任何 Chain，都会默认应用这些全局设置
```

## 注意事项

- **线程安全性**: 这些全局设置在多线程环境下是共享的。如果你的应用需要不同线程拥有不同的行为（例如，某些请求需要 debug，某些不需要），请在具体对象的调用配置（`config`）中指定，而不是修改全局变量。
- **优先级**: 大多数 LangChain 组件（如 `BaseChatModel`）允许在调用时显式传递 `verbose` 或 `cache` 参数。显式传递的参数优先级始终高于全局设置。

## 相关链接
- [LangChain 调试指南](https://python.langchain.com/docs/guides/development/debugging/)
- [langchain_core.caches](caches.md)
