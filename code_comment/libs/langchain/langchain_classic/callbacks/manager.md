# libs\langchain\langchain_classic\callbacks\manager.py

`manager.py` 负责管理和分发回调事件。它是 LangChain 运行时的“指挥中心”，确保所有的回调处理器（Handlers）都能在正确的时机接收到正确的事件。

## 核心类

### 1. CallbackManager / AsyncCallbackManager
核心管理器类，负责持有多个回调处理器并在事件发生时循环调用它们。

### 2. RunManager (及其子类)
专门为单次运行（Run）设计的管理器。每当一个 LLM、Chain 或 Tool 开始运行时，都会创建一个对应的 RunManager 实例。

- **CallbackManagerForLLMRun**: LLM 运行时的管理器。
- **CallbackManagerForChainRun**: Chain 运行时的管理器。
- **CallbackManagerForToolRun**: Tool 运行时的管理器。

## 核心功能

- **事件分发**: 当 `on_chain_start` 等事件触发时，管理器会确保所有注册的处理器都收到通知。
- **上下文管理**: 支持通过 `trace_as_chain_group` 等上下文管理器来组织复杂的运行嵌套。
- **动态加载**: 提供了对 `get_openai_callback` 和 `wandb_tracing_enabled` 等 community 组件的动态加载支持。

## 使用示例

### 获取 OpenAI Token 使用情况
```python
from langchain_classic.callbacks import get_openai_callback

with get_openai_callback() as cb:
    result = llm.invoke("Tell me a joke")
    print(f"Total Tokens: {cb.total_tokens}")
    print(f"Prompt Tokens: {cb.prompt_tokens}")
    print(f"Completion Tokens: {cb.completion_tokens}")
    print(f"Total Cost (USD): ${cb.total_cost}")
```

## 注意事项

- **线程安全**: 同步管理器在处理并发请求时需要注意线程安全问题。
- **性能开销**: 注册过多的回调处理器可能会对性能产生微弱影响，尤其是在高频调用的场景下。
