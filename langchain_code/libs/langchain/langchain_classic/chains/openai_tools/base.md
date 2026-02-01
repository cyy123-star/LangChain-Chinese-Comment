# OpenAI Tools Chains

`openai_tools` 子模块利用 OpenAI 的工具调用（Tool Calling）能力来执行结构化数据提取等任务。它是对 `openai_functions` 的升级，支持更强大的多工具调用。

## 核心组件

### 1. `create_extraction_chain_pydantic`
创建一个利用 OpenAI Tools 提取 Pydantic 对象的 Chain。

| 参数 | 类型 | 描述 |
| :--- | :--- | :--- |
| `pydantic_schemas` | `Union[List[Type[BaseModel]], Type[BaseModel]]` | 定义提取目标的 Pydantic 模型。 |
| `llm` | `BaseLanguageModel` | 必须是支持工具调用的 OpenAI 模型。 |
| `system_message` | `str` | 指导提取任务的系统提示词。 |

## 执行逻辑 (Verbatim Snippet)

该函数通过将 Pydantic 模型转换为 OpenAI 函数定义，并将其绑定到 LLM 上来实现提取：

```python
def create_extraction_chain_pydantic(
    pydantic_schemas: list[type[BaseModel]] | type[BaseModel],
    llm: BaseLanguageModel,
    system_message: str = _EXTRACTION_TEMPLATE,
) -> Runnable:
    if not isinstance(pydantic_schemas, list):
        pydantic_schemas = [pydantic_schemas]
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("user", "{input}"),
    ])
    # 转换为 OpenAI 函数格式
    functions = [convert_pydantic_to_openai_function(p) for p in pydantic_schemas]
    # 包装为工具格式
    tools = [{"type": "function", "function": d} for d in functions]
    # 绑定工具到模型
    model = llm.bind(tools=tools)
    # 组合为 Runnable：Prompt -> Model -> Parser
    return prompt | model | PydanticToolsParser(tools=pydantic_schemas)
```

## 迁移指南 (LCEL)

此函数已被弃用，建议直接使用 ChatModel 的 `with_structured_output` 方法。

### 现代 LCEL 示例
```python
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

class UserInfo(BaseModel):
    name: str = Field(description="The user's name")
    age: int = Field(description="The user's age")

model = ChatOpenAI(model="gpt-4o")
# 使用 with_structured_output
structured_model = model.with_structured_output(UserInfo)

result = structured_model.invoke("My name is John and I am 30 years old.")
print(result) # UserInfo(name='John', age=30)
```

参考：[Structured Outputs](https://python.langchain.com/docs/how_to/structured_output/)
