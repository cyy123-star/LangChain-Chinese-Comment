# libs\langchain\langchain_classic\agents\agent_toolkits\xorbits\__init__.py

此文档提供了 `libs\langchain\langchain_classic\agents\agent_toolkits\xorbits\__init__.py` 文件的详细中文注释。该模块原本用于支持 Xorbits（高性能、可扩展的 Pandas 代替品）的代理交互。

## 核心说明：已迁移至实验性模块

该模块中原本包含的 `create_xorbits_agent` 函数已经迁移到了 `langchain_experimental` 包中。

### 迁移原因：安全性 (Security)

Xorbits 代理与 Pandas/Spark 代理类似，依赖于 **Python REPL** 工具来执行针对 Xorbits 数据集的分析代码。这涉及到直接执行模型生成的 Python 代码，存在显著的安全风险。
- **风险**: 恶意生成的代码可能导致数据泄露、系统破坏或远程代码执行。
- **现状**: LangChain 官方已将其迁移至实验性模块，以明确其非核心地位和潜在风险。

## 主要函数

### `create_xorbits_agent`

创建一个专门用于处理 Xorbits 对象（如 DataFrame）的代理。

#### 关键参数 (参考实验性模块)

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `llm` | `BaseLanguageModel` | 用于生成 Python 代码的大语言模型。 |
| `data` | `Any` | Xorbits 的数据对象（通常是 DataFrame）。 |
| `agent_type` | `AgentType` | 代理类型，默认为 `ZERO_SHOT_REACT_DESCRIPTION`。 |
| `allow_dangerous_code` | `bool` | **关键参数**：必须显式设置为 `True` 才能运行，表示用户已知晓风险。 |

## 迁移指南

如果您需要继续使用 Xorbits 代理，请执行以下操作：

1. **安装依赖**:
   ```bash
   pip install langchain-experimental xorbits
   ```

2. **更新导入语句**:
   ```python
   # 旧写法 (不推荐)
   from langchain_classic.agents.agent_toolkits.xorbits import create_xorbits_agent

   # 新写法 (推荐)
   from langchain_experimental.agents.agent_toolkits import create_xorbits_agent
   ```

## 安全建议

⚠️ **警告**: 请务必在受控环境中使用此工具。

- **沙箱化**: 必须在受限制的沙箱环境（如 Docker 容器、gVisor 或专门的代码执行服务）中运行，以防止对宿主系统的未经授权访问。
- **最小权限**: 运行代理的进程应仅具有访问必要数据的最低权限。
- **参考资料**: 
  - [LangChain 安全指南](https://github.com/langchain-ai/langchain/blob/master/SECURITY.md)
  - [SECURITY.md](file:///d:/TraeProjects/langchain_code_comment/SECURITY.md) (本地副本)

