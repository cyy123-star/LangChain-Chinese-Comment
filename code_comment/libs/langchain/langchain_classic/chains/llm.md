# libs\langchain\langchain_classic\chains\llm.py

`llm.py` 实现了 LangChain 中最基础的链：`LLMChain`。

## 核心类

### `LLMChain`
该链的功能非常简单：将输入格式化为提示词（Prompt），然后调用语言模型（LLM），最后解析并返回结果。

#### 关键参数
| 参数 | 类型 | 描述 |
| :--- | :--- | :--- |
| `prompt` | `BasePromptTemplate` | 用于格式化输入的提示词模板。 |
| `llm` | `Runnable` | 要调用的语言模型。 |
| `output_key` | `str` | 输出字典中存储结果的键，默认为 "text"。 |
| `output_parser` | `BaseLLMOutputParser` | 用于处理 LLM 输出的解析器，默认为 `StrOutputParser`。 |
| `return_final_only` | `bool` | 是否只返回最终解析后的字符串。如果为 `False`，还会包含完整的生成信息。 |

#### 工作原理
1. **格式化提示词**: 根据输入变量填充 `prompt`。
2. **调用 LLM**: 将格式化后的提示词传递给 `llm`。
3. **解析输出**: 使用 `output_parser` 对模型的响应进行处理。
4. **返回结果**: 构造包含结果的字典。

## 弃用说明
`LLMChain` 已被标记为弃用。现代 LangChain 推荐使用 **LCEL (LangChain Expression Language)** 的管道语法：

```python
# 现代推荐写法
chain = prompt | llm | StrOutputParser()
result = chain.invoke({"adjective": "funny"})
```

相比之下，LCEL 更加灵活、透明，且天然支持异步、批处理和流式输出。

## 注意事项
- **输入变量**: `LLMChain` 的 `input_keys` 动态继承自 `prompt.input_variables`。
- **批量处理**: 提供了 `generate` 和 `agenerate` 方法，支持一次性处理多个输入。
