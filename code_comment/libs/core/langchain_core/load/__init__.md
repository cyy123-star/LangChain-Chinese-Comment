# __init__.py (load)

## 文件概述
`load` 模块是 LangChain 序列化系统的核心入口，提供了将 LangChain 对象（如 Chains, Prompts, Messages 等）转换为 JSON 格式（序列化）以及从 JSON 格式恢复（反序列化）的统一接口。

## 导入依赖
| 模块 | 作用 |
| :--- | :--- |
| `langchain_core._import_utils` | 提供动态属性导入工具 `import_attr`。 |
| `langchain_core.load.load` | 导入核心反序列化函数 `load`。 |

## 核心接口
该模块导出了以下关键类和函数：
- **`load`**: 从字典/对象中恢复 LangChain 对象的物理实例。
- **`loads`**: 从 JSON 字符串中恢复 LangChain 对象。
- **`dumpd`**: 将 LangChain 对象转换为可序列化的字典（包含版本和命名空间信息）。
- **`dumps`**: 将 LangChain 对象转换为 JSON 字符串。
- **`Serializable`**: 所有可序列化对象的基类。
- **`InitValidator`**: 用于反序列化过程中的参数验证逻辑。

## 动态导入机制
该模块使用了 `__getattr__` 钩子来实现延迟导入（Lazy Loading），从而优化启动性能。
- **映射关系**:
  - `dumpd`, `dumps` -> 来自 `load.dump`
  - `InitValidator`, `loads` -> 来自 `load.load`
  - `Serializable` -> 来自 `load.serializable`

## 注意事项
- **命名冲突处理**: 模块内显式地从 `langchain_core.load.load.py` 导入了 `load` 函数，以避免包名与文件名冲突导致的循环引用或导入错误。
- **推荐用法**: 用户应优先使用 `from langchain_core.load import load, dumpd` 这种顶层导入方式。

## 相关链接
- [序列化逻辑 (dump.py)](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/core/langchain_core/load/dump.md)
- [反序列化逻辑 (load.py)](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/core/langchain_core/load/load.md)
- [序列化基类 (serializable.py)](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/core/langchain_core/load/serializable.md)

---
最后更新时间: 2026-01-29
对应源码版本: LangChain Core v1.2.7
