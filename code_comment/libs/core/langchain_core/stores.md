# stores.py - 键值存储接口与实现

- **最后更新时间**: 2026-01-29
- **对应源码版本**: LangChain Core v1.2.7

## 文件概述

`stores.py` 定义了 LangChain 中用于数据持久化和缓存的基础键值存储接口 `BaseStore`。它提供了一套标准的 CRUD 操作规范，支持批量处理和异步操作。此外，该模块还包含了内存中的基础实现 `InMemoryStore`。这些存储组件广泛应用于 LLM 响应缓存、向量数据库持久化以及长短期记忆管理。

## 导入依赖

| 依赖模块 | 作用 |
| :--- | :--- |
| `abc` | 提供抽象基类支持。 |
| `collections.abc` | 提供迭代器和序列类型提示。 |
| `typing` | 提供泛型支持（`Generic`, `TypeVar`）。 |
| `langchain_core.runnables` | 提供 `run_in_executor` 用于在异步环境中运行同步方法。 |

## 类详解

### 1. BaseStore (ABC, Generic[K, V])

键值存储的抽象接口。

#### 功能描述
`BaseStore` 旨在抽象不同存储后端（如 Redis, SQLite, 内存等）的细节。它强制使用批量操作（`mget`, `mset`, `mdelete`），这在处理网络存储时能显著提高效率。

#### 方法说明

| 方法名 | 类型 | 参数 | 返回值 | 功能描述 |
| :--- | :--- | :--- | :--- | :--- |
| `mget` | 抽象方法 | `keys: Sequence[K]` | `list[V \| None]` | 批量获取键值。 |
| `mset` | 抽象方法 | `pairs: Sequence[tuple[K, V]]` | `None` | 批量设置键值。 |
| `mdelete` | 抽象方法 | `keys: Sequence[K]` | `None` | 批量删除键。 |
| `yield_keys` | 抽象方法 | `prefix: str = None` | `Iterator[K]` | 迭代匹配前缀的键。 |
| `amget` | 异步方法 | `keys: Sequence[K]` | `list[V \| None]` | `mget` 的异步版本。 |
| `ayield_keys`| 异步方法 | `prefix: str = None` | `AsyncIterator[K]` | `yield_keys` 的异步版本。 |

#### 核心逻辑
- **泛型设计**: 支持任意类型的键 `K` 和值 `V`。常用的别名 `ByteStore` 固定为 `BaseStore[str, bytes]`。
- **异步适配**: 默认情况下，异步方法通过 `run_in_executor` 调用同步实现。高性能子类应覆盖这些方法以提供原生异步支持。

---

### 2. InMemoryBaseStore (BaseStore[str, V])

基于 Python 字典的内存键值存储实现。

#### 功能描述
一个简单的、非持久化的存储实现，适用于测试、简单缓存或生命周期仅限于当前进程的场景。

#### 核心逻辑
- 内部使用 `self.store: dict[str, V]` 存储数据。
- 覆盖了异步方法以直接调用同步逻辑，避免不必要的线程切换开销。

#### 使用示例

```python
from langchain_core.stores import InMemoryStore

# 创建存储实例
store = InMemoryStore()

# 批量设置
store.mset([("key1", "value1"), ("key2", "value2")])

# 批量获取
values = store.mget(["key1", "key3"])
print(values)  # ['value1', None]

# 迭代键
for key in store.yield_keys(prefix="key"):
    print(f"找到键: {key}")

# 批量删除
store.mdelete(["key1"])
```

#### 注意事项
- **线程安全**: `InMemoryBaseStore` 并没有内置复杂的锁机制，但在大多数简单的批量操作中，依赖 Python 字典的原子性通常是安全的。
- **持久化**: 该实现不提供持久化功能，程序重启后数据将丢失。

## 内部调用关系

- **别名**: `ByteStore` 被广泛用于 `LocalFileStore` 等二进制数据存储。
- **集成**: 常被用于 `CacheBackedEmbeddings`（缓存嵌入向量）或 `EncoderBackedStore`（带序列化的存储）。

## 相关链接
- [BaseCache 源码文档](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/core/langchain_core/caches.md)
- [run_in_executor 源码文档](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/core/langchain_core/runnables/utils.md)
