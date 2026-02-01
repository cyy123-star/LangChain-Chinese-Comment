# RouterRunnable：动态路由组件

`router.py` 模块定义了 `RouterRunnable` 类，它根据输入中指定的键（Key）将任务动态分发给不同的 `Runnable` 路径。这在构建需要根据条件（如用户意图、任务类型）切换处理逻辑的 AI 应用中非常有用。

## 文件概述

| 特性 | 描述 |
| :--- | :--- |
| **角色** | 逻辑分发器、路由组件 |
| **主要职责** | 根据输入字典中的 `key` 字段，选择并执行对应的子 Runnable |
| **所属模块** | `langchain_core.runnables.router` |

`RouterRunnable` 实现了一种简单的“查表式”路由逻辑。它维护一个字符串到 `Runnable` 的映射表，根据输入的指令决定走哪条路。

## 导入依赖

| 模块/类 | 作用 |
| :--- | :--- |
| `RunnableSerializable` | 基类，支持序列化和 Pydantic 校验 |
| `coerce_to_runnable` | 强制转换工具，确保映射表中的值都是合法的 Runnable |
| `gather_with_concurrency` | 异步并发工具，用于处理 `abatch` 中的并行路由调用 |

## 类详解：RouterRunnable

### 功能描述
`RouterRunnable` 接收一个特定的字典格式作为输入：`{"key": "...", "input": "..."}`。它查找与 `key` 对应的子 `Runnable`，然后将 `input` 部分作为参数调用该子组件。

### 数据结构：RouterInput

这是一个 `TypedDict`，定义了路由器的输入规范：

| 字段名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `key` | `str` | 路由键，必须存在于 `runnables` 映射中。 |
| `input` | `Any` | 传递给目标 `Runnable` 的实际输入数据。 |

### 参数说明

| 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `runnables` | `Mapping[str, Runnable]` | - | 是 | 一个字典，键是路由标识符，值是对应的处理逻辑。 |

### 核心逻辑解读

1.  **单次调用 (`invoke`)**：
    *   从输入中提取 `key`。
    *   检查 `key` 是否在映射表中，不在则抛出 `ValueError`。
    *   调用对应的 `runnable.invoke(actual_input, config)`。
2.  **批量调用 (`batch`)**：
    *   并行地对输入列表进行路由处理。
    *   使用线程池（或异步并发）同时执行多个路由目标，提高处理效率。
3.  **流式处理 (`stream`)**：
    *   透明地转发流式调用，即调用选定目标的 `stream` 方法并产生结果。

### 使用示例

```python
from langchain_core.runnables.router import RouterRunnable
from langchain_core.runnables import RunnableLambda

# 1. 定义不同的处理分支
add_one = RunnableLambda(lambda x: x + 1)
multiply_ten = RunnableLambda(lambda x: x * 10)

# 2. 创建路由器
router = RouterRunnable(runnables={
    "increment": add_one,
    "scale": multiply_ten
})

# 3. 路由到 'increment' 分支
result1 = router.invoke({"key": "increment", "input": 5})
print(result1)  # 输出: 6

# 4. 路由到 'scale' 分支
result2 = router.invoke({"key": "scale", "input": 5})
print(result2)  # 输出: 50
```

### 注意事项

*   **输入格式强制要求**：输入必须是包含 `key` 和 `input` 两个键的字典，否则会报错。
*   **路由键缺失**：如果 `key` 在 `runnables` 映射中找不到，会抛出 `ValueError`。在实际应用中，通常建议先通过分类器确保 `key` 的合法性。
*   **配置传递**：`config` 参数会被透明地传递给选中的子 `Runnable`，确保追踪和回调在路由后依然有效。

## 内部调用关系

*   **coerce_to_runnable**：在初始化时，确保传入的函数或映射都被包装成标准的 `Runnable` 对象。
*   **get_executor_for_config**：在 `batch` 操作中获取合适的执行器（如线程池）来并行处理路由任务。

## 相关链接

*   [LangChain 概念指南 - 路由](https://python.langchain.com/docs/expression_language/how_to/routing)
*   [RunnableBranch (另一种路由方式)](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/core/langchain_core/runnables/branch.md)

---
最后更新时间：2026-01-29
对应源码版本：LangChain Core v1.2.7
