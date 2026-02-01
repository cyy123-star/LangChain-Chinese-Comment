# libs\langchain\langchain_classic\callbacks\stdout.py

`stdout.py` 提供了一个简单的回调处理器，将 LangChain 的运行日志直接输出到标准输出（Console）。

## 核心类

### `StdOutCallbackHandler`
该处理器会将 Chain、LLM 和 Tool 的开始、结束、错误等生命周期事件格式化为可读的文本并打印。

## 主要功能

- **调试辅助**: 它是开发者在开发阶段最常用的工具之一，可以清晰地看到 Prompt 的最终样子、LLM 的原始输出以及 Chain 的嵌套执行过程。
- **详细模式**: 当 `verbose=True` 被设置在 Chain 或 Agent 上时，系统默认会使用此处理器。

## 使用示例

```python
from langchain_classic.callbacks import StdOutCallbackHandler
from langchain_classic.chains import LLMChain

handler = StdOutCallbackHandler()
# 在运行链时传入处理器
chain.invoke({"input": "Hello"}, callbacks=[handler])
```

## 注意事项

- **性能**: 在生产环境的大规模调用中，频繁的 IO 打印可能会对性能产生一定影响。
- **重定向**: 它直接使用 `print()`，因此会受到系统标准输出重定向的影响。
