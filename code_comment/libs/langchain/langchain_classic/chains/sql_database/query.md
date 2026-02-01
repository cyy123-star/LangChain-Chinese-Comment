# libs\langchain\langchain_classic\chains\sql_database\query.py

## 文件概述

`query.py` 提供了 `create_sql_query_chain` 函数，它是现代 LangChain (LCEL) 风格的工厂方法，用于创建一个能够根据自然语言问题生成 SQL 查询语句的链。

## 核心方法：create_sql_query_chain

该方法利用 `Runnable` 协议构建了一个处理流程，将用户问题转换为数据库可执行的 SQL 语句。

### 参数说明

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `llm` | `BaseLanguageModel` | 用于生成 SQL 的语言模型。 |
| `db` | `SQLDatabase` | 目标数据库实例，用于获取表结构信息（Schema）。 |
| `prompt` | `BasePromptTemplate` | (可选) 自定义 Prompt。若不提供，将根据数据库方言自动选择。 |
| `k` | `int` | 生成的 SQL 中默认限制的结果行数（`top_k`）。 |
| `get_col_comments` | `bool` | (可选) 是否在表信息中包含列注释（仅支持部分方言）。 |

### 执行逻辑 (LCEL 流程)

该函数返回的链遵循以下执行顺序：

1.  **输入增强 (`RunnablePassthrough.assign`)**:
    - `input`: 将原始问题格式化，并追加 `\nSQLQuery: ` 后缀。
    - `table_info`: 调用 `db.get_table_info` 获取相关表的 Schema 和示例数据。
2.  **变量清理**: 移除中间不需要的变量（如原始 `question`）。
3.  **Prompt 填充**: 将 `top_k` 和 `dialect`（如果需要）注入 Prompt。
4.  **LLM 生成**: 调用 LLM 生成 SQL。设置 `stop=["\nSQLResult:"]` 以防止模型过度生成。
5.  **结果解析**: 使用 `StrOutputParser` 并去除多余空白字符。

### 使用示例

```python
from langchain_openai import ChatOpenAI
from langchain_classic.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase

db = SQLDatabase.from_uri("sqlite:///Chinook.db")
model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
chain = create_sql_query_chain(model, db)
response = chain.invoke({"question": "How many employees are there"})
```

## 注意事项与安全性

- **注入风险**: 生成的 SQL 语句需要由调用者谨慎执行。建议数据库用户仅具有只读权限。
- **表范围限制**: 可以通过在 `invoke` 时传入 `table_names_to_use` 来限制 LLM 可见的表范围。
- **方言支持**: 默认 Prompt 会根据 `db.dialect` 自动调整（如 `postgresql`, `mysql`, `sqlite` 等）。
