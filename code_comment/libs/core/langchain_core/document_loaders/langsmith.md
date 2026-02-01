# langchain_core.document_loaders.langsmith

`langchain_core.document_loaders.langsmith` 模块提供了将 LangSmith 数据集中的示例加载为 `Document` 对象的加载器。

## 文件概述

- **角色**: LangSmith 数据集成加载器。
- **主要职责**: 从 LangSmith 平台抓取数据集（Dataset）中的示例，并将其转换为 LangChain 标准的 `Document` 格式。
- **所属模块**: `langchain_core.document_loaders`

## 导入依赖

- `langsmith`: LangSmith 官方 SDK。
- `langchain_core.document_loaders.base`: 导入 `BaseLoader` 基类。
- `langchain_core.documents`: 导入 `Document` 定义。

## 类与函数详解

### 1. LangSmithLoader
- **功能描述**: 用于加载 LangSmith 数据集。它将示例的输入作为文档的 `page_content`，并将整个示例（包括输出和元数据）存入文档的 `metadata`。
- **设计目的**: 方便开发者快速将线上收集的真实数据转化为少样本（Few-shot）提示词的示例池。
- **参数说明**:
  | 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
  | :--- | :--- | :--- | :--- | :--- |
  | `dataset_id` | `UUID | str` | `None` | 否 | 目标数据集的 ID。 |
  | `dataset_name` | `str` | `None` | 否 | 目标数据集的名称（与 `dataset_id` 二选一）。 |
  | `content_key` | `str` | `""` | 否 | 指定输入字典中的哪个键作为 `page_content`。支持嵌套键（如 `"first.second"`）。 |
  | `format_content` | `Callable` | `None` | 否 | 将提取的内容转换为字符串的函数。默认为 JSON 序列化。 |
  | `limit` | `int` | `None` | 否 | 最大加载示例数量。 |
  | `offset` | `int` | `0` | 否 | 分页起始偏移量。 |
  | `client` | `LangSmithClient` | `None` | 否 | 可选的 LangSmith 客户端实例。 |

### 2. _stringify(x)
- **功能描述**: 内部辅助函数，用于将输入数据转换为字符串。如果输入是字典，则进行格式化的 JSON 序列化。

## 核心逻辑

- **嵌套键提取**: 通过 `content_key`（如 `a.b.c`），加载器能自动从嵌套的字典结构中提取深层字段作为文档内容。
- **元数据保留**: 加载器会自动处理 Pydantic 模型和特殊类型（如 UUID、datetime），确保元数据可以被正确序列化。

## 使用示例

```python
from langchain_core.document_loaders import LangSmithLoader

# 从名为 "my-dataset" 的数据集加载，并将 inputs["input_text"] 作为文档内容
loader = LangSmithLoader(
    dataset_name="my-dataset",
    content_key="input_text",
    limit=50
)

for doc in loader.lazy_load():
    print(f"内容: {doc.page_content}")
    print(f"元数据: {doc.metadata.keys()}")
```

## 注意事项

- **身份认证**: 使用此加载器前，需确保已正确配置 `LANGSMITH_API_KEY` 等环境变量。
- **内存安全**: 对于大型数据集，请务必使用 `lazy_load` 方法。

## 内部调用关系

- **LangSmith Client**: 内部调用 `list_examples` API。
- **Serializable**: 利用 LangChain 的序列化工具处理元数据。

## 相关链接
- [LangSmith 官方文档](https://docs.smith.langchain.com/)

---
- **最后更新时间**: 2026-01-29
- **对应源码版本**: LangChain Core v1.2.7
