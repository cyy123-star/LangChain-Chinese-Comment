# Symbolic Math Chain

`LLMSymbolicMathChain` 是一个专门用于处理符号数学计算（如代数方程求解、微积分等）的链。它利用 LLM 生成 Python 代码，并使用 `sympy` 库进行符号运算。

> **注意**：此模块已从主包迁移到 `langchain-experimental`。

## 功能描述

该模块定义了 `LLMSymbolicMathChain`，其核心逻辑是：
1. **代码生成**：使用 LLM 将自然语言描述的符号数学问题转化为 `sympy` 代码。
2. **符号计算**：在本地环境中执行 `sympy` 代码，进行精确的符号推导和计算。
3. **结果返回**：返回 `sympy` 计算出的符号结果。

## 迁移指南

由于该组件涉及复杂的符号计算逻辑，已被移动到 `langchain-experimental` 库中以进行更好的维护。

### 1. 安装依赖
```bash
pip install langchain-experimental sympy
```

### 2. 代码迁移
```python
# 旧写法 (已弃用)
# from langchain.chains import LLMSymbolicMathChain

# 新写法
from langchain_experimental.llm_symbolic_math.base import LLMSymbolicMathChain
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
        "`from langchain_experimental.llm_symbolic_math.base "
        "import LLMSymbolicMathChain`"
    )
    raise AttributeError(msg)
```

