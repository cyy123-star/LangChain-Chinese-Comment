# Runnables & LCEL (核心运行机制)

`runnables` 模块是 **LCEL (LangChain Expression Language)** 的核心。它定义了一种统一的接口，使得不同的组件（如 Prompt, LLM, OutputParser）可以通过管道符 `|` 进行无缝组合。

## 核心接口：`Runnable`

所有的 LCEL 组件都继承自 `Runnable` 基类，它规定了四个核心方法：
- `invoke(input)`: 同步调用，输入转输出。
- `batch(inputs)`: 批处理，高效处理多个输入。
- `stream(input)`: 流式输出。
- `ainvoke`, `abatch`, `astream`: 对应的异步版本。

## 常见 Runnable 类型

| 类型 | 说明 |
| :--- | :--- |
| `RunnableSequence` | 由 `|` 创建的链式组合。 |
| `RunnableParallel` | 并行执行多个组件（也称为 `RunnableMap`）。 |
| `RunnableLambda` | 将自定义 Python 函数包装为 Runnable。 |
| `RunnablePassthrough` | 透传数据，常用于在并行链中保留原始输入。 |
| `RunnableBinding` | 给 Runnable 绑定固定的参数（如 `stop` 词）。 |
| `HubRunnable` | 从 LangChain Hub 动态加载并运行提示词。 |

## 组合示例

```python
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

# 创建一个并行链
chain = RunnableParallel(
    context=retriever,
    question=RunnablePassthrough()
) | prompt | llm | parser

# 执行
result = chain.invoke("What is LCEL?")
```

## 配置与回退 (Fallbacks)

- **Configurable**: 可以在运行时动态切换模型或参数（使用 `.with_config()`）。
- **Fallbacks**: 当主要模型失败时，自动切换到备用模型（使用 `.with_fallbacks()`）。

## 迁移指南

- **核心包**: 所有的 `Runnable` 定义现在都已移至 `langchain-core`。
- **透明度**: 相比于传统的 `Chain`，`Runnable` 提供了更好的可观察性和调试支持（原生兼容 LangSmith）。
