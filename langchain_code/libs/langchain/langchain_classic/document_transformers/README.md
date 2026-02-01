# Document Transformers (文档转换器)

`document_transformers` 模块负责对加载后的 `Document` 对象进行各种转换处理，如文本提取、翻译、去重、重排序等。

## 核心职责

1. **内容清洗**: 去除 HTML 标签（`BeautifulSoupTransformer`）。
2. **文本增强**: 利用 LLM 提取摘要、翻译文本（`Doctran` 系列）。
3. **检索优化**:
   - `EmbeddingsRedundantFilter`: 过滤语义重复的文档。
   - `LongContextReorder`: 针对长上下文窗口优化文档排序（处理 Lost in the Middle 问题）。

## 常用转换器

| 转换器 | 说明 |
| :--- | :--- |
| `BeautifulSoupTransformer` | 使用 BeautifulSoup 解析并提取网页特定部分。 |
| `Html2TextTransformer` | 将 HTML 转换为 Markdown 格式的纯文本。 |
| `EmbeddingsRedundantFilter` | 使用向量相似度识别并移除内容相近的文档块。 |
| `GoogleTranslateTransformer` | 调用 Google Translate API 进行多语言翻译。 |
| `OpenAIFunctionsTransformer` | 使用 OpenAI 函数调用功能从文档中提取结构化信息。 |

## 使用示例

```python
from langchain_community.document_transformers import Html2TextTransformer

# 假设已经加载了一些 HTML 文档
# docs = loader.load()

transformer = Html2TextTransformer()
transformed_docs = transformer.transform_documents(docs)

# 现在文档内容已经转换为干净的文本
print(transformed_docs[0].page_content)
```

## 注意事项

- **切分器位置**: 传统的 `TextSplitter` 现在已迁移到独立的 `langchain-text-splitters` 包中。
- **性能开销**: 涉及 LLM 的转换器（如翻译、摘要）会产生额外的费用和延迟。
- **顺序**: 在 RAG 管道中，通常先进行加载，再进行切分，最后进行转换（如去重或重排序）。
