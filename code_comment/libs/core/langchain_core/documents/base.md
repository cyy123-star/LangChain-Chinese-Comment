# BaseMedia, Blob & Document

## 文件概述
`base.py` 定义了 LangChain 数据检索和处理流程中的核心数据结构：`BaseMedia`、`Blob` 和 `Document`。

这些类是 **数据检索和处理工作流** 的基础：
- **`BaseMedia`**: 提供统一的 `id` 和 `metadata` 字段的基类。
- **`Blob`**: 表示原始数据（文件、二进制数据），主要供文档加载器（Document Loaders）使用，实现数据加载与解析的解耦。
- **`Document`**: 表示文本内容及其关联元数据，是 RAG、向量存储和语义搜索的核心单元。

!!! note "注意：不用于 LLM 聊天消息"
    这些类用于数据处理管道，而非 LLM 的 I/O 交互。对于聊天消息中的多模态内容（如对话中的图像、音频），请使用 `langchain.messages` 中的内容块（Content Blocks）。

## 导入依赖
- `pydantic.Field`, `pydantic.model_validator`: 用于数据验证和模型定义。
- `langchain_core.load.serializable.Serializable`: 提供序列化支持，确保对象可以跨进程或持久化存储。
- `io.BytesIO`, `io.BufferedReader`: 用于处理二进制流数据。

## 类与函数详解

### 1. BaseMedia
**功能描述**: 所有检索和数据处理内容的抽象基类，提供统一的元数据管理。

#### 核心属性
| 参数名 | 类型 | 默认值 | 是否必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `id` | `str \| None` | `None` | 否 | 文档的唯一标识符。未来版本可能会变为必填。 |
| `metadata` | `dict` | `{}` | 否 | 与内容关联的任意元数据字典。 |

---

### 2. Blob
**功能描述**: 对原始数据的抽象。它可以代表内存中的字节/字符串，也可以代表文件系统中的引用。其设计灵感来自 [Mozilla 的 Blob API](https://developer.mozilla.org/en-US/docs/Web/API/Blob)。

#### 核心属性
| 参数名 | 类型 | 默认值 | 详细用途 |
| :--- | :--- | :--- | :--- |
| `data` | `bytes \| str \| None` | `None` | 原始数据内容。 |
| `mimetype` | `str \| None` | `None` | 数据的 MIME 类型。 |
| `encoding` | `str` | `"utf-8"` | 将字节解码为字符串时使用的编码。 |
| `path` | `str \| PurePath \| None` | `None` | 原始内容所在的路径。 |

#### 核心方法
- **`as_string()`**: 将数据读取为字符串。如果是文件路径，则读取文件内容。
- **`as_bytes()`**: 将数据读取为字节数组。
- **`as_bytes_io()`**: 返回一个字节流上下文管理器（`BytesIO` 或 `BufferedReader`）。
- **`from_path(path, ...)`**: 类方法，从指定路径创建一个 `Blob` 实例（不会立即加载数据）。
- **`from_data(data, ...)`**: 类方法，从内存数据创建一个 `Blob` 实例。

---

### 3. Document
**功能描述**: 存储文本片段及其关联元数据的核心类。它是 LangChain 中最常用的数据类型之一。

#### 核心属性
| 参数名 | 类型 | 是否必填 | 详细用途 |
| :--- | :--- | :--- | :--- |
| `page_content` | `str` | 是 | 文档的文本内容。 |
| `metadata` | `dict` | 否 | 关联的元数据（如来源、页码、作者等）。继承自 `BaseMedia`。 |
| `id` | `str \| None` | 否 | 文档的唯一 ID。继承自 `BaseMedia`。 |

#### 使用示例
```python
from langchain_core.documents import Document

# 创建一个简单的文档
doc = Document(
    page_content="这是文档的核心内容。",
    metadata={"source": "manual", "page": 1}
)

print(doc.page_content)
print(doc.metadata["source"])
```

#### 注意事项
- **序列化**: `Document` 继承自 `Serializable`，这意味着它可以被序列化为 JSON 格式，方便存储到向量数据库或通过 API 传输。
- **字符串表示**: 重写了 `__str__` 方法，仅显示 `page_content` 和 `metadata`，以确保在将对象直接传入 Prompt 时保持简洁。

## 内部调用关系
- **继承链**: `Blob` 和 `Document` 均继承自 `BaseMedia`，而 `BaseMedia` 继承自 `Serializable`。
- **协作关系**: `Blob` 通常由 `DocumentLoader` 生成，经过解析器（Parser）处理后转化为 `Document` 对象，再进入索引（Indexing）或检索（Retrieval）环节。

## 相关链接
- [LangChain 官方文档 - Documents](https://python.langchain.com/docs/modules/data_connection/documents/)
- [源码文件](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/core/langchain_core/documents/base.py)

---
最后更新时间: 2026-01-29
对应源码版本: LangChain Core v1.2.7
