# Callbacks (回调系统)

`callbacks` 模块是 LangChain Classic 的核心组成部分，它提供了一个强大的钩子（Hooks）系统，允许开发者在 LLM 应用的生命周期的各个阶段（如 LLM 开始执行、工具结束、链发生错误等）注入自定义逻辑。

## 核心概念

### 1. `BaseCallbackHandler`
所有回调处理器的基类。它定义了一系列以 `on_` 开头的方法，对应不同的事件：
- `on_llm_start`: 当 LLM 开始运行时触发。
- `on_chain_start`: 当 Chain 开始运行时触发。
- `on_tool_start`: 当 Tool 开始运行时触发。
- `on_llm_end`: 当 LLM 完成运行并返回结果时触发。
- `on_chain_error`: 当 Chain 发生错误时触发。

### 2. `CallbackManager`
负责管理多个回调处理器，并将事件分发给它们。在 LangChain Classic 中，几乎所有的核心组件（Chain, LLM, Agent）都可以接收一个 `callbacks` 参数。

## 常用处理器

| 处理器 | 说明 |
| :--- | :--- |
| `StdOutCallbackHandler` | 将所有事件打印到标准输出（控制台）。 |
| `FileCallbackHandler` | 将事件记录到本地文件。 |
| `OpenAICallbackHandler` | 专门用于追踪 OpenAI 的 Token 使用情况和费用。 |
| `StreamingStdOutCallbackHandler` | 实现 LLM 输出的流式打印。 |

## 使用示例

```python
from langchain_classic.callbacks import StdOutCallbackHandler
from langchain_openai import ChatOpenAI

handler = StdOutCallbackHandler()
llm = ChatOpenAI(callbacks=[handler])

llm.invoke("Hello, how are you?")
```

## 追踪与监控 (Tracers)

`tracers` 子模块提供了更高级的追踪能力，通常用于与外部监控平台集成：
- **LangChain Tracer**: 将运行数据发送到 LangSmith。
- **Wandb Tracer**: 集成 Weights & Biases 进行实验追踪。
- **Comet Tracer**: 集成 Comet ML。

## 现代替代方案

在现代 LangChain 中，建议优先使用：
1. **LangSmith**: 官方推荐的生产级追踪和调试平台，只需配置环境变量即可自动启用。
2. **LCEL `config`**: 通过 `invoke(..., config={"callbacks": [...]})` 在运行时动态传入回调。
