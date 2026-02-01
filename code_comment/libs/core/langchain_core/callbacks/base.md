# langchain_core.callbacks.base

## 文件概述
**langchain_core.callbacks.base** 是 LangChain 回调系统的核心基石。它定义了一系列 Mixin 类和基础处理器类（`BaseCallbackHandler` 和 `AsyncCallbackHandler`），为 LLM、Chain、Tool 和 Retriever 等组件在运行过程中的各个生命周期阶段（如开始、结束、出错、产生新 Token 等）提供了统一的钩子函数接口。

---

## 导入依赖
| 依赖项 | 来源 | 作用 |
| :--- | :--- | :--- |
| `logging` | 标准库 | 用于记录回调执行过程中的日志。 |
| `UUID` | `uuid` | 用于标识每个运行（Run）的唯一 ID。 |
| `RetryCallState` | `tenacity` | 用于处理重试事件的状态信息。 |
| `BaseMessage` | `langchain_core.messages` | Chat 模型回调中涉及的消息对象。 |
| `LLMResult` | `langchain_core.outputs` | LLM 完成运行时返回的结果对象。 |

---

## 类与函数详解

### 1. 核心 Mixin 类 (Manager Mixins)
这些 Mixin 类定义了针对不同组件生命周期的回调接口。
- **`RetrieverManagerMixin`**: 定义检索器（Retriever）相关的回调（`on_retriever_start`, `on_retriever_end`, `on_retriever_error`）。
- **`LLMManagerMixin`**: 定义大语言模型（LLM）相关的回调（`on_llm_new_token`, `on_llm_end`, `on_llm_error`）。
- **`ChainManagerMixin`**: 定义链（Chain）相关的回调（`on_chain_start`, `on_chain_end`, `on_chain_error`, `on_agent_action`, `on_agent_finish`）。
- **`ToolManagerMixin`**: 定义工具（Tool）相关的回调（`on_tool_start`, `on_tool_end`, `on_tool_error`）。
- **`RunManagerMixin`**: 定义通用运行相关的回调（`on_text`, `on_retry`, `on_custom_event`）。

### 2. BaseCallbackHandler
**功能描述**: 所有同步回调处理器的抽象基类。它继承了上述所有 Mixin 类。
#### 核心属性
| 参数名 | 类型 | 默认值 | 详细用途 |
| :--- | :--- | :--- | :--- |
| `raise_error` | `bool` | `False` | 如果为 `True`，回调执行出错时将抛出异常；否则仅记录日志。 |
| `run_inline` | `bool` | `False` | 是否在当前线程同步运行回调。 |

#### 过滤属性 (Properties)
提供了如 `ignore_llm`, `ignore_chain`, `ignore_agent` 等属性，允许处理器通过返回 `True` 来跳过特定类型的事件处理。

### 3. AsyncCallbackHandler
**功能描述**: `BaseCallbackHandler` 的异步版本。所有方法均为 `async`，允许在回调中执行异步操作（如异步发送监控数据）。

---

## 核心逻辑
1. **多重继承**: `BaseCallbackHandler` 通过继承多个 Mixin 类，实现了对 LangChain 几乎所有核心组件生命周期的覆盖。
2. **默认空实现**: Mixin 中的方法默认为空，子类只需重写感兴趣的方法。
3. **后备机制**: 例如，如果 `on_chat_model_start` 未实现，系统会自动尝试调用 `on_llm_start`。

---

## 使用示例
```python
from langchain_core.callbacks import BaseCallbackHandler
from typing import Any, Dict, List

class MyCustomHandler(BaseCallbackHandler):
    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any) -> None:
        print(f"LLM 启动了！提示词: {prompts}")

    def on_llm_end(self, response: Any, **kwargs: Any) -> None:
        print("LLM 结束运行。")

# 在调用时使用
# llm.invoke("Hello", config={"callbacks": [MyCustomHandler()]})
```

---

## 注意事项
- **线程安全**: 同步处理器的实现应考虑线程安全性，因为回调可能在不同线程中被触发。
- **性能影响**: 避免在回调中执行过于耗时的同步操作，以免阻塞核心业务逻辑。对于耗时操作，建议使用 `AsyncCallbackHandler` 或将任务派发到队列中。
- **错误处理**: 除非特殊需要，建议保持 `raise_error=False`，以防监控代码的问题导致主流程中断。

---

## 内部调用关系
- 该文件定义的类被 `CallbackManager` 使用，用于分发事件。
- `RunnableConfig` 中的 `callbacks` 参数最终会转换为这些处理器的列表。

---

## 相关链接
- [LangChain 官方文档 - Callbacks](https://python.langchain.com/docs/modules/callbacks/)
- [langchain_core.callbacks.manager](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/core/langchain_core/callbacks/manager.md)

---

## 元信息
- **最后更新时间**: 2026-01-29
- **对应源码版本**: LangChain Core v1.2.7
