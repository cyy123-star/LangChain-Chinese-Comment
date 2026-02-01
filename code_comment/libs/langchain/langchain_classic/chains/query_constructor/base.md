# libs\langchain\langchain_classic\chains\query_constructor\base.py

`query_constructor` 模块用于将用户的自然语言查询转换为结构化查询（Structured Query）。它是“自查询检索器”（Self-Querying Retriever）的核心，允许模型根据文档的元数据进行过滤和搜索。

## 功能描述

该模块定义了一套内部表示语言（AST），能够描述包含查询文本（Query）、过滤器（Filter）和限制（Limit）的复杂请求。其核心流程如下：
1.  **Prompt 构建**：利用 `FewShotPromptTemplate` 生成包含数据源说明、属性描述（Schema）和示例的提示词。
2.  **结构化输出**：LLM 根据 Prompt 生成 JSON 格式的请求。
3.  **AST 解析**：`StructuredQueryOutputParser` 将 JSON 转换为内部的 `StructuredQuery` 对象。
4.  **翻译与执行**：最终由特定的 `Translator`（如 Pinecone, MongoDB, Elasticsearch 等）将 `StructuredQuery` 翻译为数据库原生查询语句。

## 核心组件

### 1. `AttributeInfo`
用于描述数据源中某个属性（字段）的元数据。
- `name`: 属性名称。
- `description`: 属性含义的自然语言描述（对 LLM 非常重要）。
- `type`: 属性的数据类型（如 `string`, `integer`, `float`）。

### 2. `StructuredQuery`
查询的内部 AST 表示，包含：
- `query`: 搜索字符串。
- `filter`: 过滤器表达式（包含 `Comparison` 和 `Operation`）。
- `limit`: (可选) 结果数量限制。

## 核心方法：load_query_constructor_chain

### 参数说明

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `llm` | `BaseLanguageModel` | 用于生成结构化查询的模型。 |
| `document_contents` | `str` | 对数据源内容的简要描述（如“电影评论数据集”）。 |
| `attribute_info` | `Sequence[AttributeInfo]` | 数据源中可用于过滤的属性列表。 |
| `allowed_comparators` | `Sequence[Comparator]` | 允许模型使用的比较操作符（如 `eq`, `lt`, `gt`）。 |
| `allowed_operators` | `Sequence[Operator]` | 允许模型使用的逻辑操作符（如 `and`, `or`）。 |
| `enable_limit` | `bool` | 是否允许模型生成 `limit` 参数。 |

## 弃用说明与迁移

`load_query_constructor_chain` 已被标记为弃用。建议使用 LCEL 版本的 `load_query_constructor_runnable`。

### 迁移示例 (LCEL)

```python
from langchain.chains.query_constructor.base import load_query_constructor_runnable
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(temperature=0)
attribute_info = [
    AttributeInfo(name="genre", description="The genre of the movie", type="string"),
    AttributeInfo(name="year", description="The year the movie was released", type="integer"),
]
document_content_description = "Brief summary of a movie"

# 加载 Runnable 版本的查询构造器
chain = load_query_constructor_runnable(
    llm, 
    document_content_description, 
    attribute_info
)

# 执行
res = chain.invoke({"query": "I want to see sci-fi movies released after 2010"})
# 输出将是一个 StructuredQuery 对象
```

## 注意事项

1.  **属性描述的质量**：`AttributeInfo` 中的 `description` 是模型判断何时应用过滤器的唯一依据。描述应清晰且包含可能的取值范围。
2.  **幻觉防范**：通过设置 `allowed_comparators` 和 `allowed_operators`，可以限制模型生成的查询不超出数据库的能力范围。
3.  **JSON 解析**：该链高度依赖 LLM 生成有效的 JSON。对于小型模型，可能需要更强的 Few-Shot 示例或使用支持工具调用的模型。
