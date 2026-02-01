# Runnable Utils：通用工具库

`utils.py` 是 LangChain `runnables` 模块的底层基石，提供了一系列用于并发控制、代码自省、类型校验和动态配置管理的工具函数与类。

## 文件概述

| 特性 | 描述 |
| :--- | :--- |
| **角色** | 内部工具箱、底层支撑模块 |
| **主要职责** | 提供异步并发管理、AST 源码分析、可配置字段规范定义等通用能力 |
| **所属模块** | `langchain_core.runnables.utils` |

该文件通过高度抽象的工具集，解决了跨 Python 版本兼容性、复杂的异步上下文传播以及 LCEL 链中动态参数映射等核心技术挑战。

## 核心功能详解

### 1. 异步并发控制

| 函数/类 | 描述 |
| :--- | :--- |
| `gather_with_concurrency` | 限制并发数量的 `asyncio.gather` 封装版本，防止资源耗尽。 |
| `gated_coro` | 使用信号量（Semaphore）保护的协程运行包装器。 |
| `coro_with_context` | 确保 `ContextVar`（上下文变量）在异步任务切换中正确传播。 |

### 2. 函数自省与 AST 分析

LangChain 大量使用 Python 的 `ast` 模块来分析用户传入的函数，以实现自动化的 Schema 生成。

| 函数/类 | 描述 |
| :--- | :--- |
| `accepts_config` | 检测函数签名中是否包含 `config` 参数。 |
| `get_lambda_source` | 提取 Lambda 表达式的原始代码字符串，用于序列化。 |
| `IsFunctionArgDict` | AST 访问器，分析函数的第一个参数是否为字典，并提取其键名。 |
| `get_function_nonlocals` | 提取函数闭包中访问的非局部变量，用于上下文识别。 |

### 3. 数据聚合工具

| 类名 | 描述 |
| :--- | :--- |
| `AddableDict` | 增强版字典，支持 `+` 运算符。如果键对应的值也支持相加（如字符串或列表），则自动合并。常用于流式数据块（Chunk）的聚合。 |
| `add` / `aadd` | 同步/异步地将一系列可相加对象（SupportsAdd）累加成一个最终结果。 |

### 4. 动态配置规范 (Configurable Fields)

这些类定义了如何向用户暴露 Runnable 的内部参数。

| 类名 | 描述 |
| :--- | :--- |
| `ConfigurableField` | 描述一个可配置的字段（ID、名称、描述、类型）。 |
| `ConfigurableFieldSpec` | 更底层的字段规格说明，包含默认值和依赖关系。 |
| `get_unique_config_specs` | 从多个 Runnable 组件中收集并去重配置规格，检测是否存在命名冲突。 |

## 核心逻辑解读：AddableDict

`AddableDict` 是流式处理的核心。当两个 `AddableDict` 相加时：
1.  遍历所有键。
2.  如果键在两个字典中都存在，且值支持 `__add__`，则执行加法（如字符串拼接、列表合并）。
3.  如果不支持加法，则后者覆盖前者。
这种机制使得 `chain.stream()` 产生的增量块可以被简单地通过 `sum()` 或循环累加还原为完整结果。

## 使用示例

### 限制并发数
```python
from langchain_core.runnables.utils import gather_with_concurrency
import asyncio

async def task(i):
    await asyncio.sleep(1)
    return i

# 同时最多只运行 2 个任务
results = await gather_with_concurrency(2, *(task(i) for i in range(5)))
```

### 使用 AddableDict 聚合数据
```python
from langchain_core.runnables.utils import AddableDict

d1 = AddableDict({"text": "Hello", "count": 1})
d2 = AddableDict({"text": " World", "count": 1})

# 自动合并文本并累加计数
print(d1 + d2) # {'text': 'Hello World', 'count': 2}
```

## 注意事项

*   **Python 版本兼容性**：`coro_with_context` 在 Python 3.11+ 中利用了 `asyncio.create_task` 原生支持的 `context` 参数，而在旧版本中则有不同的处理路径。
*   **AST 局限性**：源码分析工具依赖于能够获取到源代码（`inspect.getsource`）。在某些动态生成函数或交互式环境（如某些版本的 Jupyter）中可能会失败。
*   **序列化**：配置规范类（如 `ConfigurableField`）被设计为 `NamedTuple`，以确保它们是不可变的且易于序列化。

## 内部调用关系

*   **RunnableSequence**：使用 `get_unique_config_specs` 来整合整条链的配置。
*   **RunnableLambda**：大量使用 `get_lambda_source` 和 `IsFunctionArgDict` 来推断输入输出 Schema。
*   **BaseMessageChunk**：在消息块合并时，底层逻辑与 `AddableDict` 的思想一致。

---
最后更新时间：2026-01-29
对应源码版本：LangChain Core v1.2.7
