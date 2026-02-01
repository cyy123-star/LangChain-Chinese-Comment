# langchain_core.output_parsers.openai_tools

## 文件概述
`openai_tools.py` 专门用于解析 OpenAI 风格的工具调用（Tool Calls）输出。它能够将模型返回的原始工具调用数据转换为结构化的 Python 对象、字典或 Pydantic 模型，并支持流式解析不完整的 JSON 参数。

---

## 导入依赖
| 模块 | 作用 |
| :--- | :--- |
| `json` | 用于解析工具调用的参数字符串。 |
| `pydantic` | 用于验证工具调用参数是否符合预定义的 Schema。 |
| `langchain_core.messages` | 导入 `AIMessage`, `InvalidToolCall` 等消息类型。 |
| `langchain_core.utils.json` | 导入 `parse_partial_json` 用于流式解析不完整的 JSON。 |
| `langchain_core.output_parsers.transform` | 继承 `BaseCumulativeTransformOutputParser` 以支持流式处理。 |

---

## 类与函数详解

### 1. parse_tool_call (函数)
**功能描述**: 解析单个原始工具调用。

#### 参数说明
| 参数名 | 类型 | 默认值 | 是否必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `raw_tool_call` | `dict` | - | 是 | OpenAI 返回的原始工具调用字典。 |
| `partial` | `bool` | `False` | 否 | 是否允许解析不完整的 JSON 参数。 |
| `strict` | `bool` | `False` | 否 | 是否严格遵循 JSON 规范。 |
| `return_id` | `bool` | `True` | 否 | 是否在结果中包含工具调用的 ID。 |

---

### 2. JsonOutputToolsParser
**功能描述**: 将 OpenAI 的响应解析为工具调用列表（字典形式）。

#### 属性
| 属性名 | 类型 | 默认值 | 详细用途 |
| :--- | :--- | :--- | :--- |
| `return_id` | `bool` | `False` | 是否返回工具调用的 ID。 |
| `first_tool_only` | `bool` | `False` | 是否仅返回第一个工具调用。 |

#### 核心方法
- **`parse_result`**:
    - **逻辑**: 优先从 `AIMessage.tool_calls` 中获取已解析的工具调用。如果不存在（例如缓存的旧消息），则从 `additional_kwargs` 中提取并手动解析。
    - **返回值**: 工具调用字典列表或单个字典。

---

### 3. JsonOutputKeyToolsParser
**功能描述**: 继承自 `JsonOutputToolsParser`，用于筛选并返回特定名称（key）的工具调用参数。

#### 属性
| 属性名 | 类型 | 默认值 | 详细用途 |
| :--- | :--- | :--- | :--- |
| `key_name` | `str` | - | 目标工具的名称。 |

---

### 4. PydanticToolsParser
**功能描述**: 将工具调用解析为指定的 Pydantic 模型实例。这提供了强类型的校验。

#### 属性
| 属性名 | 类型 | 默认值 | 详细用途 |
| :--- | :--- | :--- | :--- |
| `tools` | `list[type[BaseModel]]` | - | 用于验证和实例化的 Pydantic 模型列表。 |

---

## 核心逻辑
1. **部分 JSON 解析**: 通过 `parse_partial_json`，解析器可以在模型还在输出参数的过程中（即 JSON 尚未闭合时）就提取出已生成的键值对。
2. **向后兼容性**: 能够处理新版 LangChain 的 `message.tool_calls` 属性，同时也兼容旧版存储在 `additional_kwargs["tool_calls"]` 中的原始数据。
3. **错误处理**: 如果模型输出因为 `max_tokens` 被截断，解析器会记录相关的警告信息，帮助开发者定位解析失败的原因。

---

## 使用示例

### 使用 Pydantic 解析工具调用
```python
from pydantic import BaseModel, Field
from langchain_core.output_parsers.openai_tools import PydanticToolsParser

class GetWeather(BaseModel):
    location: str = Field(..., description="城市名称")

parser = PydanticToolsParser(tools=[GetWeather])

# 模拟 AI 消息
from langchain_core.messages import AIMessage
msg = AIMessage(
    content="",
    tool_calls=[{
        "name": "GetWeather",
        "args": {"location": "北京"},
        "id": "call_123"
    }]
)

result = parser.invoke(msg)
print(result) # [GetWeather(location='北京')]
```

---

## 注意事项
- **输入要求**: 此解析器仅适用于 `ChatGeneration`（聊天模型输出），不能用于普通的 `Generation`。
- **工具名称匹配**: 在 `PydanticToolsParser` 中，工具名称默认使用 Pydantic 模型的类名或 `title` 配置。如果模型返回的名称不匹配，解析将跳过该工具。
- **流式限制**: 目前 `PydanticToolsParser` 仅在 Pydantic 对象的所有字段都解析完成后才会 yield 结果，不支持对象内部字段的逐个流式输出。

---

## 内部调用关系
- 依赖于 `langchain_core.utils.json` 进行健壮的 JSON 解析。
- 深度集成在支持工具调用的 ChatModel 流程中。

---

## 元信息
- **最后更新时间**: 2026-01-29
- **对应源码版本**: LangChain Core v1.2.7
