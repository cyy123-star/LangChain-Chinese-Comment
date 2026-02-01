# libs\langchain\langchain_classic\agents\agent_toolkits\sql\base.py

此文档提供了 `libs\langchain\langchain_classic\agents\agent_toolkits\sql\base.py` 文件的详细中文注释。该模块定义了用于创建 SQL 数据库代理的工厂函数。

## 核心功能：动态重定向

为了保持向后兼容性并支持 LangChain 的模块化拆分，该文件目前主要作为一个动态导入层，将请求重定向到 `langchain_community` 包。

### 导出组件
- **`create_sql_agent`**: 用于构建 SQL 代理的主函数。

## 组件描述

### `create_sql_agent`
该函数允许开发者创建一个能够与 SQL 数据库进行自然语言交互的代理。

#### 函数原型

```python
def create_sql_agent(
    llm: BaseLanguageModel,
    toolkit: SQLDatabaseToolkit,
    callback_manager: Optional[BaseCallbackManager] = None,
    prefix: str = SQL_PREFIX,
    suffix: Optional[str] = None,
    format_instructions: str = SQL_FORMAT_INSTRUCTIONS,
    input_variables: Optional[List[str]] = None,
    top_k: int = 10,
    max_iterations: Optional[int] = 15,
    max_execution_time: Optional[float] = None,
    early_stopping_method: str = "force",
    verbose: bool = False,
    agent_executor_kwargs: Optional[Dict[str, Any]] = None,
    extra_tools: Sequence[BaseTool] = (),
    **kwargs: Any,
) -> AgentExecutor:
```

- **工作流**: 代理会根据用户问题，先查询数据库表结构，编写 SQL 语句，执行查询，最后根据查询结果生成回答。
- **安全性**: 内部通常会集成查询检查逻辑，防止执行危险的 SQL 语句。

## 迁移建议

虽然 `langchain_classic` 仍然提供此导出，但建议开发者直接从社区包中导入：
```python
from langchain_community.agent_toolkits.sql.base import create_sql_agent
```
或者使用现代的 **LangGraph** 实现来获得更好的控制流和错误处理能力。
