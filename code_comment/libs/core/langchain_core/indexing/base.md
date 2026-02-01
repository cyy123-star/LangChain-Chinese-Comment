# libs\core\langchain_core\indexing\base.py

`libs\core\langchain_core\indexing\base.py` 定义了 LangChain 索引系统的基础抽象类和接口。索引系统主要用于管理文档在向量数据库（VectorStore）中的增量更新和删除。

## 文件概述

该文件主要职责是提供一个通用的索引抽象层，包括：
1. **RecordManager**: 记录管理器，用于跟踪哪些文档已被写入向量库及其写入时间。
2. **DocumentIndex**: 文档索引接口，扩展了 `BaseRetriever`，增加了 `upsert` 和 `delete` 操作。
3. **响应模型**: 定义了索引操作的返回值结构（`UpsertResponse`, `DeleteResponse`）。

通过这些抽象，LangChain 的索引 API 可以支持多种向量库，实现避免重复索引、自动删除过期文档等功能。

## 导入依赖

| 模块 | 作用 |
| :--- | :--- |
| `abc` | 提供抽象基类（ABC）支持。 |
| `time` | 用于获取系统时间戳。 |
| `typing` | 提供类型注解支持（`Sequence`, `Any`, `TypedDict`）。 |
| `langchain_core._api` | 提供 `beta` 装饰器，标记实验性 API。 |
| `langchain_core.retrievers` | 导入 `BaseRetriever` 基类。 |
| `langchain_core.run_in_executor` | 用于将同步操作在执行器中异步运行。 |

## 类与函数详解

### 1. RecordManager (抽象基类)

记录管理器的核心职责是维护文档哈希值与时间戳的映射，以决定是否需要更新文档。

#### 功能描述
作为所有记录管理器的接口，它定义了增删改查记录的标准方法。它依赖于单调递增的时间戳来判断文档的新旧程度。

#### 方法说明

| 方法 | 功能描述 | 参数 | 返回值 |
| :--- | :--- | :--- | :--- |
| `create_schema` | 创建数据库表结构 | 无 | `None` |
| `get_time` | 获取服务器的高精度时间戳 | 无 | `float` |
| `update` | 插入或更新记录 | `keys` (键列表), `group_ids` (可选组ID), `time_at_least` (最小时间验证) | `None` |
| `exists` | 检查指定的键是否存在 | `keys` (键列表) | `list[bool]` |
| `list_keys` | 根据条件列出键 | `before`, `after`, `group_ids`, `limit` (过滤条件) | `list[str]` |
| `delete_keys` | 删除指定的记录 | `keys` (键列表) | `None` |

*注：以上方法均有对应的异步版本（如 `aupdate`, `aexists` 等）。*

---

### 2. InMemoryRecordManager

`RecordManager` 的内存实现版本，主要用于测试或小型非持久化场景。

#### 功能描述
使用 Python 字典 (`self.records`) 在内存中存储记录。记录格式为 `{'group_id': str, 'updated_at': float}`。

#### 注意事项
- 无法跨进程或在程序重启后持久化数据。
- `get_time` 使用 `time.time()`，在多节点分布式系统中可能会存在时钟漂移问题。

---

### 3. DocumentIndex (抽象基类, Beta)

文档索引接口，继承自 `BaseRetriever`。

#### 功能描述
定义了支持索引操作的检索器接口。除了查询（`get_relevant_documents`）外，还支持 `upsert` 和 `delete`。

#### 方法说明

| 方法 | 功能描述 | 参数 | 返回值 |
| :--- | :--- | :--- | :--- |
| `upsert` | 插入或更新文档 | `items`: `Sequence[Document]`, `**kwargs` | `UpsertResponse` |
| `delete` | 根据 ID 或其他准则删除文档 | `ids`: `list[str]`, `**kwargs` | `DeleteResponse` |

---

### 4. 响应模型 (TypedDict)

#### UpsertResponse
| 字段 | 类型 | 描述 |
| :--- | :--- | :--- |
| `succeeded` | `list[str]` | 成功索引的 ID 列表。 |
| `failed` | `list[str]` | 索引失败的 ID 列表。 |

#### DeleteResponse
| 字段 | 类型 | 描述 |
| :--- | :--- | :--- |
| `num_deleted` | `int` | 实际删除的条目数。 |
| `succeeded` | `Sequence[str]` | 成功删除的 ID 列表。 |
| `failed` | `Sequence[str]` | 删除失败的 ID 列表。 |
| `num_failed` | `int` | 删除失败的条目数。 |

## 核心逻辑

1. **增量索引**: 索引 API 会为每个文档计算哈希。
2. **状态核对**: 检查 `RecordManager`。如果哈希已存在且时间戳较新，则跳过；否则写入向量库并更新 `RecordManager`。
3. **清理陈旧文档**: 通过 `list_keys(before=...)` 找到在当前索引任务之前存在的旧文档 ID，并从向量库和记录管理器中同步删除。

## 使用示例

```python
from langchain_core.indexing import InMemoryRecordManager, UpsertResponse
from langchain_core.documents import Document

# 1. 初始化记录管理器
record_manager = InMemoryRecordManager(namespace="test_ns")
record_manager.create_schema()

# 2. 模拟索引操作
keys = ["doc_1_hash", "doc_2_hash"]
record_manager.update(keys, group_ids=["source_1", "source_1"])

# 3. 检查存在性
exists = record_manager.exists(["doc_1_hash", "non_existent"])
print(exists)  # [True, False]
```

## 注意事项

1. **时钟同步**: `RecordManager` 严重依赖时间戳。在生产环境中，应确保所有节点与服务器时钟同步，否则可能导致意外的数据清理。
2. **原子性**: `RecordManager` 与 `VectorStore` 是分离的。如果写入向量库成功但更新记录管理器失败，系统会处于不一致状态。
3. **ID 管理**: 建议用户显式指定文档 ID，否则 `upsert` 自动生成的 ID 可能会导致难以追踪失败项。

## 内部调用关系

- `RecordManager` 被 `langchain.indexes.index` 函数调用，用于协调同步逻辑。
- `DocumentIndex` 通常由具体的向量库子类实现（如 `ElasticsearchStore` 等）。

## 相关链接

- [LangChain 索引官方概念指南](https://python.langchain.com/docs/modules/data_connection/indexing)
- [BaseRetriever 源码](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/core/langchain_core/retrievers.py)

最后更新时间：2026-01-29
对应源码版本：LangChain Core v1.2.7
