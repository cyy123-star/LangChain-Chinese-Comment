# Deprecation 弃用工具

`deprecation.py` 是 LangChain 内部用于管理 API 弃用周期的核心工具。它提供了标准的装饰器和警告机制，引导用户从旧 API 迁移到新 API。

## 元数据
- **最后更新时间**: 2026-01-29
- **源版本**: LangChain Core v1.2.7

## 文件概述
该模块模仿了知名库（如 matplotlib）的弃用管理机制。它允许开发者标记不再推荐使用的函数、类、属性甚至参数，并提供迁移建议和预期的删除版本。

!!! warning "内部使用"
    此模块主要供 LangChain 维护者使用。

## 导入依赖
- `warnings`: 发出 `DeprecationWarning` 或 `PendingDeprecationWarning`。
- `pydantic`: 支持对 Pydantic v1 和 v2 字段的弃用标记。
- `langchain_core._api.internal`: 用于过滤内部调用产生的警告。

## 类与函数详解

### 核心装饰器

#### `deprecated(since, *, message="", name="", alternative="", alternative_import="", pending=False, obj_type="", addendum="", removal="", package="")`
标记 API 为已弃用的装饰器。

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `since` | `str` | 开始弃用的版本号（如 `"0.1.0"`）。 |
| `alternative` | `str` | 推荐的替代 API 名称。 |
| `alternative_import` | `str` | 替代 API 的完整导入路径。 |
| `removal` | `str` | 计划删除的版本号。 |
| `pending` | `bool` | 如果为 `True`，则视为“待弃用”（不立即警告）。 |

**返回值**: 装饰器函数。

#### `rename_parameter(*, since, removal, old, new)`
标记函数参数更名的装饰器。如果用户使用了旧参数名，会发出警告并自动将值赋给新参数。

### 警告类别

- `LangChainDeprecationWarning`: 标准弃用警告。
- `LangChainPendingDeprecationWarning`: 待定弃用警告（用于提前通知）。

### 辅助函数

- `warn_deprecated`: 手动发出弃用警告。
- `suppress_langchain_deprecation_warning`: 上下文管理器，用于暂时屏蔽此类警告。

## 核心逻辑解读

1. **多维度支持**: 
   - 支持类、普通函数、类方法、属性（property）。
   - 特别支持 **Pydantic 字段**：可以直接装饰 `Field` 定义。
2. **IDE 友好**: 
   - 装饰器会根据 PEP 702 设置 `__deprecated__` 属性，使 IDE（如 VS Code, PyCharm）能直接在代码中显示删除线或提示。
3. **文档自动标注**: 
   - 自动在 `__doc__` 中插入 `!!! deprecated` 指令，告知用户弃用信息及替代方案。
4. **智能消息构建**: 
   - 如果提供了 `alternative_import`，警告消息会自动提示用户如何使用 `pip install` 安装新包并进行导入。
5. **内部过滤**: 
   - 与 Beta 装饰器类似，如果调用发生在 LangChain 内部，警告会被静默，以减少开发时的干扰。

## 使用示例

```python
from langchain_core._api import deprecated

@deprecated("0.1.0", alternative="NewClass", removal="0.3.0")
class OldClass:
    pass

@deprecated("0.1.0", alternative_import="langchain_community.tools.NewTool")
def old_function():
    pass
```

## 注意事项
- **移除版本策略**: 对于 `langchain` 核心包，通常遵循严格的语义化版本控制。
- **参数校验**: 不能同时指定 `pending=True` 和 `removal` 版本（因为待定弃用还没有明确的删除计划）。
- **装饰器顺序**: 
  - 对于属性，`@deprecated` 必须在 `@property` **上方**。
  - 对于静态方法/类方法，`@deprecated` 必须在 `@staticmethod`/`@classmethod` **下方**。
