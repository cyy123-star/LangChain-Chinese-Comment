# langchain_core/runnables/passthrough.py

`RunnablePassthrough` 是 LangChain 中一个非常实用的组件，主要用于在 LCEL（LangChain 表达式语言）链中传递数据、透传输入或在不改变原有输入的情况下添加新字段。

## 文件概述

该文件实现了 `RunnablePassthrough` 类和 `RunnableAssign` 类。它们是构建复杂链的关键工具，尤其是在需要将前一步的输出原样传递给后一步，或者在处理字典输入时动态添加新键值的场景中。

## 导入依赖

| 依赖模块 | 作用 |
| :--- | :--- |
| `langchain_core.runnables.base` | 导入 `Runnable`, `RunnableParallel` 等基类。 |
| `langchain_core.runnables.config` | 提供配置处理和函数调用辅助工具（如 `ensure_config`）。 |
| `langchain_core.utils.aiter` | 处理异步迭代器。 |

## 类与函数详解

### RunnablePassthrough

透传输入或添加新键值的可运行对象。

#### 功能描述
`RunnablePassthrough` 的核心作用是“原样通过”。它可以作为链中的一个占位符，或者通过其 `assign` 静态方法，在保持原始字典输入不变的同时，计算并合并新的键值对。

#### 参数说明
| 参数名 | 类型 | 默认值 | 是否必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `func` | `Callable` | `None` | 否 | 在数据透传时执行的同步副作用函数。 |
| `afunc` | `Callable` | `None` | 否 | 在数据透传时执行的异步副作用函数。 |
| `input_type` | `type` | `None` | 否 | 指定输入的类型。 |

#### 核心方法：`assign`
`assign` 是一个类方法，用于创建一个 `RunnableAssign` 对象。它接收关键字参数，每个参数对应一个 `Runnable` 或函数，用于计算并向输入的字典中添加新的键。

### RunnableAssign

由 `RunnablePassthrough.assign` 创建的专用类。

#### 功能描述
专门用于处理 `dict` 类型的输入，将输入字典与计算得到的新字典合并。

## 使用示例

### 1. 基本透传
```python
from langchain_core.runnables import RunnablePassthrough

# 输入什么，输出就是什么
passthrough = RunnablePassthrough()
print(passthrough.invoke("hello"))  # 输出: "hello"
```

### 2. 在并行链中使用
```python
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

# 在计算新字段的同时保留原始输入
runnable = RunnableParallel(
    original=RunnablePassthrough(),
    plus_one=lambda x: x + 1
)
print(runnable.invoke(1))  # 输出: {'original': 1, 'plus_one': 2}
```

### 3. 使用 `assign` 动态添加字段
```python
from langchain_core.runnables import RunnablePassthrough

def get_length(text):
    return len(text)

# 假设输入是一个 dict
chain = RunnablePassthrough.assign(
    length=lambda x: get_length(x["input"])
)
print(chain.invoke({"input": "hello"})) 
# 输出: {'input': 'hello', 'length': 5}
```

## 注意事项

1. **输入类型限制**：使用 `assign` 方法时，输入必须是 `dict` 类型，否则在合并阶段会报错。
2. **副作用函数**：如果在构造函数中传入了 `func`，该函数会在数据通过时被调用（类似于监控或日志），但其返回值不会改变输出，输出依然是原始输入。
3. **性能影响**：`RunnablePassthrough` 本身开销极小，但在 `assign` 中执行复杂逻辑时仍需注意计算成本。

## 内部调用关系

- 继承自 [base.py](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/core/langchain_core/runnables/base.py) 中的 `RunnableSerializable`。
- `assign` 方法内部封装了 `RunnableParallel` 来并行执行新增字段的计算。

## 相关链接

- [LangChain 官方文档 - How to pass through arguments](https://python.langchain.com/docs/how_to/passthrough/)
- [源码文件: langchain_core/runnables/passthrough.py](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/core/langchain_core/runnables/passthrough.py)
- [术语表: TERMINOLOGY.md](file:///d:/TraeProjects/langchain_code_comment/TERMINOLOGY.md)

---
最后更新时间: 2026-01-29
对应源码版本: LangChain Core v1.2.7
