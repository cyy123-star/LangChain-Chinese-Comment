# langchain_core.tools.simple

## 文件概述
**langchain_core.tools.simple** 模块定义了 `Tool` 类，这是一个简化版的工具实现，专门设计用于包装仅接受**单个字符串输入**并返回字符串输出的同步或异步函数。它是 LangChain 中最基础的工具实现之一。

---

## 导入依赖
| 依赖项 | 来源 | 作用 |
| :--- | :--- | :--- |
| `Callable`, `Awaitable` | `collections.abc` | 用于类型提示同步和异步函数。 |
| `signature` | `inspect` | 用于检查包装函数的参数签名。 |
| `BaseTool` | `langchain_core.tools.base` | 工具的基类。 |
| `run_in_executor` | `langchain_core.runnables` | 用于在线程池中运行同步函数（实现异步调用同步工具）。 |

---

## 类与函数详解

### 1. Tool
**功能描述**: 一个简单的工具类，直接封装函数或协程。它严格限制为单输入，通常是一个字符串。
#### 核心属性
| 参数名 | 类型 | 默认值 | 是否必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `name` | `str` | - | 是 | 工具名称。 |
| `description` | `str` | `""` | 是 | 工具描述。模型根据此描述判断是否调用该工具。 |
| `func` | `Callable[..., str]` | `None` | 否 | 同步执行函数。如果为 `None`，则必须提供 `coroutine`。 |
| `coroutine` | `Callable[..., Awaitable[str]]` | `None` | 否 | 异步执行函数。 |

#### 核心方法
- **`args` (属性)**:
    - **功能**: 返回工具的输入参数架构。
    - **逻辑**: 如果没有定义 `args_schema`，则默认为 `{"tool_input": {"type": "string"}}`。
- **`from_function` (类方法)**:
    - **功能**: 从给定的函数或协程创建 `Tool` 实例。
    - **返回值**: `Tool` 实例。
- **`_run` / `_arun`**:
    - **功能**: 实际执行工具逻辑的内部方法。
    - **逻辑**: 自动处理回调管理器 (`run_manager`) 和配置参数 (`config`) 的传递。

---

## 核心逻辑
1. **单输入校验**: 在 `_to_args_and_kwargs` 方法中，`Tool` 会校验传入的参数数量。如果参数个数不等于 1，会抛出 `ToolException`。
2. **异步回退机制**: 如果调用 `ainvoke` 但没有提供 `coroutine`，`Tool` 会使用 `run_in_executor` 在单独的线程中运行同步的 `func`，从而保证不阻塞事件循环。
3. **后向兼容性**: `Tool` 保留了旧版的 `__init__` 构造函数和 `from_function` 方法，以兼容早期版本的 LangChain 习惯。

---

## 使用示例
```python
from langchain_core.tools import Tool

def search_wikipedia(query: str) -> str:
    """Simulate a wikipedia search."""
    return f"Results for {query} on Wikipedia..."

# 创建工具
search_tool = Tool(
    name="wikipedia",
    func=search_wikipedia,
    description="Useful for searching information on Wikipedia."
)

# 运行同步调用
result = search_tool.invoke("LangChain")
print(result) # 输出: Results for LangChain on Wikipedia...

# 运行异步调用 (会自动回退到线程运行)
import asyncio
async def run():
    result = await search_tool.ainvoke("Python")
    print(result)

asyncio.run(run())
```

---

## 注意事项
- **参数限制**: 如果你的函数需要多个参数，请使用 `StructuredTool` 而不是 `Tool`。
- **输入类型**: 默认情况下，`Tool` 假定输入是字符串。如果需要更复杂的 Pydantic 模型验证，建议在 `from_function` 中传入 `args_schema`。
- **异常处理**: `Tool` 抛出的 `ToolException` 可以被 Agent 的错误处理机制捕获。

---

## 内部调用关系
- `Tool` 继承自 `BaseTool`，并实现了 `_run` 和 `_arun` 抽象方法。
- 它利用 `langchain_core.runnables` 中的并发工具来实现同步转异步。

---

## 相关链接
- [langchain_core.tools.base](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/core/langchain_core/tools/base.md)
- [langchain_core.tools.structured](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/core/langchain_core/tools/structured.md)

---

## 元信息
- **最后更新时间**: 2026-01-29
- **对应源码版本**: LangChain Core v1.2.7
