# libs\langchain\langchain_classic\agents\agent_toolkits\csv\__init__.py

此文档提供了 `libs\langchain\langchain_classic\agents\agent_toolkits\csv\__init__.py` 文件的详细中文注释。

## 功能描述

该模块原用于提供 CSV 代理的相关功能，使用 Python REPL 工具来处理和分析 CSV 文件。

### `create_csv_agent`

创建一个专门用于处理 CSV 文件的代理。

#### 函数原型

```python
def create_csv_agent(
    llm: BaseLanguageModel,
    path: str | List[str],
    pandas_kwargs: Optional[dict] = None,
    **kwargs: Any,
) -> AgentExecutor:
```

#### 工作原理

1. **Pandas 加载**: 代理使用 Pandas 加载 CSV 文件。
2. **代码生成**: LLM 根据用户提出的数据分析问题（如“CSV 中有多少行？”）生成 Python 代码。
3. **安全执行**: 代理通过 Python REPL 执行生成的代码。**注意**: 必须在沙箱环境中运行。

## 弃用与迁移说明

**重要提示**: 该代理已迁移到 `langchain_experimental` 包中。

由于该代理在后台依赖于 Python REPL 工具来执行代码，存在潜在的安全风险。为了安全使用，请务必对 Python REPL 进行沙箱处理。

### 迁移建议

1. 安装 `langchain_experimental`:
   ```bash
   pip install langchain_experimental
   ```

2. 更新导入语句:
   将：
   `from langchain_classic.agents.agent_toolkits.csv import create_csv_agent`
   改为：
   `from langchain_experimental.agents.agent_toolkits import create_csv_agent`

## 安全警告

在使用 `create_csv_agent` 时，请务必阅读以下安全指南：
- [LangChain SECURITY.md](https://github.com/langchain-ai/langchain/blob/master/SECURITY.md)
- [关于安全执行代码的讨论](https://github.com/langchain-ai/langchain/discussions/11680)
