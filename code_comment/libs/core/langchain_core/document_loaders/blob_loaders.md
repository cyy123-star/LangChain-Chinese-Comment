# langchain_core.document_loaders.blob_loaders

`langchain_core.document_loaders.blob_loaders` 模块定义了加载原始二进制数据（Blob）的抽象接口。

## 文件概述

- **角色**: 二进制数据加载抽象层。
- **主要职责**: 提供 `BlobLoader` 接口，用于从各种存储系统（如本地文件系统、S3 等）中检索原始数据。
- **所属模块**: `langchain_core.document_loaders`

## 导入依赖

- `abc`: 提供抽象基类支持。
- `typing`: 提供类型提示支持。
- `langchain_core.documents.base`: 导入 `Blob` 和 `PathLike` 定义。

## 类与函数详解

### 1. BlobLoader (抽象基类)
- **功能描述**: 定义了加载二进制大对象（Blob）的接口。它的目标是将“内容的加载”与“内容的解析”解耦。
- **核心方法**:
  - `yield_blobs()`: **抽象方法**。子类必须实现此方法，以生成器形式产出 `Blob` 对象。

## 核心逻辑

- **解耦设计**: `BlobLoader` 只负责获取原始字节流和元数据，不关心这些字节是 PDF、文本还是图像。具体的解析工作由 `BaseBlobParser` 完成。
- **惰性生成**: 通过 `yield_blobs` 返回迭代器，支持流式处理大量文件，而无需一次性读入内存。

## 使用示例

```python
from typing import Iterable
from langchain_core.document_loaders.blob_loaders import BlobLoader, Blob

class MyFileBlobLoader(BlobLoader):
    def yield_blobs(self) -> Iterable[Blob]:
        # 模拟从文件列表加载
        paths = ["file1.txt", "file2.pdf"]
        for path in paths:
            yield Blob.from_path(path)

loader = MyFileBlobLoader()
for blob in loader.yield_blobs():
    print(f"加载了 Blob: {blob.source}")
```

## 注意事项

- **反向兼容性**: 该模块重新导出了 `Blob` 和 `PathLike`，以确保旧代码能够正常运行。
- **资源管理**: 实现者应确保在 `yield_blobs` 过程中正确处理文件句柄或其他网络资源的释放。

## 内部调用关系

- **BaseBlobParser**: 通常与解析器配合使用。一个典型的流程是：`BlobLoader` 产生 `Blob` -> `BaseBlobParser` 将 `Blob` 转换为 `Document`。

## 相关链接
- [LangChain 官方文档 - Blob 和 BlobLoader](https://python.langchain.com/docs/modules/data_connection/document_loaders/custom_document_loader/#blob-loader)

---
- **最后更新时间**: 2026-01-29
- **对应源码版本**: LangChain Core v1.2.7
