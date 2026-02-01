# Function Calling 实用工具模块文档

## 文件概述
`function_calling.py` 是 LangChain 中用于将 Python 对象（如类、函数、Pydantic 模型）转换为 LLM 可理解的“函数/工具定义”的核心工具模块。它主要支持 OpenAI 风格的函数调用（Function Calling）和工具调用（Tool Calling）协议，同时也兼容 Anthropic 和 Amazon Bedrock 等平台的格式。

## 导入依赖
- `inspect`: 用于提取 Python 函数的签名和文档字符串。
- `pydantic`: 支持 V1 和 V2 版本的模型转换。
- `langchain_core.messages`: 处理与工具调用相关的消息类型（如 `ToolMessage`）。
- `langchain_core.utils.json_schema`: 处理 JSON Schema 中的引用。

## 类与类型详解

### 1. FunctionDescription (TypedDict)
**功能描述**: 表示发送给 LLM 的可调用函数的结构。
- **属性**:
    - `name`: 函数名称。
    - `description`: 函数功能描述。
    - `parameters`: 参数的 JSON Schema 字典。

### 2. ToolDescription (TypedDict)
**功能描述**: OpenAI API 风格的工具描述。
- **属性**:
    - `type`: 固定为 `"function"`。
    - `function`: `FunctionDescription` 对象。

---

## 核心函数详解

### 1. convert_to_openai_function
**功能描述**: 将多种类型的 Python 对象统一转换为 OpenAI 函数格式。
- **参数说明**:
    | 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
    | :--- | :--- | :--- | :--- | :--- |
    | `function` | `Union[dict, type, Callable, BaseTool]` | - | 是 | 可以是字典、Pydantic 类、TypedDict、LangChain 工具或普通 Python 函数。 |
    | `strict` | `bool` | `None` | 否 | 是否启用严格模式。启用后，模型输出将严格匹配定义的 JSON Schema。 |
- **返回值**: `dict[str, Any]` - 符合 OpenAI 协议的函数定义字典。

### 2. convert_to_openai_tool
**功能描述**: 将对象转换为 OpenAI 工具格式（外层包裹 `{"type": "function", ...}`）。
- **参数说明**: 同 `convert_to_openai_function`。
- **核心逻辑**: 内部调用 `convert_to_openai_function` 并添加工具包装层。它还支持识别 OpenAI 的内置工具（如 `file_search`, `code_interpreter`）。

### 3. _convert_python_function_to_openai_function
**功能描述**: 内部工具，通过解析 Python 函数的类型提示（Type Hints）和文档字符串（Docstring）自动生成函数定义。
- **核心逻辑**: 
    1. 使用 `inspect` 获取函数签名。
    2. 解析 Google 风格或标准风格的文档字符串以提取参数描述。
    3. 构建临时的 Pydantic 模型并导出为 JSON Schema。

## 核心逻辑
1. **递归处理**: 能够处理嵌套的 `TypedDict` 和 `Annotated` 类型，将其递归转换为 Pydantic 模型。
2. **Schema 清洗**: 使用 `_rm_titles` 递归移除 JSON Schema 中的 `title` 字段（OpenAI 通常不需要这些字段，移除可节省 Token）。
3. **严格模式支持**: 如果设置 `strict=True`，会自动将所有字段设为 `required` 并设置 `additionalProperties: False`。

## 使用示例
```python
from langchain_core.utils.function_calling import convert_to_openai_tool

# 1. 转换普通函数
def get_weather(location: str, unit: str = "celsius"):
    """获取指定位置的天气。
    
    Args:
        location: 城市名称。
        unit: 温度单位。
    """
    pass

tool_schema = convert_to_openai_tool(get_weather)

# 2. 转换 Pydantic 模型
from pydantic import BaseModel, Field

class SearchQuery(BaseModel):
    query: str = Field(..., description="搜索关键词")

tool_schema_2 = convert_to_openai_tool(SearchQuery)
```

## 注意事项
- **文档字符串**: 为了获得最佳转换效果，建议为 Python 函数编写清晰的文档字符串（尤其是参数说明）。
- **Pydantic 版本**: 该模块同时兼容 Pydantic V1 和 V2，会自动根据环境选择合适的处理逻辑。
- **严格模式约束**: 启用 `strict=True` 时，必须确保所有参数都有明确的定义，且不允许额外属性。

## 相关链接
- [OpenAI 函数调用官方指南](https://platform.openai.com/docs/guides/function-calling)
- [JSON Schema 规范](https://json-schema.org/)

---
**最后更新时间**: 2026-01-29
**对应源码版本**: LangChain Core v1.2.7
