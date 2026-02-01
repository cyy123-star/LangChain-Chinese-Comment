# structured.py

## 文件概述
`structured.py` 定义了 `StructuredTool` 类，这是 LangChain 中最常用的工具实现之一。与简单的单参数工具不同，`StructuredTool` 支持多参数输入，并能自动从 Python 函数签名和文档字符串（Docstring）中推导出复杂的输入架构（Schema）。

## 导入依赖
- `langchain_core.tools.base`: 继承自 `BaseTool` 并使用其定义的辅助工具。
- `pydantic`: 用于输入验证和字段定义。
- `langchain_core.callbacks`: 处理同步和异步执行过程中的回调管理。

## 类与函数详解

### 1. StructuredTool
**功能描述**: 能够处理任意数量输入参数的工具类。它通常通过封装现有的 Python 函数或协程来创建。

#### 核心属性
| 参数名 | 类型 | 默认值 | 是否必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `func` | `Callable` | `None` | 否 | 工具执行时调用的同步函数。 |
| `coroutine` | `Callable` | `None` | 否 | 工具执行时调用的异步协程。 |
| `args_schema` | `ArgsSchema` | - | 是 | 强制要求的输入架构，用于定义工具接受的参数及其类型。 |

#### 核心方法
- **`from_function` (类方法)**:
    - **功能**: 从给定的函数或协程快速创建 `StructuredTool` 实例。这是创建此类工具的推荐方式。
    - **参数**:
        - `func`: 同步函数。
        - `coroutine`: 异步函数。
        - `name`: 工具名称（默认使用函数名）。
        - `description`: 工具描述（默认使用函数文档字符串）。
        - `infer_schema`: 是否自动推导架构（默认为 `True`）。
        - `parse_docstring`: 是否尝试解析 Google 风格的参数描述。
    - **返回值**: `StructuredTool` 实例。
- **`_run` / `_arun`**:
    - **功能**: 内部调用的执行逻辑。它们负责将输入字典解包为位置参数和关键字参数，并传递给底层函数。

## 核心逻辑解读
1. **自动架构推导**: `from_function` 使用 `create_schema_from_function` 分析函数的类型提示（Type Hints），生成一个 Pydantic 模型作为 `args_schema`。
2. **文档字符串解析**: 如果启用了 `parse_docstring`，它会解析 Google 风格的文档字符串，提取每个参数的详细描述，并将其注入到 Pydantic 字段的 `description` 中。这对于向大语言模型解释参数含义至关重要。
3. **同步与异步兼容**: 
    - 如果只提供了同步函数 `func`，调用 `ainvoke` 时会使用 `run_in_executor` 在线程池中运行。
    - 如果提供了 `coroutine`，则直接异步执行。
4. **注入参数过滤**: 自动推导架构时，会自动过滤掉如 `callbacks`、`run_manager` 和 `config` 等由框架内部管理的参数，确保发送给模型的架构只包含业务相关的参数。

## 使用示例
### 从函数创建多参数工具
```python
from langchain_core.tools import StructuredTool

def calculate_area(width: float, height: float) -> float:
    """计算矩形的面积。
    
    Args:
        width: 矩形的宽度
        height: 矩形的高度
    """
    return width * height

# 自动推导架构和描述
area_tool = StructuredTool.from_function(
    func=calculate_area,
    name="area_calculator",
    parse_docstring=True
)

print(area_tool.run({"width": 10, "height": 5}))
# 输出: 50.0
```

## 注意事项
- **文档字符串要求**: 如果不显式提供 `description`，封装的函数必须编写文档字符串（Docstring），否则会抛出 `ValueError`。
- **参数类型提示**: 强烈建议为函数参数提供准确的类型提示，以便生成正确的验证架构。
- **异步支持**: 为了获得最佳性能，在异步环境（如 FastAPI）中建议同时提供 `func` 和 `coroutine`。

## 内部调用关系
- **基类调用**: 继承自 `base.py` 中的 `BaseTool`，共享其输入解析和回调触发逻辑。
- **工具生成器**: 它是 `langchain_core.tools.tool` 装饰器内部使用的核心类之一。

## 相关链接
- [LangChain 结构化工具概念](https://python.langchain.com/docs/how_to/custom_tools/#structuredtool)
- [Pydantic 官方文档](https://docs.pydantic.dev/)

---
最后更新时间: 2026-01-29
对应源码版本: LangChain Core v1.2.7
