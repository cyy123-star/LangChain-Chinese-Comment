# libs\langchain\langchain_classic\chains\combine_documents\base.py

此文档提供了 `libs\langchain\langchain_classic\chains\combine_documents\base.py` 文件的详细中文注释，该文件定义了合并多个文档的通用接口和基础实现。

## 文件概述

在检索增强生成（RAG）等应用中，经常需要将检索到的多个文档块（Documents）合并为一个统一的响应。该文件定义了处理这一过程的抽象基类 `BaseCombineDocumentsChain`，以及一个便捷的分析链 `AnalyzeDocumentChain`。

**核心功能**：
- 定义合并文档的标准输入/输出模式。
- 提供计算提示词长度（Token 数）的接口，以防止超出上下文限制。
- 支持同步和异步的文档合并操作。

---

## 核心类：`BaseCombineDocumentsChain` (抽象基类)

这是所有文档合并链（如 Stuff, MapReduce, Refine）的基类。

### 1. 关键属性

| 属性 | 默认值 | 描述 |
| :--- | :--- | :--- |
| `input_key` | `"input_documents"` | 链期望的包含 `Document` 列表的输入键。 |
| `output_key` | `"output_text"` | 链生成的合并文本的输出键。 |

### 2. 核心方法

- **`combine_docs(docs, **kwargs)`**: (抽象方法) 将文档列表合并为单个字符串及相关字典。
- **`acombine_docs(docs, **kwargs)`**: (异步抽象方法) `combine_docs` 的异步版本。
- **`prompt_length(docs, **kwargs)`**: 计算给定文档列表生成的提示词长度（以 Token 为单位）。这对于动态调整文档数量以适应上下文窗口非常有用。

---

## 核心类：`AnalyzeDocumentChain`

这是一个高级封装链，它将“文本拆分”和“文档合并”两个步骤结合在一起。

### 1. 工作流程

1. **输入**：接收一个长文本字符串（`input_document`）。
2. **拆分**：使用 `text_splitter`（默认为 `RecursiveCharacterTextSplitter`）将长文本拆分为多个小文档。
3. **合并**：将拆分后的文档列表传递给内部的 `combine_docs_chain`（如总结链或问答链）进行处理。

### 2. 主要用途

适用于直接对单个长文档进行总结、问答或分析，而不需要先手动拆分文档。

---

## LCEL 迁移示例

由于 `BaseCombineDocumentsChain` 及其子类已被弃用，官方建议使用 LCEL 实现。以下是替代 `AnalyzeDocumentChain` 的逻辑示例：

### 1. 简单的总结链替代

```python
# 旧版方式
# analyze_chain = AnalyzeDocumentChain(combine_docs_chain=summary_chain, text_splitter=text_splitter)

# LCEL 方式
from langchain_core.runnables import RunnableLambda

split_text = RunnableLambda(lambda x: text_splitter.create_documents([x]))
summarize_document_chain = split_text | summary_chain
```

### 2. 带额外参数（如问题）的 QA 链替代

```python
from operator import itemgetter
from langchain_core.runnables import RunnableParallel

summarize_document_chain = RunnableParallel(
    question=itemgetter("question"),
    input_documents=itemgetter("input_document") | RunnableLambda(lambda x: text_splitter.create_documents([x])),
) | qa_chain.pick("output_text")
```

---

## 注意事项

1. **弃用说明**：此类及其子类（Stuff, MapReduce 等）在 LangChain 0.2.x 中已标记为弃用，计划在 1.0 版本中移除。
2. **上下文限制**：在合并文档时，务必注意 LLM 的最大上下文窗口（Context Window）。`prompt_length` 方法是处理此问题的关键。
3. **输入一致性**：子类实现必须确保能够接收 `Document` 对象列表作为主要输入。
