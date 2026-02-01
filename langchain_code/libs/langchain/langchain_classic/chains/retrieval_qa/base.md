# Retrieval QA Chain

`RetrievalQA` 是一个用于针对索引（如向量数据库）进行问答的经典链。它接收一个查询，通过检索器获取相关文档，然后使用组合文档链（如 Stuff）生成答案。

## 核心组件

| 组件 | 类型 | 说明 |
| :--- | :--- | :--- |
| `combine_documents_chain` | `BaseCombineDocumentsChain` | 用于组合检索到的文档并生成最终答案的链。 |
| `retriever` | `BaseRetriever` | 用于根据查询检索相关文档的组件。 |

## 参数表格

| 参数 | 类型 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- |
| `input_key` | `str` | `"query"` | 输入字典中查询的键名。 |
| `output_key` | `str` | `"result"` | 输出字典中答案的键名。 |
| `return_source_documents` | `bool` | `False` | 是否在输出中返回检索到的源文档。 |

## 执行逻辑 (Verbatim Snippet)

以下是 `BaseRetrievalQA._call` 的核心执行逻辑：

```python
def _call(
    self,
    inputs: dict[str, Any],
    run_manager: CallbackManagerForChainRun | None = None,
) -> dict[str, Any]:
    _run_manager = run_manager or CallbackManagerForChainRun.get_noop_manager()
    question = inputs[self.input_key]
    
    # 获取文档
    docs = self._get_docs(question, run_manager=_run_manager)
    
    # 组合文档并生成回答
    answer = self.combine_documents_chain.run(
        input_documents=docs,
        question=question,
        callbacks=_run_manager.get_child(),
    )

    if self.return_source_documents:
        return {self.output_key: answer, "source_documents": docs}
    return {self.output_key: answer}
```

## 迁移指南 (LCEL)

`RetrievalQA` 已被弃用。建议使用 `create_retrieval_chain` 构造函数。

### 现代写法示例：

```python
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# 1. 定义提示词
system_prompt = (
    "Use the given context to answer the question. "
    "Context: {context}"
)
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

# 2. 创建组合文档链
model = ChatOpenAI()
question_answer_chain = create_stuff_documents_chain(model, prompt)

# 3. 创建检索链
chain = create_retrieval_chain(retriever, question_answer_chain)

# 使用方式
chain.invoke({"input": "What is the capital of France?"})
```
