# RunnableRetry：自动重试组件

`retry.py` 模块定义了 `RunnableRetry` 类，它利用 `tenacity` 库为 LangChain 的 `Runnable` 对象提供强大的自动重试功能，常用于处理网络抖动或临时性的 API 故障。

## 文件概述

| 特性 | 描述 |
| :--- | :--- |
| **角色** | 重试逻辑装饰器、Runnable 绑定器 |
| **主要职责** | 在发生特定异常时，按照预设策略重新执行逻辑 |
| **所属模块** | `langchain_core.runnables.retry` |

该模块的核心思想是将不稳定的 `Runnable` 包装起来，通过配置最大尝试次数、退避策略和异常过滤，提高系统的鲁棒性。

## 导入依赖

| 模块/类 | 作用 |
| :--- | :--- |
| `tenacity` | 底层重试库，提供 `Retrying`, `stop_after_attempt`, `wait_exponential_jitter` 等核心能力 |
| `RunnableBindingBase` | 基类，允许将重试参数绑定到现有的 Runnable 上 |
| `patch_config` | 用于在重试过程中修改配置（如添加重试标签） |

## 类详解：RunnableRetry

### 功能描述
`RunnableRetry` 拦截 `invoke` 或 `batch` 调用。如果内部 `Runnable` 抛出指定的异常，它会根据 `tenacity` 的策略等待一段时间后再次尝试。它会自动在回调管理器的标签中注入重试信息（如 `retry:attempt:2`），方便在 LangSmith 等追踪工具中观察。

### 参数说明

| 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `bound` | `Runnable` | - | 是 | 需要被重试的原始 Runnable 对象。 |
| `retry_exception_types` | `tuple` | `(Exception,)` | 否 | 触发重试的异常类型列表。建议只重试瞬时性错误（如 429 或 5xx）。 |
| `max_attempt_number` | `int` | `3` | 否 | 最大尝试次数（包括第一次执行）。 |
| `wait_exponential_jitter` | `bool` | `True` | 否 | 是否在指数退避中加入随机抖动，以防止“惊群效应”。 |
| `exponential_jitter_params` | `dict` | `None` | 否 | 细粒度控制退避策略，如 `initial`（初始等待）、`max`（最大等待）等。 |

### 核心逻辑解读

1.  **策略构建 (`_kwargs_retrying`)**：
    *   将 Pydantic 风格的参数转换为 `tenacity` 所需的 `stop`（停止条件）、`wait`（等待策略）和 `retry`（重试判定）对象。
2.  **配置增强 (`_patch_config`)**：
    *   每次重试时，都会生成一个新的子回调管理器，并带上 `retry:attempt:N` 标签，确保重试过程的可追踪性。
3.  **批量重试 (`_batch`)**：
    *   `RunnableRetry` 优化了 `batch` 的重试逻辑：如果一批任务中只有部分失败，它只会针对失败的任务进行重试，而不会重新运行已经成功的任务，从而节省资源。

### 使用示例

最常用的方式是通过 Runnable 的 `.with_retry()` 方法：

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import httpx

# 定义一个不稳定的模型调用
model = ChatOpenAI(model="gpt-3.5-turbo")

# 配置重试：针对网络超时和 429 错误重试 3 次
runnable_with_retry = model.with_retry(
    retry_if_exception_type=(httpx.TimeoutException, httpx.HTTPStatusError),
    stop_after_attempt=3
)

prompt = ChatPromptTemplate.from_template("讲个关于 {topic} 的笑话")
chain = prompt | runnable_with_retry

# 如果第一次调用超时，它会自动重试
response = chain.invoke({"topic": "程序员"})
```

### 注意事项

*   **流式限制**：`RunnableRetry` **不支持** `stream()` 和 `transform()` 的重试。因为流式输出一旦开始，重试逻辑会变得非常复杂且不直观（例如，已经吐出了一半字符后发生错误，重试该如何处理）。
*   **重试范围**：建议将重试范围限制在最可能出错的单个组件上（如 LLM 调用），而不是整个复杂的链，以减少不必要的重复计算和副作用。
*   **异常幂等性**：确保重试的操作是幂等的，或者重试失败不会导致数据状态不一致。

## 内部调用关系

*   **tenacity**：深度集成，所有的等待和停止逻辑都委托给此库。
*   **RunnableBindingBase**：通过 Pydantic 序列化能力，确保重试配置可以被保存和加载。
*   **CallbackManager**：在重试循环中动态创建子 Run，实现链路追踪。

## 相关链接

*   [Tenacity 官方文档](https://tenacity.readthedocs.io/)
*   [LangChain 概念指南 - 重试](https://python.langchain.com/docs/expression_language/how_to/retries)

---
最后更新时间：2026-01-29
对应源码版本：LangChain Core v1.2.7
