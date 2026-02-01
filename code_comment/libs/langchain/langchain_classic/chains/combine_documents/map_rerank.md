# libs\langchain\langchain_classic\chains\combine_documents\map_rerank.py

`MapRerankDocumentsChain` 是一种文档合并策略。它对每个输入文档独立运行一个链（通常是 `LLMChain`），该链不仅生成答案，还会生成一个置信度评分（Score）。最后，该链会返回评分最高的那个答案。

## 功能描述

该模块实现了 Map-Rerank 算法，主要步骤如下：
1.  **独立映射 (Map)**：将每个文档分别输入到 `llm_chain` 中。
2.  **结果解析**：`llm_chain` 的输出解析器（通常是 `RegexParser`）会从 LLM 的响应中提取出“答案”和“分数”。
3.  **重新排名 (Rerank)**：根据分数对所有文档的结果进行排序，选择分数最高的项。
4.  **返回结果**：返回最高分的答案，并可选择性地返回关联的元数据。

## 弃用说明

该类已弃用。建议参考官方迁移指南，使用 LCEL 构建更灵活的重排序流程。

| 类/属性 | 迁移目标 |
2024-10-14 迁移建议链接 | [Map-Rerank 迁移指南](https://python.langchain.com/docs/versions/migrating_chains/map_rerank_docs_chain/) |

## 参数说明

| 参数名 | 类型 | 默认值 | 描述 |
| :--- | :--- | :--- | :--- |
| `llm_chain` | `LLMChain` | **必填** | 应用于每个独立文档的链。其 Prompt 必须包含提取分数和答案的逻辑。 |
| `document_variable_name` | `str` | - | `llm_chain` 中用于接收文档内容的变量名。如果链中只有一个变量，则可选。 |
| `rank_key` | `str` | **必填** | `llm_chain` 输出中代表“分数”的键名，用于重排序。 |
| `answer_key` | `str` | **必填** | `llm_chain` 输出中代表“答案”的键名，用于返回最终结果。 |
| `metadata_keys` | `list[str]` | `None` | (可选) 需要从选定文档中额外返回的元数据键名列表。 |
| `return_intermediate_steps` | `bool` | `False` | 是否返回每个文档的处理结果（中间步骤）。 |

## 执行逻辑 (Verbatim Snippet)

核心逻辑位于 `combine_docs` 方法中：

```python
def combine_docs(
    self,
    docs: list[Document],
    callbacks: Callbacks = None,
    **kwargs: Any,
) -> tuple[str, dict]:
    """通过映射和重排序来合并文档。"""
    # 1. 对每个文档执行 LLM 链并解析结果
    results = self.llm_chain.apply_and_parse(
        [{self.document_variable_name: d.page_content, **kwargs} for d in docs],
        callbacks=callbacks,
    )
    
    # 2. 处理结果并进行重排序
    return self._process_results(docs, results)

def _process_results(
    self,
    docs: list[Document],
    results: list[dict],
) -> tuple[str, dict]:
    # 找到分数最高的索引
    best_result = results[0]
    best_idx = 0
    for i, res in enumerate(results):
        if res[self.rank_key] > best_result[self.rank_key]:
            best_result = res
            best_idx = i
            
    # 构造输出
    output = {self.output_key: best_result[self.answer_key]}
    # ... (处理元数据和中间步骤)
    return best_result[self.answer_key], extra_info
```

## 迁移建议 (LCEL)

建议使用 LCEL 结合结构化输出（Structured Output）来实现类似功能。

### 示例：使用结构化输出进行 Map-Rerank

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

# 1. 定义输出结构
class AnswerWithScore(BaseModel):
    answer: str = Field(description="The answer to the question")
    score: int = Field(description="Confidence score from 0 to 100")

# 2. 准备模型和 Prompt
llm = ChatOpenAI(model="gpt-4o")
structured_llm = llm.with_structured_output(AnswerWithScore)
prompt = ChatPromptTemplate.from_template("Context: {context}\nQuestion: {question}")

# 3. 构建链
map_chain = prompt | structured_llm

# 4. 手动处理多个文档 (伪代码)
def map_rerank(inputs):
    docs = inputs["docs"]
    question = inputs["question"]
    # Map
    results = [map_chain.invoke({"context": d.page_content, "question": question}) for d in docs]
    # Rerank
    best = max(results, key=lambda x: x.score)
    return best.answer
```

## 注意事项

1.  **Prompt 复杂度**：Prompt 必须非常明确地要求模型输出分数，且格式需固定以便解析。
2.  **效率问题**：对每个文档都调用一次 LLM（Map），对于长文档或文档数量较多时，Token 消耗较大且速度较慢。
3.  **解析器选择**：通常与 `RegexParser` 配合使用，利用正则表达式从非结构化文本中强行提取分数。
