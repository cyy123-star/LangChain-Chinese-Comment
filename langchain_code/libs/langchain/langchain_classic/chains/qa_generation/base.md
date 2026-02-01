# QA Generation Chain

`qa_generation` 子模块提供了一个专门用于从给定文本中自动生成“问题-答案”对的 Chain。这在构建评估数据集或 FAQ 系统时非常有用。

## 核心组件

### 1. `QAGenerationChain`
核心 Chain 类，负责将输入文本拆分为块，并为每个块生成 QA 对。

| 属性 | 类型 | 描述 |
| :--- | :--- | :--- |
| `llm_chain` | `LLMChain` | 负责生成 QA 对的底层 LLM 链。 |
| `text_splitter` | `TextSplitter` | 用于拆分输入长文本的工具。默认使用 `RecursiveCharacterTextSplitter`。 |
| `input_key` | `str` | 输入文本的键名。默认 "text"。 |
| `output_key` | `str` | 输出结果的键名。默认 "questions"。 |

## 执行逻辑 (Verbatim Snippet)

`QAGenerationChain` 首先对文本进行切分，然后对每个切片并行执行生成：

```python
def _call(
    self,
    inputs: dict[str, Any],
    run_manager: CallbackManagerForChainRun | None = None,
) -> dict[str, list]:
    # 1. 切分文本
    docs = self.text_splitter.create_documents([inputs[self.input_key]])
    
    # 2. 对每个块生成 QA 对 (使用 LLMChain.generate 进行批处理)
    results = self.llm_chain.generate(
        [{"text": d.page_content} for d in docs],
        run_manager=run_manager,
    )
    
    # 3. 解析结果 (结果预期为 JSON 字符串)
    qa = [json.loads(res[0].text) for res in results.generations]
    return {self.output_key: qa}
```

## 迁移指南 (LCEL)

`QAGenerationChain` 已被弃用。使用 LCEL 可以更方便地实现异步处理和更复杂的解析逻辑。

### 现代 LCEL 示例
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnableLambda, RunnableEach
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. 定义拆分逻辑
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
split_text = RunnableLambda(lambda x: text_splitter.create_documents([x]))

# 2. 定义生成 Prompt
prompt = ChatPromptTemplate.from_template("Generate 3 QA pairs from this text: {text}. Output as JSON list.")

# 3. 组合 Chain (使用 RunnableEach 对拆分后的每个 Doc 执行)
chain = (
    split_text 
    | RunnableEach(bound=prompt | llm | JsonOutputParser())
)

result = chain.invoke("Your long text here...")
```
