# langchain_core.document_loaders.base

`langchain_core.document_loaders.base` 模块定义了 LangChain 中文档加载器的核心抽象接口。它规定了如何将外部数据源（如文件、数据库、API 等）加载并转换为统一的 `Document` 对象。

## 文件概述

- **角色**: 加载器抽象定义模块。
- **主要职责**: 提供 `BaseLoader` 和 `BaseBlobParser` 基类，确立同步与异步、即时与惰性加载的标准模式。
- **所属模块**: `langchain_core.document_loaders`

## 导入依赖

- `abc`: 提供抽象基类支持。
- `typing`: 提供类型提示支持（如 `Iterator`, `AsyncIterator`, `list`）。
- `langchain_core.runnables`: 导入 `run_in_executor` 用于实现异步惰性加载。
- `langchain_core.documents`: 导入 `Document` 和 `Blob` 定义。

## 类与函数详解

### 1. BaseLoader (基类)
- **功能描述**: 所有文档加载器的基类。它定义了如何从数据源获取数据并生成 `Document` 列表。
- **设计原则**: 实现者应优先实现 `lazy_load`（生成器模式），以避免一次性将所有文档加载进内存。
- **核心方法**:
  - `load()`: 即时加载所有文档并返回列表。默认调用 `list(self.lazy_load())`。
  - `aload()`: 异步即时加载。
  - `lazy_load()`: **核心实现点**。子类应重写此方法，以迭代器形式产出文档。
  - `alazy_load()`: 异步惰性加载。默认在执行器中运行同步的 `lazy_load`。
  - `load_and_split(text_splitter)`: 加载文档并立即使用指定的 `TextSplitter` 进行切分。

### 2. BaseBlobParser (抽象基类)
- **功能描述**: 定义了将二进制大对象（Blob）解析为 `Document` 的接口。
- **设计目的**: 将“如何获取数据”（Loader）与“如何理解数据内容”（Parser）解耦。
- **核心方法**:
  - `lazy_parse(blob)`: **抽象方法**。子类必须实现，将 `Blob` 解析为文档迭代器。
  - `parse(blob)`: 即时解析 `Blob`。

## 核心逻辑

- **惰性加载 (Lazy Loading)**: `BaseLoader` 强烈建议使用生成器模式。这对于处理数千个大文件或流式数据至关重要，能有效控制内存占用。
- **异步支持**: 默认的 `alazy_load` 使用 `run_in_executor` 封装同步迭代器。这意味着即使子类没有提供原生的 `async` 实现，框架也能在异步环境中非阻塞地运行加载任务。

## 使用示例

```python
from typing import Iterator
from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document

class MySimpleLoader(BaseLoader):
    def lazy_load(self) -> Iterator[Document]:
        # 模拟从某个地方读取数据
        yield Document(page_content="第一部分内容", metadata={"source": "local"})
        yield Document(page_content="第二部分内容", metadata={"source": "local"})

loader = MySimpleLoader()
for doc in loader.lazy_load():
    print(doc.page_content)
```

## 注意事项

- **切分器依赖**: `load_and_split` 依赖于 `langchain-text-splitters` 包。如果未安装，调用该方法将抛出 `ImportError`。
- **内存安全**: 除非确定数据量很小，否则在生产环境中应始终优先使用 `lazy_load` 而非 `load`。

## 内部调用关系

- **TextSplitter**: `load_and_split` 方法内部调用切分器的 `split_documents`。
- **VectorStores**: 向量数据库通常调用加载器的 `load` 或 `lazy_load` 来获取初始数据。

## 相关链接
- [LangChain 官方文档 - 文档加载器](https://python.langchain.com/docs/modules/data_connection/document_loaders/)

---
- **最后更新时间**: 2026-01-29
- **对应源码版本**: LangChain Core v1.2.7
