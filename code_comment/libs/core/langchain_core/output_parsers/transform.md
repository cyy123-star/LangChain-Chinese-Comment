# langchain_core.output_parsers.transform

## 文件概述
`transform.py` 定义了能够处理流式输入（Streaming Input）的输出解析器基类。与标准的 `BaseOutputParser` 不同，这些类通过实现 `transform` 和 `atransform` 方法，允许在模型生成输出的过程中逐步进行解析和转换，而不需要等待模型生成完整的响应。

---

## 导入依赖
| 模块 | 作用 |
| :--- | :--- |
| `typing` | 提供类型注解支持（`Iterator`, `AsyncIterator` 等）。 |
| `langchain_core.messages` | 导入消息基类 `BaseMessage` 及其 Chunk 版本 `BaseMessageChunk`。 |
| `langchain_core.outputs` | 导入生成结果块 `GenerationChunk` 和 `ChatGenerationChunk`。 |
| `langchain_core.runnables.config` | 导入 `run_in_executor` 用于异步运行同步代码。 |

---

## 类与函数详解

### 1. BaseTransformOutputParser
**功能描述**: 支持流式转换的解析器基类。它定义了如何将输入的流（Iterator 或 AsyncIterator）转换为输出的流。

#### 核心方法
- **`_transform` / `_atransform`**: 内部实现的生成器方法。它遍历输入流中的每一个 chunk（字符串或消息），将其转换为 `Generation` 对象并调用 `parse_result`。
- **`transform` / `atransform`**: 公开的 LCEL 接口。它包装了内部转换逻辑，并确保与 `RunnableConfig` 兼容。

---

### 2. BaseCumulativeTransformOutputParser
**功能描述**: 累积式转换解析器基类。适用于需要随着上下文累积而更新解析结果的场景（例如逐步解析 JSON）。

#### 属性
| 属性名 | 类型 | 默认值 | 详细用途 |
| :--- | :--- | :--- | :--- |
| `diff` | `bool` | `False` | 如果为 `True`，流式输出将只返回与上一次解析结果的差异（Diff），而非完整的当前状态。 |

#### 核心方法
- **`_diff` (抽象方法)**: 计算两个解析结果之间的差异。子类（如 `JsonOutputParser`）需要实现此方法（例如使用 `jsonpatch`）。
- **`_transform` (重写)**:
    - **逻辑**: 维护一个累加器 `acc_gen`，将收到的每个 chunk 累加进去。
    - **解析**: 每次累加后调用 `parse_result(partial=True)` 进行部分解析。
    - **输出**: 如果解析结果发生变化，则 yield 新结果。如果 `diff=True`，则 yield 差异。

---

## 核心逻辑
1. **流式累加**: `BaseCumulativeTransformOutputParser` 利用了 `GenerationChunk` 的加法操作（`+`），将细碎的流式块拼接成一个逻辑上完整的输出。
2. **部分解析**: 通过向 `parse_result` 传递 `partial=True`，告知解析器当前输入可能是不完整的，解析器应尽可能返回当前已确定的部分。
3. **差异计算**: 在流式输出 JSON 等复杂结构时，返回完整的对象可能会导致带宽浪费。`diff` 模式允许仅发送增量更新。

---

## 使用示例

### 累积解析逻辑演示（伪代码）
```python
# 假设我们正在解析一个流式 JSON: {"a": 1, "b": 2}
# 接收到第一个块: {"a": 1
# 解析结果: {"a": 1}

# 接收到第二个块: , "b": 2}
# 累加结果: {"a": 1, "b": 2}
# 解析结果: {"a": 1, "b": 2}

# 如果 diff=False: 输出两次结果 {"a": 1} 和 {"a": 1, "b": 2}
# 如果 diff=True: 输出第一次 {"a": 1}，第二次输出 diff 操作 (例如添加键 "b")
```

---

## 注意事项
- **Chunk 类型匹配**: 在流式处理中，输入块必须是可加的（如 `BaseMessageChunk`）。解析器会自动处理消息到 Chunk 的转换。
- **性能开销**: 累积式解析意味着每收到一个块都要重新尝试解析。对于非常长的输出或复杂的解析逻辑，这可能会带来一定的 CPU 开销。

---

## 内部调用关系
- 该模块是 `JsonOutputParser` 的核心基石，赋予了它处理不完整 JSON 字符串的能力。
- `StrOutputParser` 也继承自 `BaseTransformOutputParser`，虽然它不需要累积逻辑。

---

## 元信息
- **最后更新时间**: 2026-01-29
- **对应源码版本**: LangChain Core v1.2.7
