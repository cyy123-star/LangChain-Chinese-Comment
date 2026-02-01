# Example Generator

`example_generator` 模块提供了一个简单的实用功能，用于根据现有的示例列表生成新的示例。它内部利用了 `FewShotPromptTemplate` 和 LLM 来实现这种“类比”生成。

## 核心函数：generate_example

该函数通过给定的示例列表和提示词模板，引导 LLM 生成一个新的、符合相同模式的示例。

### 参数说明

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `examples` | `list[dict]` | 现有的示例列表，每个示例是一个字典。 |
| `llm` | `BaseLanguageModel` | 用于生成新示例的语言模型。 |
| `prompt_template` | `PromptTemplate` | 定义单个示例格式的提示词模板。 |

### 执行逻辑 (Verbatim Snippet)

```python
def generate_example(
    examples: list[dict],
    llm: BaseLanguageModel,
    prompt_template: PromptTemplate,
) -> str:
    """给定一个示例列表，返回另一个示例。"""
    # 构造 FewShotPromptTemplate
    prompt = FewShotPromptTemplate(
        examples=examples,
        suffix="Add another example.", # 引导词
        input_variables=[],
        example_prompt=prompt_template,
    )
    # 构造简单的链：Prompt -> LLM -> String
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({})
```

## 迁移指南 (LCEL)

在现代 LangChain (LCEL) 中，你不再需要这个专门的辅助函数，因为用 LCEL 实现同样的功能非常简单且更具可读性：

```python
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. 定义你的示例和模板
examples = [{"input": "happy", "output": "sad"}]
example_prompt = PromptTemplate.from_template("Input: {input}\nOutput: {output}")

# 2. 构造 FewShot Prompt
dynamic_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    suffix="Input: {input}\nOutput: ",
    input_variables=["input"]
)

# 3. 组合成链
chain = dynamic_prompt | llm | StrOutputParser()

# 调用
new_example = chain.invoke({"input": "big"})
```

## 注意事项

- **示例质量**：生成的质量高度依赖于提供的 `examples` 的多样性和准确性。
- **后缀固定**：`generate_example` 函数中使用的后缀 `"Add another example."` 是硬编码的，这在某些复杂场景下可能不够灵活。

