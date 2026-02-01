# libs\langchain\langchain_classic\chains\qa_with_sources\base.py

`QAWithSourcesChain` 是一个专门用于处理带源引用的问答任务的链。它通过结合多个文档来生成答案，并尝试从生成的文本中提取出引用的来源。

## 功能描述

该模块定义了 `BaseQAWithSourcesChain` 基类及其实现类 `QAWithSourcesChain`。其核心逻辑是：
1.  **获取文档**：从输入中获取相关的文档列表。
2.  **合并文档**：调用内部的 `combine_documents_chain`（如 `StuffDocumentsChain` 或 `MapReduceDocumentsChain`）来生成包含答案和来源的原始文本。
3.  **解析结果**：使用正则匹配提取出 "SOURCES:" 之后的内容作为引用来源。

## 参数说明

### BaseQAWithSourcesChain / QAWithSourcesChain

| 参数名 | 类型 | 默认值 | 描述 |
| :--- | :--- | :--- | :--- |
| `combine_documents_chain` | `BaseCombineDocumentsChain` | **必填** | 用于合并文档并生成答案的底层链。 |
| `question_key` | `str` | `"question"` | 输入字典中问题的键名。 |
| `input_docs_key` | `str` | `"docs"` | 输入字典中待处理文档列表的键名（仅 `QAWithSourcesChain` 使用）。 |
| `answer_key` | `str` | `"answer"` | 输出字典中纯答案的键名。 |
| `sources_answer_key` | `str` | `"sources"` | 输出字典中提取出的来源字符串的键名。 |
| `return_source_documents` | `bool` | `False` | 是否在结果中返回原始 `Document` 对象列表。 |

## 工厂方法

`BaseQAWithSourcesChain` 提供了便捷的工厂方法来快速构造链。

### 1. `from_llm` (Map-Reduce 模式)
该方法会自动配置一个 `MapReduceDocumentsChain`。它先对每个文档生成摘要（Map），然后将所有摘要合并生成最终答案（Reduce）。

```python
@classmethod
def from_llm(
    cls,
    llm: BaseLanguageModel,
    document_prompt: BasePromptTemplate = EXAMPLE_PROMPT,
    question_prompt: BasePromptTemplate = QUESTION_PROMPT,
    combine_prompt: BasePromptTemplate = COMBINE_PROMPT,
    **kwargs: Any,
) -> BaseQAWithSourcesChain:
    """从 LLM 构造链。"""
    # 1. 为 Map 阶段准备 LLMChain (生成摘要)
    llm_question_chain = LLMChain(llm=llm, prompt=question_prompt)
    # 2. 为 Reduce 阶段准备 LLMChain (合并摘要)
    llm_combine_chain = LLMChain(llm=llm, prompt=combine_prompt)
    # 3. 构造 StuffDocumentsChain 作为 Reduce 的核心
    combine_results_chain = StuffDocumentsChain(
        llm_chain=llm_combine_chain,
        document_prompt=document_prompt,
        document_variable_name="summaries",
    )
    # 4. 封装成 ReduceDocumentsChain
    reduce_documents_chain = ReduceDocumentsChain(
        combine_documents_chain=combine_results_chain,
    )
    # 5. 最终构造 MapReduceDocumentsChain
    combine_documents_chain = MapReduceDocumentsChain(
        llm_chain=llm_question_chain,
        reduce_documents_chain=reduce_documents_chain,
        document_variable_name="context",
    )
    return cls(combine_documents_chain=combine_documents_chain, **kwargs)
```

### 2. `from_chain_type` (灵活模式)
允许用户指定合并策略（`stuff`, `map_reduce`, `refine`, `map_rerank`）。

```python
@classmethod
def from_chain_type(
    cls,
    llm: BaseLanguageModel,
    chain_type: str = "stuff",
    chain_type_kwargs: dict | None = None,
    **kwargs: Any,
) -> BaseQAWithSourcesChain:
    """根据 chain_type 加载链。"""
    _chain_kwargs = chain_type_kwargs or {}
    # 使用 loading 模块加载对应的合并文档链
    combine_documents_chain = load_qa_with_sources_chain(
        llm,
        chain_type=chain_type,
        **_chain_kwargs,
    )
    return cls(combine_documents_chain=combine_documents_chain, **kwargs)
```

## 执行逻辑 (Verbatim Snippet)

核心执行流程位于 `_call` 方法中：

```python
def _call(
    self,
    inputs: dict[str, Any],
    run_manager: CallbackManagerForChainRun | None = None,
) -> dict[str, str]:
    _run_manager = run_manager or CallbackManagerForChainRun.get_noop_manager()
    # 1. 获取文档（由子类实现）
    docs = self._get_docs(inputs, run_manager=_run_manager)

    # 2. 调用合并文档链生成原始答案
    answer = self.combine_documents_chain.run(
        input_documents=docs,
        callbacks=_run_manager.get_child(),
        **inputs,
    )
    
    # 3. 解析答案，拆分出正文和来源
    answer, sources = self._split_sources(answer)
    
    result: dict[str, Any] = {
        self.answer_key: answer,
        self.sources_answer_key: sources,
    }
    # 4. 可选：返回原始文档
    if self.return_source_documents:
        result["source_documents"] = docs
    return result
```

源引用拆分逻辑 `_split_sources` 使用正则表达式：

```python
def _split_sources(self, answer: str) -> tuple[str, str]:
    """从回答中拆分来源。"""
    if re.search(r"SOURCES?:", answer, re.IGNORECASE):
        answer, sources = re.split(
            r"SOURCES?:|QUESTION:\s",
            answer,
            flags=re.IGNORECASE,
        )[:2]
        sources = re.split(r"\n", sources)[0].strip()
    else:
        sources = ""
    return answer, sources
```

## 迁移建议 (LCEL)

`QAWithSourcesChain` 已被弃用。建议使用 LCEL (LangChain Expression Language) 构建更灵活的检索问答链。

### LCEL 等效实现示例

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# 定义模板，要求模型在回答末尾包含 SOURCES
template = """Answer the question based only on the following context:
{context}

Question: {question}
Answer in the following format:
Answer: [your answer]
SOURCES: [list of sources]
"""
prompt = ChatPromptTemplate.from_template(template)

def format_docs(docs):
    return "\n\n".join(f"Content: {d.page_content}\nSource: {d.metadata['source']}" for d in docs)

chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
```

## 注意事项

1.  **提示词依赖**：该链高度依赖提示词模板，要求模型必须按照 `SOURCES:` 格式输出，否则无法提取。
2.  **结构固定**：相比 LCEL，这种传统 Chain 的结构较为僵化，难以在中间插入自定义逻辑（如重排或复杂的文档过滤）。
3.  **来源解析局限**：`_split_sources` 仅能提取一行来源信息，且对格式非常敏感。

