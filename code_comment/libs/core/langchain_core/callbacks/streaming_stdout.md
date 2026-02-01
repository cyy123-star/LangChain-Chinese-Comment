# StreamingStdOutCallbackHandler

## 文件概述
`streaming_stdout.py` 定义了 `StreamingStdOutCallbackHandler`，这是一个专门用于处理大语言模型（LLM）流式输出的回调处理器。当 LLM 开启 `streaming=True` 时，该处理器会在每一个新 Token 生成时立即将其打印到标准输出，从而实现平滑的“打字机”显示效果。

## 导入依赖
- `sys`: 用于直接操作 `sys.stdout` 和调用 `flush()` 以确保即时显示。
- `langchain_core.callbacks.base.BaseCallbackHandler`: 回调处理器的基类。

## 类与函数详解
### 1. StreamingStdOutCallbackHandler
**功能描述**: 拦截 LLM 的 `on_llm_new_token` 事件。它是许多命令行 Demo 中实现实时流式显示的核心组件。

#### 核心方法
- **`on_llm_new_token(token, **kwargs)`**: 
    - **逻辑**: 接收新生成的 `token` 字符串，通过 `sys.stdout.write(token)` 写入。
    - **关键点**: 紧接着调用 `sys.stdout.flush()`。这是因为标准输出通常是行缓冲或块缓冲的，如果不显式刷新，Token 可能不会立即显示在屏幕上。
- **其他方法 (No-op)**: 该处理器重写了大量的生命周期方法（如 `on_llm_start`, `on_chain_start` 等），但其内部实现均为空（pass）。这意味着它只专注于 Token 的流式打印，而忽略其他日志信息。

#### 使用示例
```python
from langchain_openai import ChatOpenAI
from langchain_core.callbacks import StreamingStdOutCallbackHandler

# 在初始化模型时配置
llm = ChatOpenAI(
    model="gpt-4o",
    streaming=True, # 必须开启流式模式
    callbacks=[StreamingStdOutCallbackHandler()]
)

# 当调用 invoke 时，Token 会实时显示在终端
llm.invoke("写一首关于春天的诗")
```

#### 注意事项
- **限制条件**: 仅适用于支持流式输出的 LLM。如果模型本身不支持或未开启流式开关，该处理器将不会产生任何效果。
- **干净输出**: 由于它只打印 Token，不会像 `StdOutCallbackHandler` 那样打印 `> Entering chain...` 等元信息，因此适合需要纯净回复内容的场景。

## 内部调用关系
- **继承关系**: 继承自 `BaseCallbackHandler`。
- **系统交互**: 直接与 Python 的标准库 `sys` 交互，绕过了 LangChain 的高级打印工具。

## 相关链接
- [LangChain 官方文档 - Streaming](https://python.langchain.com/docs/modules/model_io/models/llms/streaming)
- [源码文件](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/core/langchain_core/callbacks/streaming_stdout.py)

---
最后更新时间: 2026-01-29
对应源码版本: LangChain Core v1.2.7
