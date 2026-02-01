# Internal API (_api)

`_api` 模块是 LangChain 内部使用的辅助工具集，主要用于管理代码的演进、版本更迭以及对外的 API 兼容性。

> **警告**: 此模块及其子模块仅供 LangChain 内部开发使用。请勿在应用代码中直接引用其中的函数或类，因为这些接口可能会在没有任何通知的情况下发生变化。

## 核心功能

1. **弃用管理 (Deprecation)**:
   - 提供 `@deprecated` 装饰器，用于标记不再建议使用的类或函数。
   - 自动在用户调用已弃用接口时发出 `LangChainDeprecationWarning` 警告，并提供迁移建议。
   - 支持通过 `suppress_langchain_deprecation_warning` 上下文管理器临时关闭警告。

2. **动态导入 (Module Import)**:
   - 提供 `create_importer` 工具，用于实现模块的动态重定向。
   - 当用户尝试从旧路径导入已迁移的组件时，该工具可以拦截请求、发出警告，并从新位置加载对应的属性。
   - 这对于保证 `langchain` 根模块的干净以及实现“按需加载”至point。

3. **环境检测 (Interactive Env)**:
   - 能够检测当前运行环境是否为交互式环境（如 Jupyter Notebook 或 Python REPL）。
   - 在交互式环境中，通常会减少警告的输出频率，以避免干扰用户的自动补全和即时探索。

## 内部文件说明

- `deprecation.py`: 定义了所有的弃用警告类型、装饰器和控制逻辑。
- `module_import.py`: 核心的动态导入工厂，支持 `__getattr__` 模式的重定向。
- `interactive_env.py`: 简单的环境检测逻辑。
- `path.py`: 内部路径计算工具。
