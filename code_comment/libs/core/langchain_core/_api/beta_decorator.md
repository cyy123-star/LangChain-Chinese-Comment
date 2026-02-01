# Beta 装饰器

`beta_decorator.py` 是 LangChain 内部使用的工具模块，用于将 API 标记为 Beta 版本。它通过装饰器在运行时发出警告，并自动更新文档字符串。

## 元数据
- **最后更新时间**: 2026-01-29
- **源版本**: LangChain Core v1.2.7

## 文件概述
该文件提供了一个 `@beta` 装饰器，用于告知用户某个功能（函数、类或属性）目前处于 Beta 阶段。Beta 功能意味着它仍在开发中，其 API 可能会在没有任何预警的情况下发生变化。

!!! warning "内部使用"
    此模块仅供 LangChain 内部开发使用。普通用户不应在自己的代码中使用这些工具。

## 导入依赖
- `warnings`: 用于发出 Python 标准警告。
- `functools`: 用于保持装饰器包装后的函数元数据（`wraps`）。
- `inspect`: 用于检查对象属性和文档字符串。
- `langchain_core._api.internal`: 用于判断调用者是否为 LangChain 内部代码。

## 类与函数详解

### 核心函数

#### `beta(*, message="", name="", obj_type="", addendum="")`
标记一个函数、类或属性为 Beta 版本的装饰器。

| 参数名 | 类型 | 默认值 | 描述 |
| :--- | :--- | :--- | :--- |
| `message` | `str` | `""` | 覆盖默认的警告消息。 |
| `name` | `str` | `""` | 对象名称（默认为自动获取）。 |
| `obj_type` | `str` | `""` | 对象类型（类、函数、属性等）。 |
| `addendum` | `str` | `""` | 追加到警告消息末尾的额外文本。 |

**返回值**: 一个装饰器函数。

#### `warn_beta(*, message="", name="", obj_type="", addendum="")`
手动发出标准化的 Beta 警告。

#### `suppress_langchain_beta_warning()`
上下文管理器，用于在特定代码块内忽略 `LangChainBetaWarning`。

### 异常类

- `LangChainBetaWarning`: 继承自 `DeprecationWarning`，专门用于 Beta 功能的警告类别。

## 核心逻辑解读

1. **自动文档更新**: 装饰器会自动在对象的 `__doc__` 中插入 `.. beta::` 指令。这在生成 Sphinx 或 MkDocs 文档时非常有用。
2. **内部调用过滤**: 如果检测到调用者是 LangChain 内部模块（通过 `is_caller_internal()` 判断），则不会发出警告。这避免了内部组件互相调用时产生大量干扰日志。
3. **单次警告**: 每个被标记的 API 在运行期间通常只会发出一次警告（通过 `warned` 闭包变量控制）。
4. **多样化支持**:
   - **类**: 装饰类的 `__init__` 方法。
   - **属性 (Property)**: 装饰 getter, setter 和 deleter。
   - **异步函数**: 支持 `async def` 函数。

## 使用示例 (内部开发参考)

```python
from langchain_core._api import beta

@beta()
def new_experimental_feature():
    """这是一个新功能。"""
    pass

# 调用时会发出 LangChainBetaWarning
new_experimental_feature()
```

## 注意事项
- **装饰器顺序**:
  - 对于 `@classmethod` 或 `@staticmethod`，`@beta` 应该在**下方**（即先标记原始函数）。
  - 对于 `@property`，`@beta` 应该在**上方**。
- **继承限制**: 如果将 Beta 类作为多重继承的基类，该类**必须**显式定义 `__init__` 方法，否则装饰器可能会破坏继承链。
