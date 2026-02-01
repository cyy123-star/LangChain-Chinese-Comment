# libs\langchain\langchain_classic\chains\retrieval.py

`create_retrieval_chain` 是一个工厂函数，用于创建一个完整的检索问答链。它将“检索文档”和“合并文档生成答案”这两个核心步骤无缝连接起来。

## 功能描述

该方法通过 LCEL 构建了一个顺序处理流程：
1.  **检索 (Retrieve)**：利用 `retriever` 根据输入（通常是 `input` 键）获取相关文档。
2.  **增强 (Augment)**：将检索到的文档列表赋值给 `context` 键。
3.  **生成 (Generate)**：调用 `combine_docs_chain`，将原始输入和 `context` 结合，生成最终答案并赋值给 `answer` 键。

## 核心方法：create_retrieval_chain

### 参数说明

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `retriever` | `BaseRetriever` 或 `Runnable` | 用于检索文档的对象。如果是 `BaseRetriever` 子类，则默认从输入字典的 `input` 键获取查询词。 |
| `combine_docs_chain` | `Runnable` | 用于处理检索到的文档并生成最终字符串输出的链（如通过 `create_stuff_documents_chain` 创建的链）。 |

### 执行逻辑 (LCEL 流程)

该函数返回一个组合好的 `Runnable`：

```python
# 1. 确定检索逻辑
if not isinstance(retriever, BaseRetriever):
    retrieval_docs = retriever # 自定义 Runnable
else:
    retrieval_docs = (lambda x: x["input"]) | retriever # 默认从 input 键检索

# 2. 构造顺序链
return (
    RunnablePassthrough.assign(
        # 步骤 A: 检索并存入 context
        context=retrieval_docs.with_config(run_name="retrieve_documents"),
    ).assign(
        # 步骤 B: 生成答案并存入 answer
        answer=combine_docs_chain
    )
).with_config(run_name="retrieval_chain")
```

## 使用示例

```python
from langchain_openai import ChatOpenAI
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate

# 1. 准备模型和检索器
llm = ChatOpenAI(model="gpt-4o")
retriever = ... # 你的检索器 (例如向量数据库检索器)

# 2. 定义合并文档的 Prompt 和链
prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

<context>
{context}
</context>

Question: {input}""")

combine_docs_chain = create_stuff_documents_chain(llm, prompt)

# 3. 创建完整的检索链
retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)

# 4. 调用
response = retrieval_chain.invoke({"input": "What are the core features of LangChain?"})
# 输出将包含: {"input": "...", "context": [Document, ...], "answer": "..."}
```

## 注意事项

1.  **输入输出键名**：该链默认期望输入包含 `input` 键（如果使用标准 `BaseRetriever`），并且输出会自动包含 `context` 和 `answer` 键。
2.  **解耦设计**：它将检索逻辑与生成逻辑完全解耦。你可以更换不同的 `retriever`（如混合检索、多向量检索）或不同的 `combine_docs_chain`（如 Stuff, Refine, Map-Reduce）而无需改变整体结构。
3.  **调试友好**：由于使用了 `RunnablePassthrough.assign`，最终的输出字典会保留所有中间过程数据（如检索到的原始文档），方便开发者验证检索质量。
