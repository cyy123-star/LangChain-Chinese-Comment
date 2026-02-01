# _merge.py - 字典与列表合并工具

## 文件概述

`_merge.py` 是 LangChain 内部使用的实用工具模块，主要负责深度合并字典、列表以及通用对象。它在处理 `BaseMessage` 的 `additional_kwargs`、流式输出的块（Chunks）合并以及复杂配置合并时发挥着核心作用。该模块支持递归合并，并能妥善处理 `None` 值和特定的 LangChain 内部索引逻辑。

## 导入依赖

| 依赖模块 | 作用 |
| :--- | :--- |
| `typing` | 提供类型注解支持（`Any`, `annotations`）。 |

## 函数详解

### 1. merge_dicts
- **功能描述**: 深度合并多个字典。支持递归处理嵌套字典，并能处理 `None` 值的覆盖逻辑。
- **参数说明**:
    | 参数名 | 类型 | 默认值 | 必填 | 描述 |
    | :--- | :--- | :--- | :--- | :--- |
    | `left` | `dict[str, Any]` | - | 是 | 基础字典（合并的起点）。 |
    | `*others` | `dict[str, Any]` | - | 否 | 待合并的其他一个或多个字典。 |
- **核心逻辑**:
    1. **冲突处理**: 如果 `left` 中的值为 `None` 且 `right` 中的值不为 `None`，则使用 `right` 的值。
    2. **类型检查**: 确保相同键在两个字典中的值类型一致（除非一方为 `None`）。
    3. **字符串合并**: 直接拼接字符串（如 `id`, `output_version` 等特定键除外，它们在值相等时跳过）。
    4. **递归合并**: 如果值是字典，则调用 `merge_dicts`；如果是列表，则调用 `merge_lists`。
    5. **数值处理**: 整数类型执行加法运算。
- **使用示例**:
    ```python
    from langchain_core.utils._merge import merge_dicts

    dict1 = {"a": 1, "b": {"c": "hello"}}
    dict2 = {"b": {"c": " world"}, "d": 2}
    merged = merge_dicts(dict1, dict2)
    # 结果: {'a': 1, 'b': {'c': 'hello world'}, 'd': 2}
    ```

### 2. merge_lists
- **功能描述**: 合并多个列表，特别支持根据 `index` 键进行智能合并。
- **参数说明**:
    | 参数名 | 类型 | 默认值 | 必填 | 描述 |
    | :--- | :--- | :--- | :--- | :--- |
    | `left` | `list \| None` | - | 是 | 基础列表。 |
    | `*others` | `list \| None` | - | 否 | 其他待合并列表。 |
- **核心逻辑**:
    - 遍历 `other` 列表中的元素。
    - 如果元素是具有 `index` 键的字典，则尝试在 `merged` 列表中寻找具有相同 `index` 的元素进行合并。
    - 这种逻辑常用于合并流式输出中的工具调用块（Tool Call Chunks），其中每个块通过 `index` 标识其在列表中的位置。
    - 特殊处理 `non_standard` 类型的消息块合并。

### 3. merge_obj
- **功能描述**: 通用对象合并入口，支持字符串、字典、列表以及支持相等比较的对象。
- **参数说明**:
    | 参数名 | 类型 | 默认值 | 必填 | 描述 |
    | :--- | :--- | :--- | :--- | :--- |
    | `left` | `Any` | - | 是 | 基础对象。 |
    | `right` | `Any` | - | 是 | 待合并对象。 |
- **返回值**: 合并后的对象。
- **核心逻辑**:
    - 如果任一对象为 `None`，返回非 `None` 的那个。
    - 根据对象类型转发给 `merge_dicts`、`merge_lists` 或执行字符串加法。
    - 如果两者相等则直接返回。

## 注意事项
- **类型一致性**: 合并过程中会严格检查类型，不同类型的对象合并会抛出 `TypeError`。
- **不可变性**: 函数内部通过 `left.copy()` 创建副本，不会修改原始字典。
- **特殊键处理**: 针对 `id`, `index`, `type` 等 LangChain 内部使用的特定键有特殊的合并规则（如跳过或特殊转换）。

## 相关链接
- [LangChain 消息合并逻辑](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/core/langchain_core/messages/base.md)

---
**最后更新时间**: 2026-01-29
**对应源码版本**: LangChain Core v1.2.7
