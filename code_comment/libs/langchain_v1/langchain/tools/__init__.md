# Tools (工具系统)

`tools` 模块是 LangChain v1 中定义和管理可被模型调用的外部功能的入口。它集成了 `langchain_core` 的基础工具定义，并提供了与 **LangGraph** 深度集成的扩展。

## 核心组件

### 1. 基础工具定义
- **[BaseTool](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/langchain_v1/langchain/tools/__init__.py#L4)**: 所有工具的基类，定义了工具的名称、描述、输入模式以及执行逻辑。
- **[@tool](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/langchain_v1/langchain/tools/__init__.py#L8)**: 装饰器，可将普通的 Python 函数快速转换为 `BaseTool` 实例。它利用函数的类型注解和 Docstring 自动生成模型的工具规范。

### 2. LangGraph 深度集成
- **[ToolNode](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain_v1/langchain/tools/tool_node.md)**: 一个预构建的图节点，负责自动执行 `AIMessage` 中的工具调用请求。
- **InjectedState / InjectedStore**: 允许工具在执行时自动注入当前图的状态或跨运行的持久化存储，无需模型显式传递这些参数。
- **ToolRuntime**: 提供工具执行时的上下文环境和运行时控制。

## 代码参考
- [__init__.py](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/langchain_v1/langchain/tools/__init__.py): 核心组件导出。

## 快速开始

### 定义简单工具
```python
from langchain.tools import tool

@tool
def multiply(a: int, b: int) -> int:
    """计算两个整数的乘积。"""
    return a * b

# multiply.name == "multiply"
# multiply.description == "计算两个整数的乘积。"
```

### 结合 LangGraph 状态注入
```python
from typing import Annotated
from langchain.tools import tool, InjectedState

@tool
def record_action(action: str, state: Annotated[dict, InjectedState]):
    """记录当前步骤。state 参数将由 ToolNode 自动注入。"""
    print(f"当前图状态: {state}")
    return f"已记录动作: {action}"
```

详情请参考 **[ToolNode 文档](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain_v1/langchain/tools/tool_node.md)**。
