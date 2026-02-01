# langchain_text_splitters.character

`character.py` 实现了基于字符的分隔符切分逻辑，包括最常用的 `CharacterTextSplitter` 和功能更强大的 `RecursiveCharacterTextSplitter`。

## **文件概述**
该文件提供了两种主要的文本切分实现：
1. **CharacterTextSplitter**: 简单的基于单个分隔符的切分。
2. **RecursiveCharacterTextSplitter**: 递归地尝试多个分隔符（如段落、句子、单词），直到块的大小符合要求。这是 LangChain 推荐的默认切分方式。

## **导入依赖**
- `re`: 用于正则表达式处理。
- `langchain_text_splitters.base.TextSplitter`: 基础切分器接口。
- `langchain_text_splitters.base.Language`: 编程语言枚举。

## **类与函数详解**

### **1. CharacterTextSplitter (类)**
**功能描述**：根据指定的单个分隔符切分文本。

#### **构造函数 `__init__`**
| 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `separator` | `str` | `"\n\n"` | 否 | 用于切分的字符或正则表达式。 |
| `is_separator_regex` | `bool` | `False` | 否 | 标记 `separator` 是否为正则表达式。 |

#### **核心逻辑**
1. 根据 `is_separator_regex` 决定是否转义 `separator`。
2. 使用 `_split_text_with_regex` 进行初步切分。
3. 调用基类的 `_merge_splits` 合并符合 `chunk_size` 的块。

---

### **2. RecursiveCharacterTextSplitter (类)**
**功能描述**：通过一组有序的分隔符递归切分文本。它会依次尝试列表中的分隔符（默认顺序：双换行、单换行、空格、空字符串），旨在尽可能保持段落、句子和单词的完整性。

#### **构造函数 `__init__`**
| 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `separators` | `list[str]` | `["\n\n", "\n", " ", ""]` | 否 | 递归切分时尝试的分隔符列表。 |
| `keep_separator` | `bool \| Literal` | `True` | 否 | 是否在块中保留分隔符。 |

#### **核心方法**
- **`split_text(text: str) -> list[str]`**:
    - **入口方法**: 调用内部递归逻辑。
- **`from_language(language, **kwargs) -> RecursiveCharacterTextSplitter`**:
    - **功能**: 类方法。根据编程语言（如 Python, Java）自动配置特定的分隔符（如类定义、函数定义关键字）。

---

### **3. _split_text_with_regex (函数)**
**功能描述**：内部底层函数，使用正则表达式切分文本，并支持将分隔符保留在块的开始或末尾。

## **核心逻辑解析**
1. **递归降级策略**：在 `RecursiveCharacterTextSplitter` 中，如果一个块超过了 `chunk_size`，它不会盲目切断，而是会查找下一个更细粒度的分隔符（例如从“换行符”降级到“空格”）重新尝试切分。
2. **语义保持**：通过优先在自然段落或句子边界切分，这种方法比纯固定长度切分更能保留文本的语义信息，有利于提高后续 RAG（检索增强生成）系统的准确率。

## **使用示例**

### **基础递归切分**
```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

text = "这是第一段。\n\n这是第二段，内容比较长，我们希望它能被合理切分。"
splitter = RecursiveCharacterTextSplitter(
    chunk_size=20,
    chunk_overlap=5,
    separators=["\n\n", "\n", "。", "，", " "]
)
chunks = splitter.split_text(text)
for i, chunk in enumerate(chunks):
    print(f"Chunk {i}: {chunk}")
```

### **代码切分示例**
```python
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language

python_code = """
def hello_world():
    print("Hello, LangChain!")

class MyClass:
    def __init__(self):
        pass
"""
# 自动加载 Python 的分隔符（如 "class ", "def "）
python_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON, 
    chunk_size=50, 
    chunk_overlap=0
)
docs = python_splitter.create_documents([python_code])
```

## **注意事项**
- 默认情况下，`RecursiveCharacterTextSplitter` 的 `keep_separator` 为 `True`，这与 `CharacterTextSplitter` 不同。
- 使用 `from_language` 时，会自动将 `is_separator_regex` 设置为 `True`，因为代码分隔符通常包含正则表达式。

## **相关链接**
- [Text Splitter 基类文档](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/text-splitters/langchain_text_splitters/base.md)
- [编程语言支持列表](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/text-splitters/langchain_text_splitters/base.md#3-language-枚举类)
