# Output Parsers (输出解析器)

`output_parsers` 模块负责将 LLM 返回的非结构化文本转换为结构化的数据对象（如 JSON, Pydantic 模型, 列表等）。

## 核心职责

1. **指令生成**: 生成一段提示文字（`get_format_instructions`），告诉 LLM 应该以什么格式输出。
2. **结果解析**: 将 LLM 的字符串响应解析为 Python 对象。
3. **容错与重试**: 处理格式错误的响应，甚至可以配合 LLM 进行自动修正。

## 常用解析器

| 解析器 | 说明 |
| :--- | :--- |
| `PydanticOutputParser` | **最常用**。根据定义的 Pydantic 类解析为结构化对象。 |
| `JsonOutputParser` | 直接解析为 Python 字典或列表。 |
| `CommaSeparatedListOutputParser` | 解析逗号分隔的列表。 |
| `DatetimeOutputParser` | 解析日期和时间字符串。 |
| `EnumOutputParser` | 解析为预定义的枚举值。 |
| `StructuredOutputParser` | 解析为指定的 JSON 结构（不支持 Pydantic 时使用）。 |
| `XMLOutputParser` | 解析 XML 格式数据。 |

## 进阶功能

- **OutputFixingParser**: 如果第一个解析器失败，它会将错误信息和原始输出发回给 LLM，要求其修复格式。
- **RetryOutputParser**: 在解析失败时，结合提示词和模型进行更深入的重试。

## 使用示例

```python
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

class Joke(BaseModel):
    setup: str = Field(description="question to set up a joke")
    punchline: str = Field(description="answer to resolve the joke")

parser = PydanticOutputParser(pydantic_object=Joke)

# 1. 获取格式指令并加入 Prompt
# parser.get_format_instructions()

# 2. 解析输出
# result = parser.parse(llm_output)
```

## 现代方案：`with_structured_output`

在现代 LangChain 中，如果模型支持 **Tool Calling** (如 GPT-4, Claude 3)，建议直接使用：
```python
structured_llm = llm.with_structured_output(Joke)
result = structured_llm.invoke("Tell me a joke")
```
这种方式比手动提示词解析更加稳健且高效。
