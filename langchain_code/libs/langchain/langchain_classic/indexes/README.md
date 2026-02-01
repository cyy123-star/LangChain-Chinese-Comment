# Indexes (索引管理)

`indexes` 模块提供了一套用于管理向量数据库内容的工具，特别是解决“如何同步文档库与向量库”的问题。

## 核心价值

传统的向量库操作往往是“全量覆盖”或“盲目追加”，这会导致两个问题：
1. **内容重复**: 相同的文档被多次索引。
2. **数据陈旧**: 原始文档已删除或修改，但向量库中仍保留旧数据。

## 索引同步器 (Indexing API)

`langchain.indexes.index` 是一个强大的工具，支持三种模式：
- **None**: 仅添加新文档，不更新或删除。
- **Incremental**: 更新已修改的文档，跳过未变化的，不删除已消失的。
- **Full**: 确保向量库与当前文档库完全一致（添加新的，更新改动的，删除不再存在的）。

## 记录管理器 (Record Manager)

为了追踪文档的状态，索引系统需要一个 `RecordManager`（通常基于 SQL 数据库，如 SQLite 或 PostgreSQL）：
- 记录每个文档的哈希值（Hash）。
- 记录文档最后更新的时间。
- 记录文档与向量库 ID 的映射关系。

## 图谱索引 (Graph Indexes)

除了向量索引，该模块还包含了构建知识图谱（Knowledge Graph）的实验性功能：
- **实体提取**: 从文本中识别实体。
- **三元组生成**: 构建 (Subject, Predicate, Object) 关系。

## 使用示例

```python
from langchain.indexes import index

# 需要一个 RecordManager 和一个 VectorStore
# result = index(
#     docs_source,
#     record_manager,
#     vectorstore,
#     cleanup="incremental",
#     source_id_key="source"
# )
```

## 注意事项

- **生产推荐**: 在处理大规模、频繁更新的文档库时，使用 `Indexing API` 是保持 RAG 系统数据一致性的最佳实践。
- **元数据依赖**: 索引系统高度依赖文档的 `metadata`（尤其是 `source` 字段）来识别文档唯一性。
