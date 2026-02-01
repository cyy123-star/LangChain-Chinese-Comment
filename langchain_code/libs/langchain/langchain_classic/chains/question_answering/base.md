# Question Answering (QA) Chains

`question_answering` 子模块提供了一系列预配置的 Chain，用于从一组文档中回答问题。这些 Chain 封装了不同的文档组合策略（Combine Documents Strategies），并根据 LLM 的类型（如 Chat Model 或 LLM）自动选择合适的提示词。

## 核心组件

### 1. `load_qa_chain`
这是加载 QA Chain 的统一入口函数。它根据 `chain_type` 参数返回相应的 `BaseCombineDocumentsChain` 子类。

| 参数 | 类型 | 描述 |
| :--- | :--- | :--- |
| `llm` | `BaseLanguageModel` | 用于执行生成的语言模型。 |
| `chain_type` | `str` | 文档组合策略。可选值："stuff", "map_reduce", "refine", "map_rerank"。默认 "stuff"。 |
| `verbose` | `bool` | 是否开启详细模式。 |
| `**kwargs` | `Any` | 传递给底层 Chain 构造函数的其他参数。 |

## 文档组合策略

### 1. Stuff (填充)
将所有文档拼接后一次性输入给 LLM。
- **适用场景**: 文档总量较小，且能放入 LLM 的上下文窗口内。
- **优点**: 简单、高效，LLM 拥有完整的上下文。

### 2. Map-Reduce (映射-归约)
对每个文档分别执行 QA（Map），然后将所有结果汇总（Reduce）得到最终答案。
- **适用场景**: 处理大量文档，超出上下文限制。
- **优点**: 可并行处理，适合大规模数据。

### 3. Refine (精炼)
循环遍历文档。首先对第一个文档进行 QA，然后将结果与第二个文档一起输入给 LLM 以改进答案，以此类推。
- **适用场景**: 需要通过上下文逐步完善答案。
- **优点**: 答案通常更详细、更准确。

### 4. Map-Rerank (映射-重排序)
对每个文档执行 QA，并让 LLM 给出一个置信度分数。最后返回分数最高的答案。
- **适用场景**: 答案通常存在于单个文档中。
- **优点**: 能够处理大量文档并识别最相关的部分。

## 执行逻辑 (Verbatim Snippet)

以下是 `load_qa_chain` 如何根据 `chain_type` 分发逻辑的片段：

```python
def load_qa_chain(
    llm: BaseLanguageModel,
    chain_type: str = "stuff",
    verbose: bool | None = None,
    callback_manager: BaseCallbackManager | None = None,
    **kwargs: Any,
) -> BaseCombineDocumentsChain:
    loader_mapping: Mapping[str, LoadingCallable] = {
        "stuff": _load_stuff_chain,
        "map_reduce": _load_map_reduce_chain,
        "refine": _load_refine_chain,
        "map_rerank": _load_map_rerank_chain,
    }
    if chain_type not in loader_mapping:
        raise ValueError(f"Got unsupported chain type: {chain_type}.")
    return loader_mapping[chain_type](
        llm,
        verbose=verbose,
        callback_manager=callback_manager,
        **kwargs,
    )
```

## 迁移指南 (LCEL)

`load_qa_chain` 已被弃用。建议使用 LCEL 风格的实现。

### Stuff 迁移示例
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_template("Answer based on context: {context}\nQuestion: {question}")
chain = (
    {"context": lambda x: "\n\n".join(d.page_content for d in x["docs"]), "question": itemgetter("question")}
    | prompt
    | llm
    | StrOutputParser()
)
```

更多迁移指南：
- [Stuff Docs Chain](https://python.langchain.com/docs/versions/migrating_chains/stuff_docs_chain)
- [Map Reduce Chain](https://python.langchain.com/docs/versions/migrating_chains/map_reduce_chain)
- [Refine Chain](https://python.langchain.com/docs/versions/migrating_chains/refine_chain)
- [Map Rerank Docs Chain](https://python.langchain.com/docs/versions/migrating_chains/map_rerank_docs_chain)
