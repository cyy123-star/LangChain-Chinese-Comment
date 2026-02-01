# Tagging Chain (OpenAI Functions)

`Tagging Chain` 是一类专门用于给文本打标签或提取元数据的链。它利用 OpenAI 的函数调用（Function Calling）功能，确保模型输出符合预定义的 JSON 结构。

## 核心组件

- **Schema**: 定义要提取的标签及其属性（如情感、语言、关键词等）。可以是 Python 字典（JSON Schema）或 Pydantic 模型。
- **LLM**: 支持函数调用的语言模型（通常是 OpenAI 模型）。
- **Prompt**: 默认提示词，指导模型仅提取 `information_extraction` 函数中定义的属性。
- **Output Parser**: 
    - `JsonOutputFunctionsParser`: 解析为字典。
    - `PydanticOutputFunctionsParser`: 解析为 Pydantic 实例。

## 参数表 (create_tagging_chain)

| 参数 | 类型 | 说明 |
| :--- | :--- | :--- |
| `schema` | `dict` | 定义标签结构的 JSON Schema。 |
| `llm` | `BaseLanguageModel` | 支持函数调用的语言模型。 |
| `prompt` | `ChatPromptTemplate` | (可选) 自定义提示词模板。 |

## 参数表 (create_tagging_chain_pydantic)

| 参数 | 类型 | 说明 |
| :--- | :--- | :--- |
| `pydantic_schema` | `Any` | Pydantic 类，定义标签结构。 |
| `llm` | `BaseLanguageModel` | 支持函数调用的语言模型。 |
| `prompt` | `ChatPromptTemplate` | (可选) 自定义提示词模板。 |

## 执行逻辑 (Verbatim Snippet)

```python
def create_tagging_chain(
    schema: dict,
    llm: BaseLanguageModel,
    prompt: ChatPromptTemplate | None = None,
    **kwargs: Any,
) -> Chain:
    # 1. 构建 OpenAI 函数定义
    function = _get_tagging_function(schema)
    # 2. 设置提示词
    prompt = prompt or ChatPromptTemplate.from_template(_TAGGING_TEMPLATE)
    # 3. 设置输出解析器
    output_parser = JsonOutputFunctionsParser()
    # 4. 获取 LLM 函数调用参数
    llm_kwargs = get_llm_kwargs(function)
    # 5. 返回封装好的 LLMChain
    return LLMChain(
        llm=llm,
        prompt=prompt,
        llm_kwargs=llm_kwargs,
        output_parser=output_parser,
        **kwargs,
    )
```

## 迁移指南 (LCEL)

官方推荐使用 `with_structured_output` 替代此链：

```python
from typing import List
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

class Tags(BaseModel):
    sentiment: str = Field(..., description="The sentiment of the text")
    language: str = Field(..., description="The language of the text")

llm = ChatOpenAI(model="gpt-4o", temperature=0)
tagger = llm.with_structured_output(Tags)

# 使用方式
result = tagger.invoke("I am very happy with this product! It's amazing.")
# result: Tags(sentiment='positive', language='English')
```
