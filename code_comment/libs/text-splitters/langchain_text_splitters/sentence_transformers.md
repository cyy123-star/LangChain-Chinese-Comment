# langchain_text_splitters.sentence_transformers

`sentence_transformers.py` 提供了基于 Hugging Face `sentence-transformers` 模型的分词切分功能。它能够确保切分后的块完全符合特定 Embedding 模型的输入 Token 限制。

## **文件概述**
该文件实现了 `SentenceTransformersTokenTextSplitter` 类。与基于 `tiktoken` 的切分器类似，它在 Token 级别进行操作，但专门针对开源的句子嵌入模型（Sentence Embedding Models）进行了优化。

## **导入依赖**
- `sentence_transformers`: 用于加载 Embedding 模型及其分词器（必需依赖）。
- `langchain_text_splitters.base.TextSplitter`: 基础切分器接口。
- `langchain_text_splitters.base.split_text_on_tokens`: 通用 Token 切分工具函数。

## **类与函数详解**

### **SentenceTransformersTokenTextSplitter (类)**
**功能描述**：使用指定 Sentence Transformer 模型的分词器来切分文本，确保每个块的 Token 数量不超过模型的最大序列长度（max_seq_length）。

#### **构造函数 `__init__`**
| 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `chunk_overlap` | `int` | `50` | 否 | 块之间的重叠 Token 数。 |
| `model_name` | `str` | `"all-mpnet-base-v2"` | 否 | 使用的 Sentence Transformer 模型名称。 |
| `tokens_per_chunk` | `int` | `None` | 否 | 每个块的目标 Token 数。若为 None，则自动使用模型的最大序列长度。 |

#### **核心方法**
- **`split_text(text: str) -> list[str]`**:
    - **逻辑**: 使用模型的 `tokenizer.encode` 获取 Token IDs，去掉特殊的起始和结束 Token（如 CLS, SEP），然后按照 `tokens_per_chunk` 进行滑动窗口切分，最后再 `decode` 回字符串。

## **核心逻辑解析**
1. **模型对齐**：在构建 RAG 系统时，如果后续使用 `sentence-transformers` 进行向量化，那么在切分阶段就使用该模型的 Tokenizer 是最安全的做法，这可以避免因 Token 计算方式不一致导致的截断问题。
2. **自动容量检测**：切分器会自动从模型配置中读取 `max_seq_length`。如果用户设置的 `tokens_per_chunk` 超过了模型上限，它会抛出错误，从而保证生成的每一块都能被完整编码。

## **使用示例**
```python
from langchain_text_splitters import SentenceTransformersTokenTextSplitter

text = "LangChain is a framework for developing applications powered by large language models (LLMs)."

# 初始化切分器，默认使用 all-mpnet-base-v2 模型
splitter = SentenceTransformersTokenTextSplitter(chunk_overlap=0)

# 执行切分
chunks = splitter.split_text(text)

for chunk in chunks:
    print(f"Chunk: {chunk}")
```

## **注意事项**
- 必须安装 `sentence-transformers` 包。
- 首次运行时，会自动从 Hugging Face 下载模型文件（通常为几百 MB），请确保网络通畅。
- 这种切分方式比字符切分慢，因为它涉及到调用深度学习模型的分词组件，但它能提供最精确的 Token 控制。

## **相关链接**
- [Sentence Transformers 官方文档](https://www.sbert.net/)
- [Token 切分工具函数](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/text-splitters/langchain_text_splitters/base.md#4-split_text_on_tokens-函数)
