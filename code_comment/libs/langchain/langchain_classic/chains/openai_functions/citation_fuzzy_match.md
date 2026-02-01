# Citation Fuzzy Match Chain (OpenAI Functions)

`Citation Fuzzy Match Chain` 用于生成带有精确引用的回答。它要求模型从上下文中提取直接引语作为支持事实的证据，并使用模糊匹配（Fuzzy Matching）来定位引文在原始文本中的位置。

## 核心数据结构

### FactWithEvidence
表示单个事实及其证据：
- `fact`: 事实本身的陈述。
- `substring_quote`: 从上下文中直接引用的字符串列表。

### QuestionAnswer
表示完整的问题回答：
- `question`: 提出的问题。
- `answer`: `FactWithEvidence` 对象的列表。

## 参数表

| 参数 | 类型 | 说明 |
| :--- | :--- | :--- |
| `llm` | `BaseLanguageModel` | 支持函数调用（或工具调用）的语言模型。 |

## 执行逻辑 (Verbatim Snippet)

### 模糊匹配逻辑
`FactWithEvidence` 类包含一个 `_get_span` 方法，使用 `regex` 库进行模糊搜索：

```python
def _get_span(self, quote: str, context: str, errs: int = 100) -> Iterator[str]:
    import regex
    minor = quote
    major = context
    errs_ = 0
    # 逐渐增加允许的错误数量（编辑距离），直到找到匹配项
    s = regex.search(f"({minor}){{e<={errs_}}}", major)
    while s is None and errs_ <= errs:
        errs_ += 1
        s = regex.search(f"({minor}){{e<={errs_}}}", major)
    if s is not None:
        yield from s.spans()
```

### 链构建逻辑
```python
def create_citation_fuzzy_match_chain(llm: BaseLanguageModel) -> LLMChain:
    output_parser = PydanticOutputFunctionsParser(pydantic_schema=QuestionAnswer)
    schema = QuestionAnswer.model_json_schema()
    function = {
        "name": schema["title"],
        "description": schema["description"],
        "parameters": schema,
    }
    llm_kwargs = get_llm_kwargs(function)
    # 构建包含系统提示词和上下文引用的多消息模板
    prompt = ChatPromptTemplate(messages=messages)
    return LLMChain(
        llm=llm,
        prompt=prompt,
        llm_kwargs=llm_kwargs,
        output_parser=output_parser,
    )
```

## 迁移指南 (LCEL)

推荐使用 `create_citation_fuzzy_match_runnable`，它内部使用了现代的 `with_structured_output` 接口：

```python
from langchain_classic.chains import create_citation_fuzzy_match_runnable
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o", temperature=0)
chain = create_citation_fuzzy_match_runnable(model)

context = "LangChain was created by Harrison Chase in 2022. It is a framework for building LLM apps."
question = "Who created LangChain and when?"

result = chain.invoke({"question": question, "context": context})
# result 将是一个 QuestionAnswer 对象，包含事实和原文引用
```
