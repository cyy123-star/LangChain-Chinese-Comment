# libs\langchain\langchain_classic\agents\agent_toolkits\python\__init__.py

此文档提供了 `libs\langchain\langchain_classic\agents\agent_toolkits\python\__init__.py` 文件的详细中文注释。

## 核心说明：已迁移至实验性模块

该模块中原本包含的 `create_python_agent` 函数已经迁移到了 `langchain_experimental` 包中。

### `create_python_agent`

创建一个专门用于执行 Python 代码并根据结果回答问题的代理。

#### 函数原型

```python
def create_python_agent(
    llm: BaseLanguageModel,
    tool: PythonREPLTool,
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
    **kwargs: Any,
) -> AgentExecutor:
```

#### 工作原理

1. **Python REPL**: 代理持有一个 `PythonREPLTool`，它封装了一个 Python 解释器环境。
2. **代码生成**: LLM 根据用户指令生成一段 Python 脚本。
3. **闭环执行**: `AgentExecutor` 运行该脚本，获取标准输出或错误，并将其作为 `Observation` 反馈给 LLM 进行后续推理。

### 迁移原因：安全性 (Security)
Python 代理能够直接生成并执行 Python 代码。这是一种极其强大的能力，但也伴随着巨大的安全风险（如代码注入、系统访问等）。因此，LangChain 将其归类为实验性且需谨慎使用的工具。

## 迁移指南

如果您需要继续使用 Python 代理，请执行以下操作：

1. **安装依赖**:
   ```bash
   pip install langchain-experimental
   ```

2. **更新导入语句**:
   将原来的：
   ```python
   from langchain_classic.agents.agent_toolkits.python import create_python_agent
   ```
   修改为：
   ```python
   from langchain_experimental.agents.agent_toolkits import create_python_agent
   ```

## 安全建议

**警告**: 请务必在受控环境中使用此工具。
- **隔离运行**: 必须在受限制的沙箱环境（如 gVisor, Firecracker 或 Docker）中执行代码。
- **最小权限**: 运行代码的进程不应具备网络访问权限或敏感文件系统的读写权限。
- **监控**: 对执行的代码进行实时监控和审计。
