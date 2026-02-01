# FileCallbackHandler

## 文件概述
`file.py` 定义了 `FileCallbackHandler`，这是一个将 LangChain 事件日志写入本地文件的回调处理器。它继承自 `BaseCallbackHandler`，支持同步写入，并提供了对链（Chain）、代理（Agent）和工具（Tool）等组件生命周期事件的日志记录功能。该处理器推荐通过上下文管理器（Context Manager）使用，以确保文件句柄的正确关闭。

## 导入依赖
- `pathlib.Path`: 用于跨平台的路径处理和文件操作。
- `typing.TextIO`: 用于类型注解，表示文本流。
- `langchain_core._api.warn_deprecated`: 用于发出弃用警告。
- `langchain_core.callbacks.BaseCallbackHandler`: 所有回调处理器的基类。
- `langchain_core.utils.input.print_text`: LangChain 提供的统一文本打印工具，支持颜色输出。

## 类与函数详解
### 1. FileCallbackHandler
**功能描述**: 将回调事件输出到指定的文本文件中。支持追加（Append）或覆盖（Write）模式。

#### 构造函数参数
| 参数名 | 类型 | 默认值 | 是否必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `filename` | `str` | - | 是 | 输出文件的路径。 |
| `mode` | `str` | `'a'` | 否 | 文件打开模式（如 `'w'`, `'a'`, `'x'`）。 |
| `color` | `str \| None` | `None` | 否 | 输出文本的默认颜色。 |

#### 核心方法
- **`__enter__` / `__exit__`**: 实现上下文管理器协议，确保 `with` 语句结束时自动关闭文件。
- **`close()`**: 手动关闭文件句柄，释放资源。
- **`_write(text, color, end)`**: 内部写入方法。如果未使用上下文管理器，会在第一次调用时发出弃用警告。
- **`on_chain_start` / `on_chain_end`**: 记录链的启动（包含链名称）和结束。
- **`on_agent_action` / `on_agent_finish`**: 记录代理的行动日志和最终结果日志。
- **`on_tool_end`**: 记录工具的执行结果。

#### 使用示例
```python
from langchain_core.callbacks import FileCallbackHandler
from langchain_core.runnables import RunnableLambda

# 推荐用法：使用上下文管理器
with FileCallbackHandler("output.txt") as handler:
    chain = RunnableLambda(lambda x: x + 1)
    chain.invoke(1, config={"callbacks": [handler]})

# 弃用用法：直接实例化（需要手动关闭）
handler = FileCallbackHandler("output.txt")
try:
    # 执行操作...
    pass
finally:
    handler.close()
```

#### 注意事项
- **线程安全**: 该处理器并未显式加锁，在多线程并发写入同一个文件时可能存在竞争风险。
- **弃用警告**: 自 `0.3.67` 版本起，建议始终使用 `with` 语句。
- **文件编码**: 强制使用 `UTF-8` 编码打开文件。

## 内部调用关系
- **继承关系**: 继承自 `BaseCallbackHandler`。
- **外部依赖**: 调用 `print_text` 工具函数进行带颜色的文本格式化写入。

## 相关链接
- [LangChain 官方文档 - Callbacks](https://python.langchain.com/docs/modules/callbacks/)
- [源码文件](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/core/langchain_core/callbacks/file.py)

---
最后更新时间: 2026-01-29
对应源码版本: LangChain Core v1.2.7
