# libs\langchain\langchain_classic\agents\agent_toolkits\spark_sql\prompt.py

此文档提供了 `libs\langchain\langchain_classic\agents\agent_toolkits\spark_sql\prompt.py` 文件的详细中文注释。该模块定义了 Spark SQL 代理使用的核心提示词模板常量。

## 核心说明：动态重定向

与 `agent_toolkits` 中的其他模块类似，此文件不再直接持有提示词内容，而是通过动态导入机制重定向至 `langchain_community`。

### 导出常量

以下常量在 `DEPRECATED_LOOKUP` 中注册，并在访问时触发弃用警告：

- **`SQL_PREFIX`**: 
    *   **用途**: Spark SQL 代理的基础系统提示词前缀。
    *   **内容**: 它定义了代理作为 Spark SQL 专家的身份，并规定了其在操作大数据平台时的基本准则（例如：仅使用提供的工具、不要执行 DML 数据操作语言、在生成 SQL 后务必检查语法、针对大数据集优化查询等）。
- **`SQL_SUFFIX`**: 
    *   **用途**: 用于标准 ReAct 风格 Spark SQL 代理的提示词后缀。
    *   **内容**: 通常包含思考路径（Thought/Action/Observation）的引导和最终回答的格式要求。

## 源码实现机制

该模块使用 `create_importer` 实现了动态属性查找：

```python
DEPRECATED_LOOKUP = {
    "SQL_PREFIX": "langchain_community.agent_toolkits.spark_sql.prompt",
    "SQL_SUFFIX": "langchain_community.agent_toolkits.spark_sql.prompt",
}

_import_attribute = create_importer(__package__, deprecated_lookups=DEPRECATED_LOOKUP)

def __getattr__(name: str) -> Any:
    return _import_attribute(name)
```

## 迁移建议

为了保持代码的现代性并避免弃用警告，请直接从社区包导入：

```python
from langchain_community.agent_toolkits.spark_sql.prompt import (
    SQL_PREFIX, 
    SQL_SUFFIX
)
```
