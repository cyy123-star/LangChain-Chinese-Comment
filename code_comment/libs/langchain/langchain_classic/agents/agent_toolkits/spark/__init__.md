# libs\langchain\langchain_classic\agents\agent_toolkits\spark\__init__.py

此文档提供了 `libs\langchain\langchain_classic\agents\agent_toolkits\spark\__init__.py` 文件的详细中文注释。

## 核心说明：已迁移至实验性模块

该模块中原本包含的 `create_spark_dataframe_agent` 函数已经迁移到了 `langchain_experimental` 包中。

### `create_spark_dataframe_agent`

创建一个专门用于分析 Spark DataFrame 的代理。

#### 函数原型

```python
def create_spark_dataframe_agent(
    llm: BaseLanguageModel,
    df: Any, # Spark DataFrame
    agent_type: AgentType = AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    callback_manager: Optional[BaseCallbackManager] = None,
    prefix: Optional[str] = None,
    suffix: Optional[str] = None,
    input_variables: Optional[List[str]] = None,
    verbose: bool = False,
    return_intermediate_steps: bool = False,
    max_iterations: Optional[int] = 15,
    max_execution_time: Optional[float] = None,
    early_stopping_method: str = "force",
    agent_executor_kwargs: Optional[Dict[str, Any]] = None,
    allow_dangerous_code: bool = False, # 关键安全参数
    **kwargs: Any,
) -> AgentExecutor:
```

#### 工作原理

1. **Spark 环境**: 代理持有一个指向 Spark DataFrame 的引用。
2. **PySpark 代码生成**: LLM 根据用户提出的数据分析问题（如“各部门平均薪资是多少？”）生成 PySpark 代码。
3. **安全执行**: 代理通过 Python REPL 执行代码。**注意**: 必须设置 `allow_dangerous_code=True` 才能执行。

### 迁移原因：安全性 (Security)

Spark 代理（类似于 Pandas 代理）依赖于 Python REPL 工具来执行生成的代码。这涉及到直接在环境中执行 Python 代码，因此存在重大的安全风险。LangChain 官方建议将其放在实验性模块中，并要求用户在沙箱环境中运行。

## 迁移指南

如果您需要继续使用 Spark DataFrame 代理，请执行以下操作：

1. **安装依赖**:
   ```bash
   pip install langchain-experimental
   ```

2. **更新导入语句**:
   将原来的：
   ```python
   from langchain_classic.agents.agent_toolkits.spark import create_spark_dataframe_agent
   ```
   修改为：
   ```python
   from langchain_experimental.agents.agent_toolkits import create_spark_dataframe_agent
   ```

## 安全建议

**警告**: 请务必在受控环境中使用此工具。
- **沙箱化**: 强烈建议在隔离的沙箱环境（如容器）中运行 Python REPL。
- **参考资料**: 
  - [LangChain 安全指南](https://github.com/langchain-ai/langchain/blob/master/SECURITY.md)
  - [关于 Python REPL 安全性的讨论](https://github.com/langchain-ai/langchain/discussions/11680)

