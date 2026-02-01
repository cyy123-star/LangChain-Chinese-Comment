# libs\langchain\langchain_classic\agents\agent_toolkits\sql\toolkit.py

此文档提供了 `libs\langchain\langchain_classic\agents\agent_toolkits\sql\toolkit.py` 文件的详细中文注释。该模块定义了用于 SQL 数据库交互的工具包。

## 核心功能：动态重定向

该文件通过 `create_importer` 机制，将对 `SQLDatabaseToolkit` 的引用重定向到 `langchain_community`。

### 导出组件
- **`SQLDatabaseToolkit`**: 包含与 SQL 数据库交互所需的所有标准工具。

## 组件描述

### `SQLDatabaseToolkit`
这是一个功能强大的工具包，它为代理提供了一组用于操作 SQL 数据库的工具。

#### 初始化

```python
def __init__(
    self,
    db: SQLDatabase,
    llm: BaseLanguageModel,
    callback_manager: Optional[BaseCallbackManager] = None,
):
```

#### 包含工具

该工具包通常包含以下工具：
1. **sql_db_query**: 执行查询语句并获取结果。
2. **sql_db_schema**: 获取表结构（Schema）信息。
3. **sql_db_list_tables**: 列出数据库中的所有表。
4. **sql_db_query_checker**: 在执行前检查 SQL 语句的语法正确性，防止常见错误。

## 迁移建议

建议开发者直接从社区包中导入该工具包：
```python
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
```
注意：使用此工具包需要安装 `langchain-community` 和对应的数据库驱动程序（如 `sqlalchemy`）。
