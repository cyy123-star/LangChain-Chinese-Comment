# Structured Output Chains (Deprecated)

`structured_output` 模块提供了一系列用于生成结构化数据（如 JSON, Pydantic 对象）的工具函数和链。

> **警告**: 该模块中的大部分方法自 v0.1.14 起已弃用。建议使用 ChatModels 原生的 `with_structured_output` 方法。

## 核心功能

主要通过 `create_openai_fn_runnable` 等函数，利用 OpenAI 的函数调用（Function Calling）功能来提取结构化信息。

### `create_openai_fn_runnable`
创建一个能够调用特定函数并返回结构化结果的 Runnable 序列。

| 参数 | 类型 | 说明 |
| :--- | :--- | :--- |
| `functions` | `Sequence` | 定义结构的 Pydantic 模型、Python 函数或字典。 |
| `llm` | `Runnable` | 支持函数调用的模型。 |
| `prompt` | `Optional[BasePromptTemplate]` | 引导模型执行提取任务的提示词。 |
| `enforce_single_function_usage` | `bool` | 是否强制模型使用指定的函数。 |

## 执行逻辑

1. **结构转换**: 将 Pydantic 模型或 Python 函数转换为 OpenAI 格式的函数定义。
2. **模型调用**: 调用模型并传递函数定义。
3. **输出解析**: 根据定义的结构自动解析模型的输出。

```python
# 核心逻辑 (简化)
def create_openai_fn_runnable(functions, llm, prompt):
    # 1. 转换结构
    oai_functions = [convert_to_openai_function(f) for f in functions]
    # 2. 绑定到模型
    llm_with_fns = llm.bind(functions=oai_functions)
    # 3. 组合成 LCEL 链
    return prompt | llm_with_fns | output_parser
```

## 迁移方案 (推荐)

现代做法是直接在支持工具调用的 ChatModel 上调用 `with_structured_output`：

```python
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

class Person(BaseModel):
    name: str = Field(description="人的姓名")
    age: int = Field(description="人的年龄")

model = ChatOpenAI(model="gpt-4o")
# 这种方式更简洁、类型安全，且支持更多模型（Anthropic, Google 等）
structured_model = model.with_structured_output(Person)
result = structured_model.invoke("我的名字是张三，今年 25 岁。")
# result 为 Person(name="张三", age=25)
```

## 适用场景

- **信息提取**: 从非结构化文本中提取特定字段。
- **数据转换**: 将自然语言指令转换为 API 调用参数。
- **分类标签**: 为文本打上结构化的标签。
