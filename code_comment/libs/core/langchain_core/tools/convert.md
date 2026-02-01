# convert.py

## 文件概述
`convert.py` 提供了一系列实用工具和装饰器，用于将普通的 Python 函数、协程（Coroutines）以及 LangChain 的 `Runnable` 对象转换为标准的 `BaseTool` 对象。这是开发者在 LangChain 中定义工具最便捷的入口点。

## 导入依赖
- `pydantic`: 用于创建动态模型和处理字段定义。
- `langchain_core.runnables`: 支持将 LCEL 链转换为工具。
- `langchain_core.tools.simple / .structured`: 内部根据转换目标创建 `Tool` 或 `StructuredTool` 实例。

## 类与函数详解

### 1. tool (装饰器/函数)
**功能描述**: 这是一个高度灵活的工具，既可以作为装饰器使用，也可以作为普通函数调用。它是创建 LangChain 工具的首选方式。

#### 装饰器用法
- **无参数装饰器**: `@tool` 直接作用于函数，使用函数名作为工具名，文档字符串作为描述。
- **带参数装饰器**: `@tool("custom_name", parse_docstring=True)` 允许自定义名称和配置。

#### 参数说明
| 参数名 | 类型 | 默认值 | 是否必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `name_or_callable` | `str \| Callable` | `None` | 否 | 工具名称或被包装的函数。若作为装饰器参数，则表示自定义名称。 |
| `description` | `str` | `None` | 否 | 工具的功能描述。若不提供，则使用函数的文档字符串。 |
| `return_direct` | `bool` | `False` | 否 | 是否直接返回结果。 |
| `args_schema` | `Type[BaseModel]` | `None` | 否 | 显式指定输入验证架构。 |
| `infer_schema` | `bool` | `True` | 否 | 是否自动从函数签名推导架构。 |
| `parse_docstring` | `bool` | `False` | 否 | 是否解析 Google 风格文档字符串中的参数说明。 |
| `response_format` | `str` | `"content"` | 否 | 响应格式（"content" 或 "content_and_artifact"）。 |

#### 返回值
- 返回一个 `BaseTool` 实例（通常是 `StructuredTool`），或者返回一个用于包装函数的工厂装饰器。

### 2. convert_runnable_to_tool
**功能描述**: 专门用于将 `Runnable` 对象（如一个 LCEL 链）转换为工具。这使得开发者可以将复杂的逻辑流包装成一个简单的、可供 Agent 调用的单元。

## 核心逻辑解读
1. **重载支持**: `tool` 函数通过多次 `@overload` 定义，支持多种调用模式（作为装饰器、带参数装饰器、直接转换函数等）。
2. **Runnable 包装**: 当转换 `Runnable` 时，它会检查 `runnable.input_schema`。
    - 如果输入是字符串，则创建简单的 `Tool`。
    - 如果输入是对象（字典），则创建 `StructuredTool` 并包装 `invoke` 和 `ainvoke` 方法。
3. **架构优先级**: 
    - 显式提供的 `args_schema` 优先级最高。
    - 其次是 `infer_schema` 自动推导。
    - 如果两者都没有且 `infer_schema=False`，则退化为仅接收字符串输入的简单工具。
4. **描述优先级**:
    - `description` 参数 > 函数文档字符串 > `args_schema` 的文档字符串。

## 使用示例
### 使用装饰器创建工具
```python
from langchain_core.tools import tool

@tool(parse_docstring=True)
def get_weather(city: str) -> str:
    """获取指定城市的实时天气。
    
    Args:
        city: 城市名称，如 '北京'
    """
    return f"{city} 的天气是晴天"

print(get_weather.name) # get_weather
print(get_weather.run({"city": "上海"}))
```

### 将 Runnable 转换为工具
```python
from langchain_core.runnables import RunnableLambda
from langchain_core.tools import convert_runnable_to_tool

def logic(x: dict) -> str:
    return f"Result: {x['a'] + x['b']}"

runnable = RunnableLambda(logic)
tool = convert_runnable_to_tool(
    runnable, 
    name="adder", 
    description="Adds two numbers a and b"
)

print(tool.run({"a": 1, "b": 2}))
```

## 注意事项
- **类型提示**: 为了使 `infer_schema` 正常工作，被装饰的函数必须具有完整的类型提示。
- **Runnable 名称**: 将 `Runnable` 转换为工具时，必须显式提供 `name`（或 `name_or_callable` 为字符串），因为 `Runnable` 对象通常没有 `__name__` 属性。
- **文档字符串格式**: 只有在 `parse_docstring=True` 时，才会解析 `Args:` 块。

## 内部调用关系
- **StructuredTool**: 绝大多数复杂工具的实际生成类。
- **create_model**: 在 `_get_schema_from_runnable_and_arg_types` 中动态创建 Pydantic 模型。

## 相关链接
- [LangChain 装饰器定义工具](https://python.langchain.com/docs/how_to/custom_tools/#tool-decorator)
- [LCEL 与 Runnable 介绍](https://python.langchain.com/docs/concepts/#langchain-expression-language-lcel)

---
最后更新时间: 2026-01-29
对应源码版本: LangChain Core v1.2.7
