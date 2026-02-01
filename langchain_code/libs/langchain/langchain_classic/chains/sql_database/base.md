# SQL Database Chain

SQL Database 链用于将自然语言问题转换为 SQL 查询，在数据库上执行该查询，并将结果转换回自然语言回答。

## 核心功能

通过 `create_sql_query_chain` 函数可以创建一个专门用于生成 SQL 的链。

| 参数 | 类型 | 说明 |
| :--- | :--- | :--- |
| `llm` | `BaseLanguageModel` | 用于生成 SQL 的语言模型。 |
| `db` | `SQLDatabase` | 目标数据库连接对象，提供 Schema 信息和查询能力。 |
| `prompt` | `Optional[BasePromptTemplate]` | 自定义提示词模板。如果不提供，将根据数据库方言自动选择。 |
| `k` | `int` | 默认限制查询结果的最大行数（Top K）。 |

## 执行逻辑

1. **上下文准备**: 链会自动从 `db` 中提取表结构（Schema）和示例行数据。
2. **SQL 生成**: LLM 根据用户问题和表结构生成符合特定方言（如 SQLite, MySQL, PostgreSQL）的 SQL 语句。
3. **安全过滤**: 可以通过 `table_names_to_use` 限制 LLM 只能访问特定的表。

```python
# 使用示例
db = SQLDatabase.from_uri("sqlite:///Chinook.db")
chain = create_sql_query_chain(llm, db)
sql_query = chain.invoke({"question": "有多少个员工？"})
# 输出: "SELECT COUNT(*) FROM Employee;"
```

## 安全提示

**重要**: 该链会生成并可能执行 SQL 语句。
- **权限最小化**: 数据库连接账号应仅具有只读权限。
- **范围限制**: 仅暴露必要的表给 LLM。
- **注入防范**: 始终对用户输入进行监控，并考虑在执行前人工审核生成的 SQL。

## 迁移建议

现代做法推荐使用 **SQL Agent**，因为它具有更好的容错能力（例如当 SQL 报错时能自动修复）：

```python
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.utilities import SQLDatabase

agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)
```
