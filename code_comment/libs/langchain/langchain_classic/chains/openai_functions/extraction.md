# libs\langchain\langchain_classic\chains\openai_functions\extraction.py

`create_extraction_chain` 是一个专门用于从文本中提取多个实体实例的工具。它通过 OpenAI 的函数调用功能，确保提取出的实体符合预定义的 JSON Schema。

## 功能描述

该链的主要逻辑是将用户定义的 Schema 包装成一个名为 `information_extraction` 的函数，并要求模型将所有发现的实体放入一个数组中。

## 核心方法：create_extraction_chain

### 参数说明

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `schema` | `dict` | 实体结构的 JSON Schema 定义。 |
| `llm` | `BaseLanguageModel` | 支持函数调用的语言模型。 |
| `prompt` | `BasePromptTemplate` | (可选) 自定义提取 Prompt。默认会提示模型“提取并保存文本中提到的相关实体”。 |

### 执行逻辑 (Verbatim Snippet)

核心逻辑在于构造 `information_extraction` 函数定义：

```python
def _get_extraction_function(entity_schema: dict) -> dict:
    return {
        "name": "information_extraction",
        "description": "Extracts the relevant information from the passage.",
        "parameters": {
            "type": "object",
            "properties": {
                # 关键：将用户 Schema 放入一个数组中，允许提取多个实例
                "info": {"type": "array", "items": _convert_schema(entity_schema)},
            },
            "required": ["info"],
        },
    }
```

## 弃用说明与迁移

该方法已弃用。建议使用支持 `with_structured_output` 的模型配合 `list` 类型的 Pydantic 模型。

---

# libs\langchain\langchain_classic\chains\openai_functions\tagging.py

`create_tagging_chain` 用于对文本进行标记或分类。与 `extraction_chain` 不同，它通常用于提取关于文本整体属性的信息（如情感、语言、主题等），而不是提取文本中的具体实体列表。

## 功能描述

该链将标记任务转化为一个函数调用，其中函数的参数即为用户想要标记的属性。

## 核心方法：create_tagging_chain

### 参数说明

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `schema` | `dict` | 标记属性的 JSON Schema 定义。 |
| `llm` | `BaseLanguageModel` | 支持函数调用的语言模型。 |
| `prompt` | `ChatPromptTemplate` | (可选) 自定义标记 Prompt。 |

### 示例用法 (旧版)

```python
schema = {
    "properties": {
        "sentiment": {"type": "string", "enum": ["happy", "neutral", "sad"]},
        "language": {"type": "string"}
    }
}
chain = create_tagging_chain(schema, llm)
res = chain.run("I am so happy to see you!")
# 输出: {'sentiment': 'happy', 'language': 'English'}
```

## 注意事项

1.  **Extraction vs Tagging**：
    - `extraction_chain` 适用于提取**多个实体**（如从新闻中提取所有提到的人物）。
    - `tagging_chain` 适用于提取**单组属性**（如判断一封邮件的情感倾向和紧急程度）。
2.  **Schema 定义**：对于分类任务，建议在 Schema 中使用 `enum` 来限制 LLM 的输出范围，提高准确性。
