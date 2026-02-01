# mapping.py

## 文件概述
`mapping.py` 定义了 LangChain 序列化命名空间（`lc_namespace`）与实际代码路径之间的映射关系。其核心作用是确保在代码重构或模块移动后，旧版本序列化的对象仍能被正确地反序列化。

## 导入依赖
该文件仅包含 Python 字典定义，不依赖外部 LangChain 模块。

## 核心映射表

### `SERIALIZABLE_MAPPING`
- **类型**: `dict[tuple[str, ...], tuple[str, ...]]`
- **功能**: 主映射表。将序列化时使用的逻辑路径（通常以 `langchain` 开头）映射到当前的实际物理路径（通常以 `langchain_core` 或具体集成包开头）。
- **示例**:
  - `("langchain", "schema", "messages", "AIMessage")` -> `("langchain_core", "messages", "ai", "AIMessage")`
  - 这意味着原本在 `langchain.schema.messages` 下的 `AIMessage`，现在应从 `langchain_core.messages.ai` 加载。

### `_OG_SERIALIZABLE_MAPPING`
- **类型**: `dict[tuple[str, ...], tuple[str, ...]]`
- **功能**: 针对极早期 LangChain 版本的兼容性映射。处理那些甚至没有完整 schema 路径的旧对象。

### `OLD_CORE_NAMESPACES_MAPPING`
- **类型**: `dict[tuple[str, ...], tuple[str, ...]]`
- **功能**: 针对过渡期（曾短暂使用 `langchain_core` 作为序列化路径的版本）的兼容性映射。

## 核心逻辑
当 `load` 函数尝试恢复一个对象时，它会检查序列化数据中的 `lc_id`（命名空间元组）。
1. 首先在 `SERIALIZABLE_MAPPING` 中查找。
2. 如果未找到，依次检查 `_OG_SERIALIZABLE_MAPPING` 和 `OLD_CORE_NAMESPACES_MAPPING`。
3. 找到对应的目标路径后，使用 `importlib` 动态加载对应的类。

## 使用场景
- **跨版本兼容**: 升级 LangChain 版本后，读取旧的存储数据（如数据库中的 Prompt 或 Chain 配置）。
- **解耦物理路径**: 允许开发者在不破坏序列化兼容性的前提下，自由地重新组织代码结构。

## 注意事项
- **手动维护**: 这是一个需要手动维护的文件。每当 `Serializable` 子类发生移动时，都应在此添加对应的映射条目。
- **元组格式**: 映射的键和值都是字符串元组，代表 Python 的包/模块路径。

## 相关链接
- [Serializable 基类](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/core/langchain_core/load/serializable.md)
- [反序列化逻辑 (load.py)](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/core/langchain_core/load/load.md)

---
最后更新时间: 2026-01-29
对应源码版本: LangChain Core v1.2.7
