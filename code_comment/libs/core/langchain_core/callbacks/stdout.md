# StdOutCallbackHandler

## 文件概述
`stdout.py` 定义了 `StdOutCallbackHandler`，这是 LangChain 中最基础的回调处理器之一，用于将事件日志直接打印到标准输出（Console/Terminal）。它提供了简单的视觉反馈，帮助开发者实时观察 Chain 和 Agent 的运行状态，特别是它们进入和退出各个步骤的过程。

## 导入依赖
- `langchain_core.callbacks.base.BaseCallbackHandler`: 回调处理器的抽象基类。
- `langchain_core.utils.print_text`: 用于向标准输出打印带颜色文本的辅助工具。

## 类与函数详解
### 1. StdOutCallbackHandler
**功能描述**: 实时打印 LangChain 组件的执行进度。它通过 ANSI 转义序列（如 `\033[1m`）实现加粗显示，并利用 `print_text` 提供颜色支持。

#### 构造函数参数
| 参数名 | 类型 | 默认值 | 是否必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `color` | `str \| None` | `None` | 否 | 全局默认打印颜色。如果为 `None`，则使用终端默认颜色。 |

#### 核心方法
- **`on_chain_start`**: 打印加粗的 `> Entering new {name} chain...`。
- **`on_chain_end`**: 打印加粗的 `> Finished chain.`。
- **`on_agent_action`**: 打印代理执行的具体动作日志。
- **`on_tool_end`**: 打印工具返回的结果（Observation）。
- **`on_agent_finish`**: 打印代理结束时的日志。

#### 使用示例
```python
from langchain_core.callbacks import StdOutCallbackHandler
from langchain_core.runnables import RunnableLambda

# 实例化处理器，设置颜色为绿色
handler = StdOutCallbackHandler(color="green")

chain = RunnableLambda(lambda x: f"Processed {x}")
# 在调用时通过 config 传入
chain.invoke("input data", config={"callbacks": [handler]})
```

#### 注意事项
- **简单性**: 相比于 `FileCallbackHandler`，它没有上下文管理器的需求，因为它只是简单的向 `sys.stdout` 打印。
- **格式化**: 它内部硬编码了一些格式（如 `> Entering...`），适合快速调试，但不适合作为高度自定义的日志方案。

## 内部调用关系
- **继承关系**: 继承自 `BaseCallbackHandler`。
- **交互**: 频繁调用 `langchain_core.utils.print_text` 来处理不同颜色的文本输出。

## 相关链接
- [LangChain 官方文档 - Callbacks](https://python.langchain.com/docs/modules/callbacks/)
- [源码文件](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/core/langchain_core/callbacks/stdout.py)

---
最后更新时间: 2026-01-29
对应源码版本: LangChain Core v1.2.7
