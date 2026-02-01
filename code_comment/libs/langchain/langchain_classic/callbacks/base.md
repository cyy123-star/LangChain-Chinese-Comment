# libs\langchain\langchain_classic\callbacks\base.py

`base.py` 提供了回调处理器的基础接口定义。在 `langchain_classic` 中，它主要是对 `langchain_core.callbacks` 中定义的接口进行了重导出（Re-export）。

## 核心接口

这些接口定义了在 LangChain 组件（LLM, Chain, Tool 等）运行的不同阶段触发的动作。

- **BaseCallbackHandler**: 所有回调处理器的基类。
- **AsyncCallbackHandler**: 异步回调处理器的基类。
- **Callbacks**: 回调处理器的集合类型定义。

## 混合类 (Mixins)

这些类定义了特定组件的回调接口：

- **LLMManagerMixin**: 处理 LLM 相关的事件（如 `on_llm_start`, `on_llm_end`）。
- **ChainManagerMixin**: 处理 Chain 相关的事件（如 `on_chain_start`, `on_chain_end`）。
- **ToolManagerMixin**: 处理 Tool 相关的事件（如 `on_tool_start`, `on_tool_end`）。
- **RetrieverManagerMixin**: 处理 Retriever 相关的事件（如 `on_retriever_start`）。

## 使用说明

开发者通常通过继承 `BaseCallbackHandler` 或 `AsyncCallbackHandler` 并重写特定的 `on_*` 方法来创建自定义回调。

```python
from langchain_classic.callbacks import BaseCallbackHandler

class MyCustomHandler(BaseCallbackHandler):
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        print(f"Token: {token}")
```
