# RunnableBranch 详解

## 文件概述
`RunnableBranch` 是 LangChain 表达式语言 (LCEL) 中的核心组件之一，用于实现基于条件的逻辑分支。它允许根据输入动态选择执行不同的 `Runnable` 路径。

在 LangChain 框架中，`RunnableBranch` 扮演着类似编程语言中 `if-elif-else` 结构的角色，是构建复杂、具有决策能力的链条（Chains）的关键工具。

---

## 导入依赖
- `AsyncIterator`, `Awaitable`, `Callable`, `Iterator`, `Mapping`, `Sequence`: 标准类型注解，用于定义接口和数据结构。
- `BaseModel`, `ConfigDict`: 来自 Pydantic，用于数据验证和配置。
- `Runnable`, `RunnableLike`, `RunnableSerializable`, `coerce_to_runnable`: `langchain_core` 的基础运行单元及其转换工具。
- `RunnableConfig`, `ensure_config`, `patch_config`: 用于管理运行时的配置和回调。

---

## 类与函数详解

### `RunnableBranch` 类
`RunnableBranch` 继承自 `RunnableSerializable`，表示它可以被序列化并在运行时根据条件执行分支。

#### 初始化 `__init__`
```python
def __init__(self, *branches: Union[tuple[Condition, RunnableLike], RunnableLike]) -> None:
```

**参数说明**
| 参数名 | 类型 | 默认值 | 是否必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `*branches` | 变长参数 | - | 是 | 包含多个 `(condition, runnable)` 元组，以及最后一个作为默认执行路径的 `RunnableLike` 对象。 |

**功能描述**
- 接收一系列条件分支和一个默认分支。
- 至少需要两个参数（一个分支 + 一个默认路径）。
- 会自动将 `Callable` 或 `Mapping` 转换为 `Runnable` 对象（通过 `coerce_to_runnable`）。

#### 核心方法 `invoke` / `ainvoke`
这两个方法分别用于同步和异步执行分支逻辑。

**核心逻辑**
1. **初始化配置**：确保配置对象存在，并获取回调管理器。
2. **触发回调**：调用 `on_chain_start` 标记链开始。
3. **条件匹配**：
   - 遍历 `branches` 列表中的每一项。
   - 调用 `condition.invoke(input)` 评估条件是否成立。
   - 如果条件为 `True`，则执行对应的 `runnable.invoke(input)`。
   - 如果所有条件都不满足，执行 `default.invoke(input)`。
4. **错误处理**：捕获异常并通知回调管理器。
5. **结束回调**：执行完毕后调用 `on_chain_end`。

#### 流式方法 `stream` / `astream`
支持以流的形式返回分支执行的结果。

---

## 使用示例

```python
from langchain_core.runnables import RunnableBranch

# 定义一个分支逻辑：
# 1. 如果输入是字符串，则转换为大写
# 2. 如果输入是整数，则加 1
# 3. 否则，返回 "unknown"
branch = RunnableBranch(
    (lambda x: isinstance(x, str), lambda x: x.upper()),
    (lambda x: isinstance(x, int), lambda x: x + 1),
    lambda x: "unknown"
)

# 测试示例
print(branch.invoke("hello"))  # 输出: "HELLO"
print(branch.invoke(10))       # 输出: 11
print(branch.invoke(3.14))     # 输出: "unknown"
```

---

## 注意事项
- **评估顺序**：条件是按顺序评估的，一旦发现第一个满足的分支，就会执行该分支并跳过后续所有分支（包括默认分支）。
- **默认分支**：最后一个参数必须是默认分支，不能是条件元组。
- **输入一致性**：所有分支（包括条件和执行体）接收到的输入是完全相同的。
- **性能影响**：条件评估本身也是 `Runnable` 调用，如果条件逻辑过于复杂，可能会增加延迟。

---

## 内部调用关系
- **与 `coerce_to_runnable` 关系**：在初始化时，`RunnableBranch` 使用此函数确保所有输入（函数、字典等）都被包装为统一的 `Runnable` 接口。
- **与回调系统关系**：通过 `patch_config` 为每个条件评估和分支执行注入子回调（子标签如 `condition:1`, `branch:1` 等），方便在可视化工具（如 LangSmith）中追踪。

---

## 相关链接
- [LangChain 官方文档 - RunnableBranch](https://python.langchain.com/docs/expression_language/how_to/routing)
- [源码引用: base.py](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/core/langchain_core/runnables/base.py)

---
最后更新时间: 2026-01-29
对应源码版本: LangChain Core v1.2.7
