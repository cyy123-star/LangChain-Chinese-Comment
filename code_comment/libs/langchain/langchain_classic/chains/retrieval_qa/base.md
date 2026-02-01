# libs\langchain\langchain_classic\chains\retrieval_qa\base.py

## 文件概述

`base.py` 定义了经典 RAG (Retrieval-Augmented Generation) 流程的核心链：`RetrievalQA`。它将“检索器（Retriever）”和“文档组合链（Combine Documents Chain）”结合在一起，实现了基于向量数据库的问答功能。

## 核心类：RetrievalQA (已弃用)

### 功能描述

`RetrievalQA` 是一个高级控制器。当你向它提出问题时，它首先调用检索器获取相关的文档，然后将这些文档连同问题一起传递给内部的文档组合链（如 Stuff 或 Map-Reduce）来生成最终答案。

### 核心属性

| 属性名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `retriever` | `BaseRetriever` | 检索组件，负责从向量库或其他数据源获取相关文档。 |
| `combine_documents_chain` | `BaseCombineDocumentsChain` | 负责将检索到的多个文档组合并生成答案的链。 |
| `input_key` | `str` | 用户查询的键名，默认为 `query`。 |
| `output_key` | `str` | 生成结果的键名，默认为 `result`。 |
| `return_source_documents` | `bool` | 是否在输出中包含检索到的原始文档。 |

### 执行逻辑 (`_call`)

```python
def _call(
    self,
    inputs: dict[str, Any],
    run_manager: CallbackManagerForChainRun | None = None,
) -> dict[str, Any]:
    question = inputs[self.input_key]
    
    # 1. 检索相关文档
    docs = self._get_docs(question, run_manager=run_manager)
    
    # 2. 调用文档组合链生成答案
    answer = self.combine_documents_chain.run(
        input_documents=docs,
        question=question,
        callbacks=run_manager.get_child(),
    )

    # 3. 构造输出
    result = {self.output_key: answer}
    if self.return_source_documents:
        result["source_documents"] = docs
    return result
```

## 实例化方法

### 1. from_chain_type (最常用)
根据指定的类型（如 "stuff", "map_reduce"）自动加载预定义的 QA 链。

```python
qa = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(),
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)
```

### 2. from_llm
手动指定 LLM 和 Prompt。

## 迁移建议 (LCEL)

该类已被弃用，建议使用 `create_retrieval_chain` 工厂函数。它提供了更好的流式支持和更高的灵活性。

### 现代替代示例

```python
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# 1. 定义组合文档的链
prompt = ChatPromptTemplate.from_template("Context: {context}\nQuestion: {input}")
combine_docs_chain = create_stuff_documents_chain(llm, prompt)

# 2. 创建 RAG 链
retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)

# 3. 调用
response = retrieval_chain.invoke({"input": "我的问题"})
```

## 相关类：VectorDBQA

`VectorDBQA` 是一个较旧的实现，它直接绑定了一个 `VectorStore` 而不是抽象的 `BaseRetriever`。现在已基本被 `RetrievalQA` 取代。

## 注意事项

1. **Token 限制**：如果使用 "stuff" 类型且检索到的文档过多，可能会超出 LLM 的上下文窗口。
2. **异步支持**：`RetrievalQA` 支持异步调用 `ainvoke`，前提是底层的检索器和组合链也支持异步。
3. **调试**：设置 `return_source_documents=True` 对调试检索质量非常有用。

