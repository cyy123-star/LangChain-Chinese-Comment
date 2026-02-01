# libs\langchain\langchain_classic\agents\utils.py

此文档提供了 `libs\langchain\langchain_classic\agents\utils.py` 文件的详细中文注释。该模块包含代理模块中使用的实用工具函数。

## 功能描述

该模块目前主要负责对代理所使用的工具进行兼容性检查。

## 核心函数：`validate_tools_single_input`

该函数用于验证提供给代理的工具列表是否符合“单输入”限制。

### 1. 背景说明

许多经典的代理（如 `ZeroShotAgent`）设计时仅能处理简单的字符串输入。如果将需要复杂 JSON 或多个参数的工具分配给这些代理，会导致运行失败。该函数提供了一种前置校验机制。

### 2. 函数逻辑

```python
def validate_tools_single_input(class_name: str, tools: Sequence[BaseTool]) -> None:
    for tool in tools:
        if not tool.is_single_input:
            msg = f"{class_name} does not support multi-input tool {tool.name}."
            raise ValueError(msg)
```

- **参数**:
  - `class_name`: 调用方的类名，用于生成清晰的错误消息。
  - `tools`: 待检查的工具列表。
- **行为**: 遍历所有工具，若发现任一工具的 `is_single_input` 为 `False`，则抛出 `ValueError`。

## 使用场景

通常在代理类的 `from_llm_and_tools` 或 `__init__` 方法中调用。例如，[ZeroShotAgent](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/langchain/langchain_classic/agents/mrkl/base.py) 会使用它来确保它能正确地将输入传递给工具。

