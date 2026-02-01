# Pydantic 实用工具模块文档

## 文件概述
`pydantic.py` 是 LangChain 中处理数据验证和模型转换的核心工具模块。它最重要的职责是提供一个**兼容层**，确保 LangChain 的核心功能能够同时在 Pydantic V1 和 V2 环境下无缝运行。该模块封装了版本检测、模型创建、字段提取以及针对 LangChain 特定需求的装饰器。

## 导入依赖
- `pydantic`: 基础验证库。
- `packaging.version`: 用于精确比较 Pydantic 的版本号。
- `typing_extensions`: 提供跨 Python 版本的类型支持（如 `deprecated`, `override`）。

---

## 核心常量与环境检测
- `PYDANTIC_MAJOR_VERSION`: 当前环境 Pydantic 的主版本号（1 或 2）。
- `IS_PYDANTIC_V1 / IS_PYDANTIC_V2`: 布尔标志，用于快速分支逻辑。
- `PydanticBaseModel`: 指向当前环境的 `BaseModel` 基类。

---

## 核心函数详解

### 1. is_basemodel_subclass / is_basemodel_instance
**功能描述**: 跨版本检查一个类是否是 Pydantic 的 `BaseModel` 子类或实例。它会同时检查 V1 的 `pydantic.v1.BaseModel` 和 V2 的 `pydantic.BaseModel`。

### 2. pre_init (装饰器)
**功能描述**: 允许在 Pydantic 模型实例化（`__init__`）之前运行自定义逻辑。这在需要根据输入动态调整字段值或处理别名时非常有用。
- **内部逻辑**: 封装了 `root_validator(pre=True)`，并自动处理了字段别名填充和默认值工厂的逻辑。

### 3. create_model_v2
**功能描述**: 动态创建一个 Pydantic 模型。
- **参数说明**:
    | 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
    | :--- | :--- | :--- | :--- | :--- |
    | `model_name` | `str` | - | 是 | 新模型的类名。 |
    | `field_definitions` | `dict` | `None` | 否 | 字段定义字典，格式为 `name: (type, default)`。 |
    | `root` | `Any` | `None` | 否 | 如果提供，则创建 `RootModel`。 |
- **核心逻辑**: 自动处理保留关键字（如 `model_` 开头的字段名）的重映射，并利用缓存机制（`_create_model_cached`）提升性能。

### 4. get_fields
**功能描述**: 统一获取 Pydantic 模型的所有字段信息。
- **返回值**: 在 V2 中返回 `model_fields`，在 V1 中返回 `__fields__`。

---

## 内部辅助逻辑

### `_remap_field_definitions`
Pydantic V2 保护了许多以 `model_` 开头的名称。该函数会自动将这些名称重映射为 `private_` 前缀，并设置 `alias`，从而允许用户继续使用这些受保护的名称作为输入键，而不触发 Pydantic 的内部冲突。

### `_IgnoreUnserializable`
一个自定义的 JSON Schema 生成器，用于在生成模型的 JSON Schema 时忽略无法序列化的类型，防止抛出异常。

---

## 使用示例

### 1. 跨版本检查
```python
from langchain_core.utils.pydantic import is_basemodel_subclass
from pydantic import BaseModel

class MyModel(BaseModel):
    pass

print(is_basemodel_subclass(MyModel)) # True (无论 Pydantic 是 V1 还是 V2)
```

### 2. 使用 pre_init
```python
from langchain_core.utils.pydantic import pre_init, BaseModel

class MyModel(BaseModel):
    a: int

    @pre_init
    def validate_a(cls, values):
        if "a" not in values:
            values["a"] = 1
        return values
```

## 注意事项
- **延迟加载**: 许多核心功能（如模型创建）使用了缓存，以减少频繁反射带来的性能损耗。
- **弃用警告**: 部分 Pydantic V1 的功能（如 `root_validator`）在 V2 环境下会触发弃用警告，该模块通过 `warnings.filterwarnings` 进行了内部处理。
- **内部 API**: 带有下划线前缀的函数（如 `_create_subset_model`）主要供 LangChain 内部组件使用，外部集成时应谨慎。

## 相关链接
- [Pydantic V2 迁移指南](https://docs.pydantic.dev/latest/migration/)
- [Pydantic 官方文档](https://docs.pydantic.dev/)

---
**最后更新时间**: 2026-01-29
**对应源码版本**: LangChain Core v1.2.7
