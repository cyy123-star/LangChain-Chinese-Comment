# libs\langchain\langchain_classic\chains\structured_output\base.py

`structured_output` 模块提供了用于生成结构化数据输出的 LCEL `Runnable` 对象。它是 `openai_functions` 链的更现代、更灵活的替代方案，支持多种模式（Functions, Tools, JSON Mode）来确保 LLM 返回符合特定 Schema 的数据。

## 功能描述

该模块的核心在于将结构定义（如 Pydantic 模型）与 LLM 的特定功能（如 OpenAI 的函数调用）绑定，并自动配置相应的输出解析器。

## 核心方法

### 1. `create_openai_fn_runnable`
创建一个利用 OpenAI 函数调用功能的 Runnable。
- **参数**:
    - `functions`: 函数定义序列（Pydantic 类、字典或 Python 函数）。
    - `llm`: 语言模型。
    - `prompt`: 可选的提示词模板。
- **执行逻辑**: 将函数定义转换为 OpenAI Schema，使用 `llm.bind` 注入参数，并连接 `output_parser`。

### 2. `create_structured_output_runnable`
一个更通用的工厂方法，支持多种结构化输出模式。
- **模式 (`mode`)**:
    - `openai-functions`: 使用 OpenAI 函数调用。
    - `openai-tools`: 使用 OpenAI 工具调用（更现代）。
    - `openai-json`: 使用 OpenAI JSON 模式。

## 弃用说明与迁移

该模块中的工厂方法已被标记为弃用。**强烈建议**直接使用 Chat 模型自带的 `with_structured_output` 方法。

| 弃用方法 | 迁移目标 |
| :--- | :--- |
| `create_openai_fn_runnable` | `llm.with_structured_output(...)` |
| `create_structured_output_runnable` | `llm.with_structured_output(...)` |

### 现代用法示例 (LCEL)

```python
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

# 1. 定义输出结构
class Joke(BaseModel):
    setup: str = Field(description="The setup of the joke")
    punchline: str = Field(description="The punchline to the joke")

# 2. 绑定结构化输出 (推荐做法)
llm = ChatOpenAI(model="gpt-4o")
structured_llm = llm.with_structured_output(Joke)

# 3. 直接调用
joke = structured_llm.invoke("Tell me a cat joke")
```

## 注意事项

1.  **Pydantic 版本**: 建议使用 Pydantic v2，该模块已做了兼容性处理。
2.  **多函数选择**: 如果提供了多个函数，且 `enforce_single_function_usage` 为 `False`，模型将自行决定调用哪个函数，输出将包含被调用函数的名称和参数。
3.  **解析器自动推断**: 该模块能根据传入的 `functions` 类型自动选择最合适的解析器（如 `PydanticOutputFunctionsParser`），无需手动配置。
