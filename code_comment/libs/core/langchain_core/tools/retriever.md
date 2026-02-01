# langchain_core.tools.retriever

## 文件概述
**langchain_core.tools.retriever** 模块提供了一个方便的函数 `create_retriever_tool`，用于将 LangChain 的 `BaseRetriever` 对象包装成一个 `BaseTool`（具体为 `StructuredTool`）。这使得 Agent 能够像使用其他工具一样使用检索器来查找相关文档。

---

## 导入依赖
| 依赖项 | 来源 | 作用 |
| :--- | :--- | :--- |
| `BaseModel`, `Field` | `pydantic` | 用于定义工具的输入参数架构。 |
| `BaseRetriever` | `langchain_core.retrievers` | 检索器的基类。 |
| `StructuredTool` | `langchain_core.tools.structured` | 可处理多参数输入的工具类。 |
| `BasePromptTemplate`, `PromptTemplate` | `langchain_core.prompts` | 用于格式化检索到的文档。 |
| `format_document`, `aformat_document` | `langchain_core.prompts` | 同步和异步格式化文档的工具函数。 |

---

## 类与函数详解

### 1. RetrieverInput (Pydantic 模型)
**功能描述**: 定义了检索器工具的输入结构。它仅包含一个 `query` 字段。
#### 属性说明
| 属性名 | 类型 | 默认值 | 详细用途 |
| :--- | :--- | :--- | :--- |
| `query` | `str` | - | 需要在检索器中查找的查询字符串。 |

### 2. create_retriever_tool
**功能描述**: 创建一个 `StructuredTool` 实例，该实例在调用时会运行检索器并将结果格式化为字符串。
#### 参数说明
| 参数名 | 类型 | 默认值 | 是否必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `retriever` | `BaseRetriever` | - | 是 | 要包装的检索器对象。 |
| `name` | `str` | - | 是 | 工具的名称。应该具有描述性且唯一。 |
| `description` | `str` | - | 是 | 工具的描述，模型根据此描述决定何时使用检索。 |
| `document_prompt` | `BasePromptTemplate` | `None` | 否 | 用于格式化单个文档的 Prompt 模板。默认使用 `{page_content}`。 |
| `document_separator` | `str` | `"\n\n"` | 否 | 多个文档之间的分隔符。 |
| `response_format` | `Literal["content", "content_and_artifact"]` | `"content"` | 否 | 响应格式。如果是 `content_and_artifact`，则返回内容和原始文档列表。 |
#### 返回值解释
- **类型**: `StructuredTool`
- **含义**: 封装后的检索器工具，可直接传递给 Agent。

---

## 核心逻辑
1. **内部函数定义**: 在 `create_retriever_tool` 内部定义了同步函数 `func` 和异步函数 `afunc`。
2. **检索与格式化**:
   - 调用检索器的 `invoke` 或 `ainvoke` 获取文档列表。
   - 使用 `format_document` 和指定的 `document_prompt` 将每个文档转换为字符串。
   - 使用 `document_separator` 将所有文档字符串连接起来。
3. **响应构造**: 根据 `response_format` 返回格式化后的字符串或 `(字符串, 文档列表)` 的元组。
4. **工具封装**: 返回一个 `StructuredTool`，将上述逻辑封装在其中，并自动设置 `args_schema` 为 `RetrieverInput`。

---

## 使用示例
```python
from langchain_core.tools.retriever import create_retriever_tool
from langchain_core.retrievers import BaseRetriever
from langchain_core.documents import Document

# 假设我们有一个简单的检索器（实际使用时通常是向量存储检索器）
class SimpleRetriever(BaseRetriever):
    def _get_relevant_documents(self, query, *, run_manager):
        return [Document(page_content=f"Result for {query}")]

retriever = SimpleRetriever()
tool = create_retriever_tool(
    retriever,
    "search_docs",
    "Searches for information about various topics in the knowledge base."
)

# 使用工具
result = tool.invoke({"query": "langchain"})
print(result) # 输出: Result for langchain
```

---

## 注意事项
- **提示词工程**: `name` 和 `description` 对 Agent 的表现至关重要。请确保它们能准确描述检索器的用途。
- **文档格式化**: 如果文档包含重要的元数据（如来源、日期），建议通过 `document_prompt` 将其包含在输出中，以便模型参考。

---

## 内部调用关系
- 该函数利用 `StructuredTool` 来处理复杂的输入和输出格式。
- 它依赖于 `langchain_core.prompts` 中的格式化工具来处理文档内容。

---

## 相关链接
- [LangChain 官方文档 - Retrievers](https://python.langchain.com/docs/modules/data_connection/retrievers/)
- [langchain_core.tools.structured](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/core/langchain_core/tools/structured.md)

---

## 元信息
- **最后更新时间**: 2026-01-29
- **对应源码版本**: LangChain Core v1.2.7
