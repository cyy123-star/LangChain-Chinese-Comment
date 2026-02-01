# langchain_core.documents

## 模块概述
`langchain_core.documents` 模块提供了处理数据检索和处理工作流的核心抽象。它是构建 RAG（检索增强生成）管道、向量数据库交互以及文档预处理任务的基石。

## 核心区别：Documents vs. Message Content
该模块与 `langchain_core.messages.content` 有着本质的区别，开发者需注意不要混淆：

- **Documents (本模块)**: 
    - **用途**: 用于 **数据检索和处理工作流**。
    - **场景**: 向量存储（Vector Stores）、检索器（Retrievers）、文本拆分、语义搜索。
    - **示例**: 将 PDF 拆分成多个文本块并存储在向量库中。

- **Content Blocks (`messages.content`)**:
    - **用途**: 用于 **LLM 对话 I/O**。
    - **场景**: 发送给模型的多模态内容（图像、音频）、工具调用、引用。
    - **示例**: 在聊天过程中向 Vision 模型发送一张图片。

## 核心组件导出
本模块采用了动态导入机制，主要导出以下核心类：

### 1. 核心数据模型 (from `base.py`)
- **`Document`**: 最常用的文本数据承载类，包含 `page_content` 和 `metadata`。
- **`Blob`**: 原始数据的二进制/文本封装，常用于加载阶段。

### 2. 处理接口 (from `compressor.py` & `transformers.py`)
- **`BaseDocumentCompressor`**: 检索后的文档压缩与精简接口。
- **`BaseDocumentTransformer`**: 通用的文档转换接口（如拆分、过滤）。

## 架构角色
在典型的 LangChain 应用中，数据流转通常遵循：
1. **加载**: `DocumentLoader` 生成 `Blob` 或 `Document`。
2. **转换**: `BaseDocumentTransformer`（如 `RecursiveCharacterTextSplitter`）对文档进行拆分。
3. **存储**: 文档被存入 `VectorStore`。
4. **检索**: `Retriever` 返回相关 `Document`。
5. **后处理**: `BaseDocumentCompressor` 对检索结果进行精简或重排。

## 相关链接
- [LangChain 官方文档 - Data Connection](https://python.langchain.com/docs/modules/data_connection/)
- [源码目录](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/core/langchain_core/documents/)

---
最后更新时间: 2026-01-29
对应源码版本: LangChain Core v1.2.7
