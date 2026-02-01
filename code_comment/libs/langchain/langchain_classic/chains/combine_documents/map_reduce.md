# libs\langchain\langchain_classic\chains\combine_documents\map_reduce.py

此文档提供了 `libs\langchain\langchain_classic\chains\combine_documents\map_reduce.py` 文件的详细中文注释，该文件实现了经典的 Map-Reduce 文档合并策略。

## 文件概述

Map-Reduce 是一种用于处理大规模文档集的策略。与简单的“填充”（Stuffing）不同，它通过两个阶段来解决上下文窗口限制问题：
1. **Map（映射）阶段**：对每个文档块（Document）独立应用一个 LLM 链（例如为每个块生成摘要）。由于每个文档是独立处理的，这一步可以并行执行。
2. **Reduce（归约）阶段**：将 Map 阶段产生的所有中间结果合并为一个最终结果。如果中间结果仍然太多，可以递归地进行归约。

**核心优势**：
- **突破长度限制**：可以处理任意数量和长度的文档。
- **并行处理**：Map 阶段可以显著提高处理速度。

**核心局限**：
- **多次调用**：需要多次调用 LLM，增加了成本和延迟。
- **上下文丢失**：在 Map 阶段，模型无法看到其他文档块的信息，可能丢失跨块的上下文。

---

## 核心类：`MapReduceDocumentsChain`

该类负责协调 Map 阶段和 Reduce 阶段的执行。

### 1. 关键属性

| 属性 | 类型 | 描述 |
| :--- | :--- | :--- |
| `llm_chain` | `LLMChain` | 用于 Map 阶段的链，应用于每个独立文档。 |
| `reduce_documents_chain` | `BaseCombineDocumentsChain` | 用于 Reduce 阶段的链，通常是 `ReduceDocumentsChain` 或 `StuffDocumentsChain`。 |
| `document_variable_name` | `str` | `llm_chain` 中用于接收文档内容的变量名。 |
| `return_intermediate_steps`| `bool` | 是否在最终输出中包含 Map 阶段生成的中间结果。 |

### 2. 执行流程

- **同步执行 (`combine_docs`)**:
    1. 使用 `llm_chain.apply` 并行地对所有文档执行 Map 操作。
    2. 将 Map 结果封装为新的 `Document` 对象。
    3. 调用 `reduce_documents_chain.combine_docs` 进行结果合并。
- **异步执行 (`acombine_docs`)**: 使用 `llm_chain.aapply` 实现异步并行的 Map 操作。

---

## 使用示例

```python
from langchain_classic.chains import (
    StuffDocumentsChain,
    LLMChain,
    ReduceDocumentsChain,
    MapReduceDocumentsChain,
)
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI

# 1. Map 阶段：为每个文档生成摘要
map_template = "请总结以下内容：\n\n{context}"
map_prompt = PromptTemplate.from_template(map_template)
llm = OpenAI()
map_chain = LLMChain(llm=llm, prompt=map_prompt)

# 2. Reduce 阶段：合并摘要
reduce_template = "请根据以下中间摘要生成最终总结：\n\n{context}"
reduce_prompt = PromptTemplate.from_template(reduce_template)
reduce_llm_chain = LLMChain(llm=llm, prompt=reduce_prompt)

# 2a. 使用 Stuff 策略作为归约的基础
combine_chain = StuffDocumentsChain(
    llm_chain=reduce_llm_chain,
    document_variable_name="context"
)

# 2b. 定义 Reduce 链（可以包含折叠逻辑）
reduce_chain = ReduceDocumentsChain(combine_documents_chain=combine_chain)

# 3. 创建最终的 Map-Reduce 链
map_reduce_chain = MapReduceDocumentsChain(
    llm_chain=map_chain,
    reduce_documents_chain=reduce_chain,
    document_variable_name="context"
)
```

---

## 注意事项

1. **已弃用**：该类已弃用，官方建议参考[迁移指南](https://python.langchain.com/docs/versions/migrating_chains/map_reduce_chain/)使用 LCEL 构建更灵活的 Map-Reduce 流程。
2. **中间步骤返回**：如果你需要调试或展示 Map 阶段生成的摘要，请设置 `return_intermediate_steps=True`。
3. **元数据保留**：Map 阶段产生的新文档会尽量保留原始文档的元数据（Metadata），这对于后续追溯来源非常有用。
4. **递归合并**：如果使用 `ReduceDocumentsChain` 作为归约步骤，它会自动根据 Token 限制决定是否需要多轮“折叠”（Collapse）文档。
