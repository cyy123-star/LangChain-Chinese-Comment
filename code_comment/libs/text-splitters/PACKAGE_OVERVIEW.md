# LangChain Text Splitters (langchain-text-splitters) 技术文档

`langchain-text-splitters` 是 LangChain 专门用于文本切分的工具包。在 LLM 应用中，由于模型上下文窗口（Context Window）的限制，长文本必须被切分为较小的块（Chunks），同时尽可能保持语义的连贯性。

---

## **1. 核心功能与主要 API**

### **核心功能**
- **智能切分**：不仅支持按长度切分，还支持根据文档结构（如 Markdown 标题、HTML 标签、代码语法）进行语义感知的切分。
- **Token 感知**：支持集成 `tiktoken`, `HuggingFace` 等分词器，确保切分后的块符合模型的 Token 限制。
- **重叠管理**：支持设置 `chunk_overlap`，在块与块之间保留冗余信息，防止语义在切分处断裂。
- **多格式支持**：内置对 Python, JS, Markdown, HTML, LaTeX, JSON 等多种格式的专项支持。

### **主要 API 概览**

| 类名 | 切分策略 | 适用场景 |
| :--- | :--- | :--- |
| `RecursiveCharacterTextSplitter` | 递归尝试一组分隔符（如 `\n\n`, `\n`, ` `） | **最通用**。尽可能保持段落、句子的完整。 |
| `CharacterTextSplitter` | 基于单一字符分隔符进行简单切分 | 简单的固定长度切分。 |
| `MarkdownHeaderTextSplitter` | 根据 Markdown 的标题层级（# ## ###）切分 | 结构化 Markdown 文档，提取元数据。 |
| `TokenTextSplitter` | 基于 Token 数量进行精确切分 | 严格控制模型输入成本。 |
| `PythonCodeTextSplitter` | 识别 Python 类、函数定义进行切分 | 代码分析、代码检索增强（RAG）。 |
| `HTMLHeaderTextSplitter` | 基于 HTML 标签（h1-h6）进行切分 | 网页抓取数据处理。 |

### **通用配置参数**
- `chunk_size`: 每个块的最大长度（字符数或 Token 数）。
- `chunk_overlap`: 相邻块之间的重叠长度，用于保持上下文。
- `length_function`: 计算长度的函数，默认为 `len`（按字符），可替换为 Token 计算函数。
- `add_start_index`: 是否在结果的元数据中包含块在原始文档中的起始位置。

### **使用示例**

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. 初始化切分器
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20,
    length_function=len,
    is_separator_regex=False,
)

# 2. 待切分文本
text = "这是一个非常长的示例文本...（此处省略数千字）"

# 3. 执行切分
# 返回字符串列表
texts = text_splitter.split_text(text)
# 返回 Document 对象列表（包含元数据）
docs = text_splitter.create_documents([text])
```

---

## **2. 整体架构分析**

### **内部模块划分**
- **`base.py`**：定义了 `TextSplitter` 抽象基类，封装了切分的核心逻辑（如处理重叠、合并块等）。
- **结构化切分模块**：`markdown.py`, `html.py`, `latex.py` 等，利用正则表达式或解析器识别特定格式的边界。
- **集成模块**：`tiktoken.py`, `nltk.py`, `spacy.py` 等，利用成熟的 NLP 库提供更高精度的切分（如按句子切分）。

### **依赖关系**
- **核心依赖**：`langchain-core`。该包继承了 `core` 中定义的 `BaseDocumentTransformer` 接口。
- **可选依赖**：`tiktoken` (OpenAI 分词), `beautifulsoup4` (HTML 解析), `lxml` (XML/HTML 处理)。

### **设计模式**
- **模版方法模式 (Template Method Pattern)**：`TextSplitter` 定义了 `split_text` 的通用骨架，子类只需通过重写特定逻辑（如分隔符列表）即可实现不同的切分策略。
- **组合模式**：某些切分器（如 `MarkdownHeaderTextSplitter`）可以将文档转换为具有层次结构的块。

### **数据流转机制**
1. **输入**：原始长字符串或 `Document` 对象列表。
2. **预处理**：识别文档类型，加载对应的分词器或分隔符。
3. **递归切分**：如果是 `RecursiveCharacterTextSplitter`，会先尝试用段落分隔符切分，如果块太大，再尝试换行符，以此类推。
4. **后处理**：将切分后的片段重新组合，确保每个块的大小在 `chunk_size` 左右，并添加 `chunk_overlap` 长度的上下文。
5. **输出**：一组包含切分后内容及元数据（如 `start_index`）的 `Document` 对象。

---

## **3. 注意事项**
- **语义丢失**：过度切分会导致语义断裂，建议始终保留一定的 `chunk_overlap`。
- **性能开销**：对于超大规模文档，使用复杂的 NLP 切分器（如 `SpacyTextSplitter`）可能会消耗较多 CPU 资源。
- **Token 计算**：模型通常按 Token 计费，因此在生产环境建议使用基于 Token 的长度计算函数。
