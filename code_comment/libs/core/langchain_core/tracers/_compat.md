# libs\core\langchain_core\tracers\_compat.py

## 文件概述

`_compat.py` 是一个内部兼容性工具模块，专门用于处理 Pydantic v1 和 v2 版本在 LangSmith `Run` 对象上的差异。由于 LangSmith 的对象（如 `Run` 和 `Example`）会同步迁移，该模块提供了一组统一的 API 来执行字典转换、对象复制和构造操作。

## 导入依赖

- `langchain_core.tracers.schemas.Run`: 导入 LangSmith 的运行模型。
- `typing`: 提供类型提示和 `TypeVar` 支持。

## 类与函数详解

### 1. run_to_dict
- **功能描述**: 将 `Run` 对象转换为字典，自动适配 Pydantic v1 (`dict()`) 和 v2 (`model_dump()`)。
- **参数说明**:
| 参数名 | 类型 | 默认值 | 是否必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `run` | `Run` | - | 是 | 要转换的 Run 对象。 |
| `**kwargs` | `Any` | - | 否 | 传递给 Pydantic 转换方法的额外参数。 |
- **返回值**: `dict[str, Any]`，对象的字典表示。

### 2. run_copy
- **功能描述**: 复制 `Run` 对象，适配 Pydantic v1 (`copy()`) 和 v2 (`model_copy()`)。
- **参数说明**:
| 参数名 | 类型 | 默认值 | 是否必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `run` | `Run` | - | 是 | 要复制的 Run 对象。 |
| `**kwargs` | `Any` | - | 否 | 传递给 Pydantic 复制方法的额外参数。 |
- **返回值**: `Run`，对象的副本。

### 3. run_construct
- **功能描述**: 在不进行校验的情况下构造 `Run` 对象，适配 Pydantic v1 (`construct()`) 和 v2 (`model_construct()`)。
- **参数说明**:
| 参数名 | 类型 | 默认值 | 是否必填 | 详细用途 |
| `**kwargs` | `Any` | - | 否 | 要设置在对象上的字段属性。 |
- **返回值**: `Run`，新构造的 Run 实例。

### 4. pydantic_to_dict / pydantic_copy
- **功能描述**: 通用的 Pydantic 对象转换和复制工具。它们通过检查 `Run` 模型的 Pydantic 版本来决定使用哪种方法。
- **适用场景**: 专门用于与 `Run` 对象一同迁移的 LangSmith 相关模型。

## 核心逻辑

1. **版本探测**: 在模块导入时，通过 `hasattr(Run, "model_dump")` 静态探测当前 `Run` 类使用的是 Pydantic v1 还是 v2。
2. **分支处理**: 所有工具函数内部都根据探测到的版本标志 `_RUN_IS_PYDANTIC_V2` 走不同的代码路径。

## 使用示例

```python
from langchain_core.tracers.schemas import Run
from langchain_core.tracers._compat import run_to_dict

# 无论安装的是 pydantic v1 还是 v2，都能正确工作
run_obj = Run(...)
run_dict = run_to_dict(run_obj)
```

## 注意事项

- **专用性**: 该模块仅推荐用于 LangSmith 相关的对象处理。对于通用的 Pydantic 版本兼容，应使用 `langchain_core.utils.pydantic`。
- **内部工具**: 主要供 LangChain 内部的追踪器和 LangSmith 集成逻辑使用。

---
最后更新时间: 2026-01-29
对应源码版本: LangChain Core v1.2.7
