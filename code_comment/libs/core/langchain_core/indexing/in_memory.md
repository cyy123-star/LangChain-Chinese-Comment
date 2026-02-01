# libs\core\langchain_core\indexing\in_memory.py

`libs\core\langchain_core\indexing\in_memory.py` 提供了一个内存中的文档索引实现 `InMemoryDocumentIndex`。

## 文件概述

该文件实现了一个简单的、基于内存的文档存储和检索系统。它继承自 `DocumentIndex`，将文档存储在 Python 字典中。它主要用于：
- 快速原型开发和测试。
- 演示 `DocumentIndex` 接口的使用。
- 在不需要持久化或高性能向量搜索的小规模场景下使用。

其搜索逻辑非常简单：基于查询字符串在文档内容中出现的次数进行排序。

## 导入依赖

| 模块 | 作用 |
| :--- | :--- |
| `uuid` | 用于为没有 ID 的文档生成唯一标识符。 |
| `pydantic` | 提供 `Field` 支持，用于模型定义。 |
| `langchain_core.documents` | 导入 `Document` 类。 |
| `langchain_core.indexing.base` | 导入 `DocumentIndex` 基类及响应模型。 |

## 类与函数详解

### 1. InMemoryDocumentIndex (Beta)

内存文档索引类。

#### 功能描述
将文档存储在内存字典中 (`store: dict[str, Document]`)。它支持基本的 CRUD 操作和简单的关键词计数检索。

#### 属性说明
- `store`: 存储 ID 到 `Document` 对象的映射。
- `top_k`: 检索时返回的最大文档数量，默认为 4。

#### 方法说明

| 方法 | 功能描述 | 参数 | 返回值 |
| :--- | :--- | :--- | :--- |
| `upsert` | 插入或更新文档。如果文档没有 ID，则自动生成 UUID。 | `items`: 文档序列 | `UpsertResponse` |
| `delete` | 根据 ID 列表从内存中删除文档。 | `ids`: ID 列表 | `DeleteResponse` |
| `get` | 根据 ID 列表获取文档。 | `ids`: ID 序列 | `list[Document]` |
| `_get_relevant_documents` | 检索逻辑：计算查询词在 `page_content` 中出现的次数并排序。 | `query`: 查询字符串 | `list[Document]` |

## 核心逻辑

1. **Upsert 流程**:
   - 遍历每个文档。
   - 如果文档 `id` 为空，使用 `uuid.uuid4()` 生成一个新 ID，并复制文档对象设置该 ID。
   - 将 ID 存入 `self.store` 字典。
   - 返回所有成功的 ID。

2. **检索流程 (Keyword Counting)**:
   - 遍历 `self.store` 中的所有文档。
   - 调用 `document.page_content.count(query)` 计算查询词出现的频率。
   - 按频率从高到低排序。
   - 返回前 `top_k` 个文档的副本。

## 使用示例

```python
from langchain_core.indexing.in_memory import InMemoryDocumentIndex
from langchain_core.documents import Document

# 1. 初始化索引
index = InMemoryDocumentIndex()

# 2. 插入文档
doc1 = Document(page_content="LangChain is great for AI apps.", id="1")
doc2 = Document(page_content="AI is the future.")
index.upsert([doc1, doc2])

# 3. 简单检索
results = index.get_relevant_documents("AI")
for doc in results:
    print(f"ID: {doc.id}, Content: {doc.page_content}")

# 4. 删除
index.delete(ids=["1"])
```

## 注意事项

1. **非向量检索**: 该实现**不是**向量检索（Vector Search）。它不使用嵌入（Embeddings）或余弦相似度，仅基于字符串匹配计数。
2. **易失性**: 数据存储在内存中，程序结束即丢失。
3. **性能**: 对于大规模文档集，遍历所有文档进行字符串计数会非常缓慢。
4. **并发性**: 该实现未显式处理线程安全问题，在多线程环境下需注意。

## 内部调用关系

- 继承自 `DocumentIndex` 并实现了其所有抽象方法。
- 使用 `uuid` 模块处理自动 ID 生成。

## 相关链接

- [DocumentIndex 接口定义](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/core/langchain_core/indexing/base.md)
- [Document 类源码](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/core/langchain_core/documents/base.py)

最后更新时间：2026-01-29
对应源码版本：LangChain Core v1.2.7
