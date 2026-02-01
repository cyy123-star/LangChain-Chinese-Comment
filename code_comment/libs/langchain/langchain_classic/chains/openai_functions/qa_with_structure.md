# QA with Structure Chain (OpenAI Functions)

`QA with Structure Chain` 允许用户定义问答系统的输出结构。通过结合 OpenAI 的函数调用功能，它可以强制模型以特定的 JSON 格式（如带有来源列表的回答）返回结果。

## 核心数据结构

### AnswerWithSources
默认的输出结构示例：
- `answer`: 对问题的回答。
- `sources`: 用于回答问题的来源列表（通常是文档 ID 或链接）。

## 参数表

| 参数 | 类型 | 说明 |
| :--- | :--- | :--- |
| `llm` | `BaseLanguageModel` | 支持函数调用的语言模型。 |
| `schema` | `dict \| type[BaseModel]` | 定义输出结构的 JSON Schema 或 Pydantic 类。 |
| `output_parser` | `str` | 输出解析器类型：`'pydantic'` (返回 Pydantic 实例) 或 `'base'` (返回字典)。默认为 `'base'`。 |
| `prompt` | `ChatPromptTemplate` | (可选) 自定义提示词模板。 |

## 执行逻辑 (Verbatim Snippet)

```python
def create_qa_with_structure_chain(
    llm: BaseLanguageModel,
    schema: dict | type[BaseModel],
    output_parser: str = "base",
    prompt: PromptTemplate | ChatPromptTemplate | None = None,
    verbose: bool = False,
) -> LLMChain:
    # 1. 根据 output_parser 类型选择解析器
    if output_parser == "pydantic":
        _output_parser = PydanticOutputFunctionsParser(pydantic_schema=schema)
    else:
        _output_parser = OutputFunctionsParser()

    # 2. 将 Pydantic schema 转换为 OpenAI 函数定义格式
    if isinstance(schema, type) and is_basemodel_subclass(schema):
        schema_dict = cast("dict", schema.model_json_schema())
    else:
        schema_dict = cast("dict", schema)
    
    function = {
        "name": schema_dict["title"],
        "description": schema_dict["description"],
        "parameters": schema_dict,
    }
    
    # 3. 获取函数调用的 kwargs (如 functions 和 function_call)
    llm_kwargs = get_llm_kwargs(function)
    
    # 4. 构建包含系统消息和上下文占位符的消息列表
    messages = [...] 
    prompt = prompt or ChatPromptTemplate(messages=messages)

    # 5. 返回封装好的 LLMChain
    return LLMChain(
        llm=llm,
        prompt=prompt,
        llm_kwargs=llm_kwargs,
        output_parser=_output_parser,
        verbose=verbose,
    )
```

## 迁移指南 (LCEL)

官方推荐使用 `with_structured_output` 结合 RAG 流程来替代此链。以下是一个现代化的等效实现：

```python
from typing import List
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

class StructuredAnswer(BaseModel):
    answer: str = Field(..., description="The answer to the user question")
    sources: List[str] = Field(..., description="The sources used to answer the question")

llm = ChatOpenAI(model="gpt-4o", temperature=0)
structured_llm = llm.with_structured_output(StructuredAnswer)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Answer the question using only the provided context."),
    ("human", "Context: {context}\n\nQuestion: {question}")
])

# 构建 LCEL 链
qa_chain = prompt | structured_llm

# 执行
result = qa_chain.invoke({
    "context": "LangChain is a framework for LLM apps. It was created in 2022.",
    "question": "What is LangChain?"
})
# result: StructuredAnswer(answer='LangChain is a framework for building LLM applications.', sources=['...'])
```
