# VectorStores 初始化模块文档

## 文件概述
`__init__.py` 是 `langchain_core.vectorstores` 模块的入口文件。它采用了**延迟导入（Lazy Import）**机制，定义了该模块公开导出的核心类和类型，主要包括向量存储基类及其检索器实现。这种设计旨在减少初始加载时间并避免循环依赖。

## 导入依赖
- `langchain_core._import_utils`: 提供 `import_attr` 工具，用于实现属性的动态导入。

## 类与类型导出

### 核心组件
该模块统一导出了以下核心组件：

- **`VectorStore`**: 所有向量数据库实现的抽象基类。
- **`VectorStoreRetriever`**: 将向量存储包装为 `BaseRetriever` 的类，用于 LCEL 链中。
- **`InMemoryVectorStore`**: 官方提供的轻量级内存向量存储实现。
- **`VST`**: 用于类型提示的泛型变量，代表 `VectorStore` 的子类。

## 核心逻辑

### 延迟导入机制
模块通过覆盖 `__getattr__` 和 `__dir__` 函数实现了延迟加载：

1. **`__getattr__(attr_name)`**:
    - 当用户尝试访问模块属性（如 `from langchain_core.vectorstores import VectorStore`）时，该函数会被触发。
    - 它根据 `_dynamic_imports` 映射表，查找属性所在的子模块（如 `base` 或 `in_memory`）。
    - 调用 `import_attr` 动态加载该属性，并将其注入到 `globals()` 中，确保后续访问不再触发动态导入。

2. **`__dir__()`**:
    - 返回模块所有公开导出的属性名称列表，支持 IDE 的代码补全功能。

## 使用示例
```python
# 推荐的导入方式
from langchain_core.vectorstores import VectorStore, InMemoryVectorStore

# 只有在执行上述代码时，对应的 base.py 或 in_memory.py 才会被真正加载
```

## 注意事项
- **代码补全**: 虽然使用了延迟导入，但由于定义了 `__dir__` 和 `__all__`，现代 IDE（如 PyCharm, VS Code）仍能提供完美的自动补全支持。
- **性能优化**: 这种模式在大规模框架中非常常见，有助于提升应用程序的启动速度。

## 相关链接
- [Python __getattr__ 官方文档](https://docs.python.org/3/reference/datamodel.html#customizing-attribute-access)
- [LangChain 架构概览](https://python.langchain.com/docs/get_started/introduction)

---
**最后更新时间**: 2026-01-29
**对应源码版本**: LangChain Core v1.2.7
