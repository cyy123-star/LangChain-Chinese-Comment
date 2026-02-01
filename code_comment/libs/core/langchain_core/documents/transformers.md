# BaseDocumentTransformer

## 文件概述
`transformers.py` 定义了 `BaseDocumentTransformer` 抽象基类。它用于对一系列文档进行 **结构化转换**。与压缩器（Compressor）不同，转换器通常更通用，不一定依赖于查询上下文，常见的操作包括文本拆分（Splitting）、格式转换、提取元数据或过滤冗余。

## 导入依赖
- `abc.ABC`, `abc.abstractmethod`: 定义接口规范。
- `langchain_core.runnables.config.run_in_executor`: 用于支持异步调用。

## 类与函数详解
### 1. BaseDocumentTransformer
**功能描述**: 文档转换器的抽象基类。它接受一组文档并返回转换后的另一组文档。

#### 核心方法
- **`transform_documents(documents, **kwargs)`**:
    - **功能**: 执行转换逻辑的核心同步方法。
    - **参数**: 
        - `documents`: 待转换的文档序列。
        - `**kwargs`: 额外的配置参数。
    - **返回值**: 转换后的文档序列。
- **`atransform_documents(...)`**:
    - **功能**: 异步转换接口。
    - **逻辑**: 默认调用 `run_in_executor` 执行同步逻辑。

#### 使用示例
```python
from langchain_core.documents import BaseDocumentTransformer, Document
from typing import Sequence, Any

class SimpleTextCleaner(BaseDocumentTransformer):
    def transform_documents(self, documents: Sequence[Document], **kwargs: Any) -> Sequence[Document]:
        for doc in documents:
            # 简单的文本清洗示例
            doc.page_content = doc.page_content.strip().lower()
        return documents

cleaner = SimpleTextCleaner()
docs = [Document(page_content="  Hello World  ")]
transformed = cleaner.transform_documents(docs)
print(transformed[0].page_content) # "hello world"
```

#### 注意事项
- **有状态 vs 无状态**: 转换器可以是无状态的（如文本清洗），也可以是有状态的（如根据全局信息过滤冗余）。

## 内部调用关系
- **协作关系**: 常见的子类包括各种 `TextSplitter`。在 RAG 管道中，它通常用于数据入库前的预处理。

## 相关链接
- [LangChain 官方文档 - Document Transformers](https://python.langchain.com/docs/modules/data_connection/document_transformers/)
- [源码文件](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/core/langchain_core/documents/transformers.py)

---
最后更新时间: 2026-01-29
对应源码版本: LangChain Core v1.2.7
