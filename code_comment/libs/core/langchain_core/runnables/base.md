# libs\core\langchain_core\runnables\base.py

## 文件概述

`base.py` 是 LangChain 核心库中的关键文件，定义了 **Runnable** 协议及其相关基类。它是 **LCEL (LangChain Expression Language)** 的基石，提供了一套统一的接口，使得不同的组件（如提示词模板、模型、输出解析器等）可以像乐高积木一样通过 `|` 操作符进行自由组合、并行执行和流式处理。

主要职责包括：
1. 定义所有可运行对象的基类 `Runnable`。
2. 实现可序列化的运行对象基类 `RunnableSerializable`。
3. 提供组合多个 Runnable 的序列化类 `RunnableSequence`。
4. 提供并行执行多个 Runnable 的类 `RunnableParallel`。
5. 定义标准的同步与异步调用接口（invoke, batch, stream 等）。

## 导入依赖

| 模块/类 | 作用 |
| :--- | :--- |
| `abc.ABC`, `abstractmethod` | 用于定义抽象基类和抽象方法，强制子类实现核心接口。 |
| `asyncio` | 提供异步编程支持，用于实现 `ainvoke`, `abatch` 等异步方法。 |
| `pydantic.BaseModel` | 用于数据验证和设置，支持 Runnable 的输入输出 Schema 定义。 |
| `langchain_core._api.beta_decorator` | 用于标记处于 Beta 阶段的 API。 |
| `langchain_core.runnables.config` | 提供运行时的配置管理（如 `RunnableConfig`）。 |

## 类与函数详解

### 1. Runnable (基类)

#### 功能描述
`Runnable` 是所有可运行组件的抽象基类。它定义了处理输入并产生输出的标准协议。通过继承此类，组件可以自动获得批处理、异步、流式传输和组合能力。

#### 核心方法

##### `invoke`
将单个输入转换为输出。

- **参数说明**
| 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `input` | `Input` | - | 是 | 传递给 Runnable 的输入数据。 |
| `config` | `RunnableConfig` | `None` | 否 | 运行时配置，包含 tags, metadata, callbacks 等。 |
| `**kwargs` | `Any` | - | 否 | 传递给底层实现的额外参数。 |

- **返回值解释**
返回 `Output` 类型，代表处理后的结果。

##### `batch`
并行处理多个输入。

- **参数说明**
| 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `inputs` | `list[Input]` | - | 是 | 输入数据列表。 |
| `config` | `RunnableConfig \| list` | `None` | 否 | 单个配置或与输入对应的配置列表。 |
| `return_exceptions` | `bool` | `False` | 否 | 如果为 True，遇到异常时返回异常对象而非抛出。 |

- **返回值解释**
返回 `list[Output]`，处理后的结果列表。

##### `stream`
流式返回处理结果。

- **参数说明**
| 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `input` | `Input` | - | 是 | 输入数据。 |
| `config` | `RunnableConfig` | `None` | 否 | 运行时配置。 |

- **返回值解释**
返回 `Iterator[Output]`，逐步产生输出块。

---

### 2. RunnableSerializable

#### 功能描述
继承自 `Serializable` 和 `Runnable`，为 Runnable 增加了序列化能力。这使得 Runnable 对象可以被保存、加载并在不同的环境中传输。

---

### 3. RunnableSequence

#### 功能描述
代表一系列按顺序执行的 Runnable 对象。前一个 Runnable 的输出将作为后一个 Runnable 的输入。

- **核心逻辑**：
  1. 接收一个 Runnable 列表。
  2. 在调用时，依次执行列表中的每个组件。
  3. 处理中间步骤的追踪和回调透传。

---

### 4. RunnableParallel

#### 功能描述
并发执行多个 Runnable 对象。它通常接收一个字典，字典的键是输出的字段名，值是对应的 Runnable。

- **核心逻辑**：
  1. 将相同的输入分发给所有并行的 Runnable。
  2. 使用线程池（同步）或 `asyncio.gather`（异步）并发执行。
  3. 将结果汇总成一个字典。

## 核心逻辑解读

### 1. 运算符重载 (`|`)
`Runnable` 类通过重载 `__or__` 和 `__ror__` 运算符实现了声明式的链式组合。
- 当执行 `step1 | step2` 时，实际上是创建了一个 `RunnableSequence([step1, step2])`。
- 这种设计使得代码非常直观，类似于 Unix 管道。

### 2. 自动异步转换
如果子类只实现了同步的 `invoke` 而没有实现 `ainvoke`，`Runnable` 基类提供了一个默认实现，它会使用 `run_in_executor` 在线程池中运行同步代码，从而保证了异步接口的可用性。

## 使用示例

```python
from langchain_core.runnables import RunnableLambda

# 定义简单逻辑
add_one = RunnableLambda(lambda x: x + 1)
mul_two = RunnableLambda(lambda x: x * 2)

# 组合成链
chain = add_one | mul_two

# 调用
print(chain.invoke(2))  # 输出: 6 (2+1=3, 3*2=6)

# 并行执行
parallel_chain = add_one | {
    "original": RunnableLambda(lambda x: x),
    "multiplied": mul_two
}
print(parallel_chain.invoke(2)) # 输出: {'original': 3, 'multiplied': 6}
```

## 注意事项

1. **配置透传**：在自定义 Runnable 时，务必将 `config` 透传给内部调用的组件，否则会导致追踪信息丢失。
2. **状态安全**：Runnable 应该是无状态的。如果需要存储状态，应考虑使用 `RunnableConfig` 中的 `metadata` 或外部存储。
3. **并发限制**：在使用 `batch` 或 `RunnableParallel` 时，可以通过 `config` 中的 `max_concurrency` 限制并发数，防止资源耗尽。

## 内部调用关系

- `Runnable` 通过 `RunnableConfig` 与回调系统 (`CallbackManager`) 交互。
- `RunnableSequence` 内部维护一个 `list[Runnable]`。
- `RunnableParallel` 内部维护一个 `dict[str, Runnable]`。

## 相关链接

- [LangChain 官方文档 - Expression Language (LCEL)](https://python.langchain.com/docs/expression_language/)
- [源码文件: langchain_core/runnables/base.py](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/core/langchain_core/runnables/base.py)
- [术语表: TERMINOLOGY.md](file:///d:/TraeProjects/langchain_code_comment/TERMINOLOGY.md)

---
最后更新时间: 2026-01-29
对应源码版本: LangChain Core v1.2.7
