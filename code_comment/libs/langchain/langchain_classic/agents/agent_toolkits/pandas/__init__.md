# libs\langchain\langchain_classic\agents\agent_toolkits\pandas\__init__.py

此文档提供了 `libs\langchain\langchain_classic\agents\agent_toolkits\pandas\__init__.py` 文件的详细中文注释。

## 核心说明：已迁移至实验性模块

该模块中原本包含的 `create_pandas_dataframe_agent` 函数已经迁移到了 `langchain_experimental` 包中。

### `create_pandas_dataframe_agent`

创建一个专门用于处理 Pandas DataFrame 的代理。

#### 函数原型

```python
def create_pandas_dataframe_agent(
    llm: BaseLanguageModel,
    df: Any,  # pd.DataFrame or List[pd.DataFrame]
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
    allow_dangerous_code: bool = False,  # 关键安全参数
    **kwargs: Any,
) -> AgentExecutor:
```

#### 工作原理

1. **Python REPL**: 代理内部持有一个 Python 交互式环境（REPL）。
2. **代码生成**: LLM 根据用户的自然语言请求，生成相应的 Pandas 操作代码（例如 `df.iloc[0]`）。
3. **执行与观察**: 代理在 REPL 中执行代码，捕获输出（Observation），并根据结果决定是否结束任务或进行下一步。

### 迁移原因：安全性 (Security)
Pandas 代理在底层依赖于 **Python REPL** 工具来执行生成的 Pandas 代码（如 `df.groupby(...).mean()`）。由于执行任意生成的 Python 代码存在严重的安全风险，该工具已被移至实验性模块。

## 迁移指南

如果您需要继续使用 Pandas 数据帧代理，请执行以下操作：

1. **安装依赖**:
   ```bash
   pip install langchain-experimental
   ```

2. **更新导入语句**:
   将原来的：
   ```python
   from langchain_classic.agents.agent_toolkits.pandas import create_pandas_dataframe_agent
   ```
   修改为：
   ```python
   from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
   ```

## 安全建议

在使用此代理时，强烈建议：
- **沙箱化**: 在隔离的沙箱环境（如 Docker 容器）中运行 Python REPL。
- **权限限制**: 确保运行代码的用户权限受到严格限制。
- **参考资料**: 了解更多关于安全的信息，请阅读 [LangChain GitHub Security](https://github.com/langchain-ai/langchain/blob/master/SECURITY.md)。
