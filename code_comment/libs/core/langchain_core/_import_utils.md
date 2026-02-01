# _import_utils.py - 动态导入工具

## 文件概述

`_import_utils.py` 是 LangChain 内部使用的一个小型实用工具模块，主要用于支持懒加载（Lazy Loading）和动态属性获取。它允许在包的 `__init__.py` 文件中通过自定义 `__getattr__` 方法来延迟加载子模块或类，从而减少包初始化的时间开销并避免循环导入。

## 导入依赖

| 依赖模块 | 作用 |
| :--- | :--- |
| `importlib.import_module` | 用于在运行时动态导入指定的 Python 模块。 |

## 函数详解

### 1. import_attr
- **功能描述**: 从指定包的模块中动态导入属性（类、函数或变量）。
- **参数说明**:
    | 参数名 | 类型 | 默认值 | 必填 | 描述 |
    | :--- | :--- | :--- | :--- | :--- |
    | `attr_name` | `str` | - | 是 | 要导入的属性名称。 |
    | `module_name` | `str \| None` | - | 否 | 属性所在的模块名。如果为 `None` 或 `"__module__"`，则尝试从包自身导入。 |
    | `package` | `str \| None` | - | 否 | 模块所属的包名。 |
- **返回值**: `object`。成功导入的属性对象。
- **核心逻辑**:
    1. **直接导入模块**: 如果 `module_name` 为空，则尝试导入名为 `package.attr_name` 的模块。
    2. **从模块获取属性**: 如果指定了 `module_name`，先导入该子模块，再使用 `getattr` 获取其中的属性。
    3. **异常处理**: 捕获 `ModuleNotFoundError` 并将其包装为更具描述性的 `ImportError` 或 `AttributeError`。
- **使用示例 (在 `__init__.py` 中)**:
    ```python
    # langchain_core/prompts/__init__.py
    from langchain_core._import_utils import import_attr

    def __getattr__(name: str):
        return import_attr(name, module_name="base", package=__package__)
    ```

## 注意事项
- **懒加载**: 这是实现 LangChain 大规模模块高效加载的关键技术之一。
- **调试限制**: 动态导入可能会使某些 IDE 的自动补全功能失效（除非配合 `TYPE_CHECKING` 使用）。

## 内部调用关系

该工具被广泛应用于 LangChain Core 各个子包的 `__init__.py` 文件中，用于管理导出属性。

---
**最后更新时间**: 2026-01-29
**对应源码版本**: LangChain Core v1.2.7
