# libs\core\langchain_core\indexing\api.py

`libs\core\langchain_core\indexing\api.py` 包含了将文档索引到向量库（Vector Store）的核心逻辑。

## 文件概述

该模块是 LangChain 索引系统的核心实现，提供了 `index` 和 `aindex` 函数。其主要职责包括：
1. **文档哈希**: 为文档内容和元数据生成确定性的唯一 ID。
2. **去重**: 在单次批处理中以及跨批处理进行文档去重。
3. **状态同步**: 与 `RecordManager` 交互，跟踪已索引文档的状态。
4. **清理逻辑**: 根据配置的模式（增量、全量等）自动删除陈旧文档。
5. **批处理**: 支持高效的批量处理，减少与向量库和数据库的交互次数。

## 导入依赖

| 模块 | 作用 |
| :--- | :--- |
| `hashlib` | 提供 SHA-1, SHA-256 等哈希算法支持。 |
| `json` | 用于序列化元数据以便进行哈希。 |
| `uuid` | 用于生成基于哈希的 UUID。 |
| `langchain_core.documents` | 导入 `Document` 类。 |
| `langchain_core.indexing.base` | 导入 `RecordManager` 和 `DocumentIndex` 抽象。 |
| `langchain_core.vectorstores` | 导入 `VectorStore` 基类。 |

## 类与函数详解

### 1. index (核心函数)

将来自加载器（Loader）的数据索引到向量库中。

#### 功能描述
这是索引系统的主要入口。它通过 `RecordManager` 确保只有新增或变更的文档被写入向量库，并根据 `cleanup` 模式管理过期文档的删除。

#### 参数说明

| 参数 | 类型 | 默认值 | 必填 | 描述 |
| :--- | :--- | :--- | :--- | :--- |
| `docs_source` | `BaseLoader \| Iterable[Document]` | - | 是 | 文档来源。 |
| `record_manager` | `RecordManager` | - | 是 | 用于跟踪文档状态的记录管理器。 |
| `vector_store` | `VectorStore \| DocumentIndex` | - | 是 | 目标向量库或文档索引。 |
| `batch_size` | `int` | `100` | 否 | 索引时的批次大小。 |
| `cleanup` | `str` | `None` | 否 | 清理模式：`incremental`, `full`, `scoped_full` 或 `None`。 |
| `source_id_key` | `str \| Callable` | `None` | 否 | 用于标识文档原始来源的键或函数。 |
| `force_update` | `bool` | `False` | 否 | 即使文档已存在也强制更新（适用于更新 Embeddings）。 |
| `key_encoder` | `str \| Callable` | `"sha1"` | 否 | 哈希算法（建议使用 `sha256`）。 |

#### 返回值解释
返回 `IndexingResult` (TypedDict)，包含以下字段：
- `num_added`: 新增文档数。
- `num_updated`: 更新的文档数。
- `num_deleted`: 删除的文档数。
- `num_skipped`: 跳过的文档数（内容未变）。

---

### 2. 清理模式 (Cleanup Modes)

| 模式 | 描述 | 适用场景 |
| :--- | :--- | :--- |
| `None` | 不删除任何文档。 | 仅追加数据的场景。 |
| `incremental` | 实时清理。删除与当前处理的 `source_id` 相关但未出现在当前批次中的旧文档。 | 持续更新大型数据集，且能明确 `source_id` 的场景。 |
| `full` | 全量清理。在所有文档索引完成后，删除 `RecordManager` 中存在但此次任务未触达的所有文档。 | 确保索引与数据源完全同步，且加载器能返回全量数据的场景。 |
| `scoped_full` | 范围全量清理。仅针对此次任务中见过的 `source_id` 进行全量清理。 | 适合无法一次性加载全量数据，但能按来源（如按文件）分批处理的场景。 |

---

### 3. 辅助函数

- `_get_document_with_hash`: 计算文档的哈希值并将其赋值给 `document.id`。哈希通常基于 `page_content` 和序列化后的 `metadata`。
- `_calculate_hash`: 实现具体的哈希算法（sha1, sha256, blake2b 等）。
- `_batch` / `_abatch`: 将迭代器切分为指定大小的块。

## 核心逻辑

1. **计算哈希**: 使用 `key_encoder` 为每个文档生成唯一的、确定性的 ID。
2. **批处理循环**:
   - **去重**: 移除当前批次内重复的文档。
   - **状态检查**: 询问 `RecordManager` 哪些 ID 已存在。
   - **过滤**: 跳过已存在且内容未变的文档。
   - **写入**: 将新文档/变更文档写入 `VectorStore`。
   - **更新状态**: 在 `RecordManager` 中记录当前的写入操作及时间戳。
   - **实时清理**: 如果是 `incremental` 模式，执行局部清理。
3. **收尾清理**: 如果是 `full` 或 `scoped_full` 模式，在循环结束后执行删除操作。

## 使用示例

```python
from langchain_core.indexing import index, InMemoryRecordManager
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document

# 准备组件
vec_store = InMemoryVectorStore(...)
record_manager = InMemoryRecordManager(namespace="my_app")
record_manager.create_schema()

# 待索引文档
docs = [
    Document(page_content="Content 1", metadata={"source": "file1.txt"}),
    Document(page_content="Content 2", metadata={"source": "file1.txt"}),
]

# 执行增量索引
result = index(
    docs,
    record_manager,
    vec_store,
    cleanup="incremental",
    source_id_key="source"
)

print(result) # {'num_added': 2, 'num_updated': 0, 'num_skipped': 0, 'num_deleted': 0}
```

## 注意事项

1. **SHA-1 警告**: 默认使用 SHA-1，它不是抗碰撞的。对于安全性要求高的应用，请显式指定 `key_encoder="sha256"`。
2. **Full 模式风险**: 在 `full` 模式下，如果加载器只返回了部分数据，索引中其余的文档会被**全部删除**。请务必确认加载器返回的是完整数据集。
3. **原子性缺失**: 写入向量库和更新记录管理器不是原子操作。如果中途崩溃，可能需要重新运行索引。
4. **性能建议**: 尽量使用较大的 `batch_size`（如 100-1000），以减少网络往返开销。

## 相关链接

- [RecordManager 接口定义](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/core/langchain_core/indexing/base.md)
- [VectorStore 接口源码](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/core/langchain_core/vectorstores/base.py)

最后更新时间：2026-01-29
对应源码版本：LangChain Core v1.2.7
