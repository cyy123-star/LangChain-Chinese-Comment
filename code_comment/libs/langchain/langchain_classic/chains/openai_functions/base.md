# libs\langchain\langchain_classic\chains\openai_functions\base.py

`openai_functions` 模块提供了一系列用于创建利用 OpenAI 函数调用（Function Calling）API 的链。它是将非结构化文本转换为结构化数据、执行工具调用以及进行分类和标记的核心工具。

## 功能描述

该模块通过将 Python 对象（如 Pydantic 模型、字典或函数）转换为 OpenAI 的 `functions` 参数格式，使 LLM 能够以结构化的 JSON 格式返回结果。

## 核心方法：create_openai_fn_chain

### 参数说明

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `functions` | `Sequence` | 函数定义列表。可以是字典、Pydantic 类或 Python 函数。 |
| `llm` | `BaseLanguageModel` | 支持函数调用的语言模型（通常是 OpenAI 的 Chat 模型）。 |
| `prompt` | `BasePromptTemplate` | 传给模型的 Prompt。 |
| `enforce_single_function_usage` | `bool` | 如果只提供了一个函数，是否强制模型必须使用该函数。默认为 `True`。 |
| `output_parser` | `BaseLLMOutputParser` | (可选) 用于解析模型输出的解析器。默认会根据函数类型自动推断。 |

### 执行逻辑

1.  **函数转换**：利用 `convert_to_openai_function` 将输入的 `functions` 转换为 OpenAI 规范的 JSON Schema。
2.  **LLM 配置**：在调用 LLM 时，将转换后的 Schema 注入到 `functions` 参数中。
3.  **结果解析**：根据定义的 Schema，将 LLM 返回的 JSON 字符串解析回 Python 对象或字典。

## 弃用说明与迁移建议

该模块中的许多工厂方法已被标记为弃用。现代做法是使用 Chat 模型自带的 `with_structured_output` 方法，它支持 LCEL 且逻辑更简洁。

| 弃用方法 | 迁移目标 |
| :--- | :--- |
| `create_openai_fn_chain` | `llm.with_structured_output(...)` |
| `create_structured_output_chain` | `llm.with_structured_output(...)` |

### 现代用法示例 (LCEL)

```python
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

# 1. 定义输出结构
class Person(BaseModel):
    name: str = Field(description="The person's name")
    age: int = Field(description="The person's age")

# 2. 绑定结构化输出
llm = ChatOpenAI(model="gpt-4o")
structured_llm = llm.with_structured_output(Person)

# 3. 执行
person = structured_llm.invoke("My name is John and I am 30 years old.")
# 输出: Person(name='John', age=30)
```

## 注意事项

1.  **模型兼容性**：并非所有模型都支持函数调用。确保使用的模型（如 `gpt-3.5-turbo`, `gpt-4o`）具备此功能。
2.  **Schema 描述**：Pydantic 模型的字段 `description` 和类 `docstring` 对于 LLM 准确理解字段含义至关plus重要。
3.  **安全性**：如果函数调用涉及到执行代码或访问外部系统，请务必进行输入验证。
