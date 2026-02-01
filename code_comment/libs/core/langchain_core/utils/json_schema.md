# libs\core\langchain_core\utils\json_schema.py

## 文件概述

`json_schema.py` 模块提供了处理 JSON Schema 的工具函数，核心功能是解析和展开（dereference）JSON Schema 中的 `$ref` 引用。这在处理复杂、嵌套或循环引用的模型定义时非常有用，例如将 Pydantic 模型生成的 Schema 转换为 LLM 可以理解的平铺结构。

## 导入依赖

- `copy.deepcopy`: 用于在处理过程中创建 Schema 的深拷贝，避免修改原始对象。
- `typing`: 提供类型提示和转换。

## 类与函数详解

### 1. dereference_refs
- **功能描述**: 解析并内联 JSON Schema 中的所有 `$ref` 引用。它能够处理简单引用、混合引用（带有额外属性的 `$ref`）以及循环引用。
- **参数说明**:
| 参数名 | 类型 | 默认值 | 是否必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `schema_obj` | `dict` | - | 是 | 要处理的 JSON Schema 对象或片段。 |
| `full_schema` | `dict \| None` | `None` | 否 | 包含所有定义的完整 Schema。如果不提供，默认使用 `schema_obj`。 |
| `skip_keys` | `Sequence[str] \| None` | `None` | 否 | 控制递归深度。如果为 `None`，则使用浅解析并跳过 `$defs`。 |
- **返回值**: `dict`，引用被内联后的新字典。

### 2. _dereference_refs_helper (内部函数)
- **功能描述**: `dereference_refs` 的核心递归实现。处理四种情况：带 `$ref` 的对象、普通字典、列表和原始值。
- **核心逻辑**:
    1. **循环检测**: 使用 `processed_refs` 集合记录当前正在处理的路径，发现循环时停止递归以防止死循环。
    2. **属性合并**: 对于混合引用（如 `{"$ref": "...", "description": "..."}`），将引用的内容与当前对象的其他属性合并，当前对象的属性优先级更高。

### 3. _retrieve_ref (内部函数)
- **功能描述**: 根据 JSON 指针（如 `#/definitions/MyType`）从 Schema 中检索具体对象。
- **异常处理**: 如果路径格式不正确（不以 `#` 开头）或找不到路径，会抛出 `ValueError` 或 `KeyError`。

## 使用示例

```python
from langchain_core.utils.json_schema import dereference_refs

schema = {
    "type": "object",
    "properties": {
        "user": {"$ref": "#/$defs/User"}
    },
    "$defs": {
        "User": {"type": "string"}
    }
}

# 展开后
resolved = dereference_refs(schema)
# resolved["properties"]["user"] 将变为 {"type": "string"}
```

## 注意事项

- **循环引用**: 该模块能优雅地处理循环引用，通过在循环点停止内联来保证程序的健壮性。
- **不可变性**: 函数返回的是深拷贝后的新对象，原始 `schema_obj` 不会被修改。
- **性能**: 对于极大型且高度嵌套的 Schema，全量展开可能会消耗较多内存。

---
最后更新时间: 2026-01-29
对应源码版本: LangChain Core v1.2.7
