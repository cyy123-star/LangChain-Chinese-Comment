# langchain_text_splitters.json

`json.py` 实现了针对 JSON 数据的递归切分。它能够在保持 JSON 层次结构的同时，将大型 JSON 对象拆分为更小的字典或 JSON 字符串块。

## **文件概述**
该文件定义了 `RecursiveJsonSplitter` 类。它不继承自 `TextSplitter`，因为它直接处理 Python 字典（JSON 对象）而非纯文本。它的目标是确保每个切分后的块都是有效的 JSON 结构，并且大小在指定范围内。

## **导入依赖**
- `json`: 用于序列化和反序列化。
- `langchain_core.documents.Document`: 标准文档对象。

## **类与函数详解**

### **RecursiveJsonSplitter (类)**
**功能描述**：递归地将 JSON 数据拆分为较小的、结构化的块。

#### **构造函数 `__init__`**
| 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `max_chunk_size` | `int` | `2000` | 否 | 每个块的最大字符长度（序列化后）。 |
| `min_chunk_size` | `int` | `None` | 否 | 每个块的最小字符长度。默认为 `max_chunk_size - 200`。 |

#### **核心方法**
- **`split_json(data: dict, convert_lists: bool = False) -> list[dict]`**:
    - **功能**: 执行切分，返回字典列表。
    - **参数**: `convert_lists` 若为 True，会将列表转换为以索引为键的字典，以便更好地递归切分。
- **`split_text(data: dict, convert_lists: bool = False) -> list[str]`**:
    - **功能**: 执行切分，并返回 JSON 字符串列表。
- **`create_documents(texts: list[dict], metadatas=None) -> list[Document]`**:
    - **功能**: 将切分后的 JSON 块转换为 `Document` 对象。

## **核心逻辑解析**
1. **层次保持**：切分器会尝试在字典的键值对之间进行拆分。如果一个嵌套字典太大，它会深入到该字典内部继续拆分，并保留从根部到该位置的路径。
2. **列表处理**：由于 JSON 列表很难在保持语义的情况下拆分，该类提供了 `_list_to_dict_preprocessing` 方法，将 `[a, b]` 转换为 `{"0": a, "1": b}`，从而允许在列表项之间进行拆分。
3. **大小控制**：在遍历过程中，它会不断计算当前块序列化后的长度。如果添加下一个键值对会超过 `max_chunk_size`，则开启一个新块。

## **使用示例**
```python
from langchain_text_splitters import RecursiveJsonSplitter

data = {
    "company": "LangChain",
    "products": [
        {"name": "Chain", "description": "Lego-like building blocks for LLMs"},
        {"name": "Agent", "description": "Autonomous entities that use LLMs"},
        {"name": "LangSmith", "description": "Debugging and monitoring platform"}
    ],
    "locations": ["San Francisco", "Remote"]
}

# 初始化切分器
splitter = RecursiveJsonSplitter(max_chunk_size=100)

# 执行切分
chunks = splitter.split_json(data)

for i, chunk in enumerate(chunks):
    print(f"Chunk {i}: {chunk}")
```

## **注意事项**
- 该切分器处理的是 Python `dict` 对象。如果你有 JSON 字符串，需要先用 `json.loads()` 解析。
- 默认情况下，如果一个值本身的大小就超过了 `max_chunk_size`（且不可再分，如一个极长的字符串），它可能会产生超过限制的块。
- 对于包含深层嵌套且需要作为 RAG 上下文的数据，`RecursiveJsonSplitter` 优于简单的文本切分，因为它保留了数据的结构含义。

## **相关链接**
- [Python json 模块](https://docs.python.org/3/library/json.html)
- [Text Splitter 基类接口](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/text-splitters/langchain_text_splitters/base.md)
