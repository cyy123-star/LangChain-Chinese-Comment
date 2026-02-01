# libs\langchain\langchain_classic\agents\agent_toolkits\spark_sql\__init__.py

`spark_sql` 模块提供了用于与 Spark SQL 交互的工具包。该模块目前已作为弃用模块，其核心实现已迁移至 `langchain_community`。

## 主要内容

- **SparkSQLToolkit**: 整合了操作 Spark SQL 的工具，如查询、检查语法、列出表等。
- **create_spark_sql_agent**: 创建专门用于执行 Spark SQL 查询的代理。

## 迁移建议

该模块中的所有功能已迁移到 `langchain_community` 包中。建议开发者更新导入语句：

```python
# 弃用的导入方式
from langchain_classic.agents.agent_toolkits.spark_sql import SparkSQLToolkit, create_spark_sql_agent

# 推荐的导入方式
from langchain_community.agent_toolkits.spark_sql import SparkSQLToolkit, create_spark_sql_agent
```

## 注意事项

- **环境依赖**: 使用此工具包需要安装 `pyspark`。
- **安全警告**: 代理能够执行 SQL 查询。请确保连接的 Spark 账号权限受到严格限制，以防止未经授权的数据访问。
- **大数据处理**: 代理生成的 SQL 会直接在 Spark 集群运行。建议通过 `top_k` 等参数限制返回的数据量。

