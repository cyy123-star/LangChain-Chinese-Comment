# libs\langchain\langchain_classic\chains\combine_documents\stuff.py

此文档提供了 `libs\langchain\langchain_classic\chains\combine_documents\stuff.py` 文件的详细中文注释，该文件实现了最简单的文档合并策略：填充（Stuffing）。

## 文件概述

“填充”（Stuffing）是合并文档最直观的方法。它将所有检索到的文档块（Documents）简单地连接在一起，然后一次性放入提示词（Prompt）的特定变量中传递给 LLM。

**核心优势**：
- **简单高效**：只需一次 LLM 调用。
- **上下文完整**：模型可以同时看到所有相关信息，有助于理解跨文档的关联。

**核心局限**：
- **长度限制**：受限于 LLM 的最大上下文窗口。如果文档总长度超过限制，调用将失败。

---

## 核心函数：`create_stuff_documents_chain`

这是推荐的 LCEL 构造函数，用于创建填充式文档链。

### 1. 参数说明

| 参数 | 类型 | 描述 |
| :--- | :--- | :--- |
| `llm` | `LanguageModelLike` | 目标语言模型。 |
| `prompt` | `BasePromptTemplate` | 包含文档占位符（默认 `{context}`）的提示词模板。 |
| `document_prompt` | `BasePromptTemplate` | 如何格式化单个文档（例如只取 `page_content` 或包含元数据）。 |
| `document_separator` | `str` | 文档之间的分隔符，默认为 `\n\n`。 |
| `document_variable_name`| `str` | 提示词中存放合并后文本的变量名，默认为 `"context"`。 |

### 2. 返回值

返回一个 `Runnable` 对象。该对象接收包含文档列表的字典，并输出模型生成的响应。

---

## 核心类：`StuffDocumentsChain` (遗留)

这是经典的类实现方式，目前已弃用。

### 1. 核心逻辑

1. **`_get_inputs`**: 遍历文档列表，使用 `document_prompt` 格式化每个文档，并用 `document_separator` 连接。
2. **`combine_docs`**: 将连接后的长文本填入 `llm_chain` 的输入字典中，并调用 `llm_chain.predict`。

### 2. 自动变量推断

如果未显式提供 `document_variable_name`，该类会检查 `llm_chain.prompt`。如果提示词中只有一个变量，它会自动将该变量视为文档存放位置。

---

## 使用示例 (推荐方式)

```python
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

# 1. 定义包含 {context} 的提示词
prompt = ChatPromptTemplate.from_template("根据以下背景回答问题：\n\n{context}\n\n问题：{input}")

# 2. 初始化模型
llm = ChatOpenAI()

# 3. 创建填充链
chain = create_stuff_documents_chain(llm, prompt)

# 4. 准备文档和输入
docs = [
    Document(page_content="LangChain 是一个开发 LLM 应用的框架。"),
    Document(page_content="它支持 Python 和 JavaScript。")
]

# 5. 执行
result = chain.invoke({"input": "LangChain 支持什么语言？", "context": docs})
```

---

## 注意事项

1. **弃用警告**：`StuffDocumentsChain` 类已弃用，请迁移到 `create_stuff_documents_chain`。
2. **Token 管理**：对于长文档或大量文档，填充策略极易导致 `context_length_exceeded` 错误。在调用前，建议使用 `prompt_length` 方法或在外部计算总 Token 数。
3. **性能开销**：虽然只有一次 LLM 调用，但如果输入内容非常庞大，推理延迟和成本也会相应增加。
