# libs\langchain\langchain_classic\agents\agent_toolkits\spark_sql\toolkit.py

此文档提供了 `libs\langchain\langchain_classic\agents\agent_toolkits\spark_sql\toolkit.py` 文件的详细中文注释。该模块定义了用于 Spark SQL 交互的工具包。

## 核心说明：动态重定向

该模块已弃用，其核心工具包类已通过动态导入机制重定向至 `langchain_community`。

### 导出类

以下类在 `DEPRECATED_LOOKUP` 中注册，并在访问时触发弃用警告：

- **`SparkSQLToolkit`**: 
    *   **功能**: 封装了一组用于与 Spark SQL 交互的工具。
    *   **初始化**:
        ```python
        def __init__(
            self,
            db: SparkSQL,
            llm: BaseLanguageModel,
            callback_manager: Optional[BaseCallbackManager] = None,
        ):
        ```
    *   **包含工具**:
        - `query_spark_sql`: 执行 SQL 查询并返回结果。
        - `info_spark_sql`: 获取表的结构和样本数据。
        - `list_tables_spark_sql`: 列出数据库中的所有表。
        - `checker_spark_sql`: 检查 SQL 语法的正确性。

## 源码实现机制

该模块利用 `create_importer` 实现动态属性查找：

```python
DEPRECATED_LOOKUP = {
    "SparkSQLToolkit": "langchain_community.agent_toolkits.spark_sql.toolkit",
}

_import_attribute = create_importer(__package__, deprecated_lookups=DEPRECATED_LOOKUP)

def __getattr__(name: str) -> Any:
    return _import_attribute(name)
```

## 迁移建议

为了保持代码的现代性并避免弃用警告，请直接从社区包导入：

```python
from langchain_community.agent_toolkits.spark_sql.toolkit import SparkSQLToolkit
```
