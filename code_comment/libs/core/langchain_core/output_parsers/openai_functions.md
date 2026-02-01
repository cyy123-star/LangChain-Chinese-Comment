# langchain_core.output_parsers.openai_functions

## 文件概述
`openai_functions.py` 专门用于解析 OpenAI 风格的函数调用（Function Calling）输出。虽然 OpenAI 后来推出了更通用的 Tool Calling，但 Function Calling 模式在许多模型和旧版应用中仍然广泛使用。此模块提供了将函数调用信息解析为字典或 Pydantic 对象的工具。

---

## 导入依赖
| 模块 | 作用 |
| :--- | :--- |
| `json` | 用于解析函数调用的参数字符串。 |
| `pydantic` | 用于将解析出的参数验证并实例化为强类型的 Python 对象。 |
| `jsonpatch` | 用于流式模式下计算解析结果的增量差异。 |
| `langchain_core.output_parsers` | 导入 `BaseGenerationOutputParser` 和 `BaseCumulativeTransformOutputParser`。 |
| `langchain_core.outputs` | 导入 `ChatGeneration` 和 `Generation` 数据结构。 |

---

## 类与函数详解

### 1. OutputFunctionsParser
**功能描述**: 最基本的函数调用解析器。它直接从消息的 `additional_kwargs["function_call"]` 中提取信息。

#### 属性
| 属性名 | 类型 | 默认值 | 详细用途 |
| :--- | :--- | :--- | :--- |
| `args_only` | `bool` | `True` | 如果为 `True`，仅返回函数参数字符串；如果为 `False`，返回包含函数名和参数的完整字典。 |

---

### 2. JsonOutputFunctionsParser
**功能描述**: 累积式流式解析器，能够实时将函数调用的参数字符串解析为 JSON 对象。

#### 核心方法
- **`_diff`**: 使用 `jsonpatch` 计算流式输出之间的差异。
- **`parse_result`**:
    - **功能**: 支持部分解析（`partial=True`）。当模型还在生成参数时，它会尝试解析已有的片段。
    - **逻辑**: 如果 `args_only=True`，返回已解析的参数字典；否则返回包含函数名的完整结构。

---

### 3. PydanticOutputFunctionsParser
**功能描述**: 将函数调用参数解析并验证为 Pydantic 模型实例。

#### 属性
| 属性名 | 类型 | 默认值 | 详细用途 |
| :--- | :--- | :--- | :--- |
| `pydantic_schema` | `type[BaseModel] \| dict` | - | 用于验证的目标 Pydantic 类。如果提供字典，则根据函数名选择对应的模型。 |

#### 核心方法
- **`parse_result`**: 首先调用父类逻辑提取原始数据，然后根据 `pydantic_schema` 进行 `model_validate_json` 转换。

---

## 核心逻辑
1. **数据来源**: 所有的函数调用解析器都从 `ChatGeneration` 消息的 `additional_kwargs` 中读取数据，因为 OpenAI 将函数调用信息放在该字段中而非正文内容中。
2. **流式 JSON 处理**: `JsonOutputFunctionsParser` 内部使用了 `parse_partial_json`。这使得在长文本输出过程中，用户可以立即看到已生成的 JSON 键值对，极大地提升了交互体验。
3. **版本兼容性**: 同时支持 Pydantic v1 和 v2 版本的模型验证。

---

## 使用示例

### 使用 Pydantic 解析特定的函数调用
```python
from pydantic import BaseModel
from langchain_core.output_parsers.openai_functions import PydanticOutputFunctionsParser

class UserInfo(BaseModel):
    name: str
    age: int

# 假设模型被告知要调用 "save_user" 函数
parser = PydanticOutputFunctionsParser(pydantic_schema=UserInfo)

# 模拟消息输入
from langchain_core.messages import AIMessage
import json

msg = AIMessage(
    content="",
    additional_kwargs={
        "function_call": {
            "name": "save_user",
            "arguments": json.dumps({"name": "张三", "age": 25})
        }
    }
)

# 解析
user = parser.invoke(msg)
print(f"姓名: {user.name}, 年龄: {user.age}")
```

---

## 注意事项
- **单结果限制**: `JsonOutputFunctionsParser` 明确要求结果列表中只能有一个 `Generation`。
- **输入限制**: 仅支持 `ChatGeneration`（聊天模型输出）。
- **字段位置**: 与工具调用（Tool Calls）不同，函数调用信息位于 `additional_kwargs["function_call"]` 路径下。

---

## 内部调用关系
- 它是许多高层 `OpenAIFunctionsAgent` 逻辑的核心组件。
- 依赖于 `langchain_core.output_parsers.json` 中的部分解析算法。

---

## 元信息
- **最后更新时间**: 2026-01-29
- **对应源码版本**: LangChain Core v1.2.7
