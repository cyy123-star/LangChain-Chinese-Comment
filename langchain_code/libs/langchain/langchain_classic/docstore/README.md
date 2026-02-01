# Docstore (文档存储)

`docstore` 模块提供了一个轻量级的接口，用于按 ID 检索文档。它通常作为 `VectorStore` 的补充，用于在相似度搜索后获取完整的文档内容。

## 核心接口

### `Docstore`
定义了 `search(id)` 方法，通过唯一的 ID 查找并返回 `Document` 对象。

## 常见实现

| 实现类 | 说明 |
| :--- | :--- |
| `InMemoryDocstore` | 在内存中使用字典（Dict）存储文档，适合小规模应用。 |
| `Wikipedia` | 将维基百科作为一个动态文档库，通过页面标题（Title）进行检索。 |
| `ArbitraryFnDocstore` | 允许用户传入一个自定义函数来实现检索逻辑。 |

## 使用示例

```python
from langchain.docstore import InMemoryDocstore
from langchain_core.documents import Document

doc = Document(page_content="Hello world", metadata={"id": "1"})
docstore = InMemoryDocstore({"1": doc})

# 检索
result = docstore.search("1")
```

## 注意事项

- **已弃用/迁移**: 随着 `BaseStore` (位于 `storage` 模块) 的引入，许多传统的 `Docstore` 用例已被更通用的存储接口所取代。
- **与向量库配合**: 在许多 RAG 实现中，向量库只存储向量和 ID，而完整的文本内容则存储在 `Docstore` 中以节省内存。
