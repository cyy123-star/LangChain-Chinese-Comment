# Bash Chain

`LLMBashChain` 是一个允许 LLM 通过生成并执行 Bash 脚本来回答问题的链。它通常用于需要系统级操作、文件处理或运行特定命令行工具的场景。

> **警告**：此组件具有高度风险，因为它允许执行任意 Shell 命令。已迁移到 `langchain-experimental`。

## 功能描述

该模块定义了 `LLMBashChain`，其核心逻辑是：
1. **脚本生成**：LLM 根据用户问题生成一段 Bash 脚本。
2. **本地执行**：在本地 Shell 环境中执行生成的脚本。
3. **结果解析**：捕获脚本的输出（stdout/stderr）并返回给用户或进一步处理。

## 迁移指南

为了安全性和维护性，该组件已被移动到 `langchain-experimental`。

### 1. 安装依赖
```bash
pip install langchain-experimental
```

### 2. 代码迁移
```python
# 旧写法 (已弃用)
# from langchain.chains import LLMBashChain

# 新写法
from langchain_experimental.llm_bash.base import LLMBashChain
```

## 执行逻辑 (Verbatim Snippet)

该模块在 `langchain_classic` 中仅保留了重定向和弃用警告逻辑：

```python
def __getattr__(_: str = "") -> None:
    """Raise an error on import since is deprecated."""
    msg = (
        "This module has been moved to langchain-experimental. "
        "For more details: https://github.com/langchain-ai/langchain/discussions/11352."
        "To access this code, install it with `pip install langchain-experimental`."
        "`from langchain_experimental.llm_bash.base "
        "import LLMBashChain`"
    )
    raise AttributeError(msg)
```

## 安全性建议

强烈建议不要在生产环境中使用 `LLMBashChain`，除非它运行在完全隔离的容器（如 Docker）中。现代替代方案是使用 **LangGraph** 配合受限的工具调用，或者使用专门的代码解释器环境。

