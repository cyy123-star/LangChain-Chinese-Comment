# libs\langchain\langchain_classic\chains\combine_documents\refine.py

此文档提供了 `libs\langchain\langchain_classic\chains\combine_documents\refine.py` 文件的详细中文注释，该文件实现了通过迭代改进（Refining）来合并文档的策略。

## 文件概述

“改进”（Refine）策略是一种通过循环迭代来处理文档的方法。它不是一次性处理所有文档，也不是并行处理，而是按顺序一个接一个地处理文档：
1. **初始阶段**：对第一个文档运行一个初始链，得到初始响应。
2. **改进阶段**：对于后续的每个文档，将该文档内容与**上一步的响应**一起传递给改进链。改进链的目标是根据新文档的信息来更新或优化之前的响应。

**核心优势**：
- **逐步演进**：响应会随着看到的文档增多而变得越来越精确。
- **上下文关联**：每一轮改进都能参考之前的结论。

**核心局限**：
- **无法并行**：必须串行执行，因此处理速度较慢。
- **潜在遗忘**：如果文档很多，模型可能会在后期迭代中逐渐丢失早期文档的细节（受限于 LLM 的记忆和提示词结构）。

---

## 核心类：`RefineDocumentsChain`

### 1. 关键属性

| 属性 | 类型 | 描述 |
| :--- | :--- | :--- |
| `initial_llm_chain` | `LLMChain` | 用于处理第一个文档的链。 |
| `refine_llm_chain` | `LLMChain` | 用于后续改进步骤的链。 |
| `document_variable_name`| `str` | 提示词中存放当前文档内容的变量名。 |
| `initial_response_name` | `str` | 改进链中存放上一步响应结果的变量名。 |
| `return_intermediate_steps`| `bool` | 是否返回每一轮改进的中间结果。 |

### 2. 执行流程

- **`combine_docs`**:
    1. **第一步**：取第一个文档，构造输入并调用 `initial_llm_chain.predict`。
    2. **迭代步**：遍历从第二个开始的所有文档。
    3. 在每一轮中，将“当前文档”和“上一轮答案”填入 `refine_llm_chain` 并执行。
    4. 最终返回最后一轮的答案。

---

## 使用示例

```python
from langchain_classic.chains import RefineDocumentsChain, LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI

# 1. 定义初始提示词（只处理一个文档）
initial_template = "请基于以下内容生成初始总结：\n\n{context}"
initial_prompt = PromptTemplate.from_template(initial_template)
llm = OpenAI()
initial_chain = LLMChain(llm=llm, prompt=initial_prompt)

# 2. 定义改进提示词（处理一个文档 + 上一步响应）
refine_template = (
    "已有的总结如下：{prev_response}\n"
    "现在请结合以下新内容改进上述总结：\n\n{context}"
)
refine_prompt = PromptTemplate.from_template(refine_template)
refine_chain = LLMChain(llm=llm, prompt=refine_prompt)

# 3. 创建 Refine 链
chain = RefineDocumentsChain(
    initial_llm_chain=initial_chain,
    refine_llm_chain=refine_chain,
    document_variable_name="context",
    initial_response_name="prev_response"
)
```

---

## 注意事项

1. **已弃用**：此类已弃用，建议迁移到 LCEL 实现的 Refine 模式。
2. **提示词设计**：改进提示词的设计非常关键。它必须明确告知模型如何利用新信息去“更新”而不是简单的“追加”。
3. **顺序依赖**：由于是串行处理，文档的输入顺序可能会影响最终结果。
4. **性能监控**：如果文档集很大，该链会消耗大量的 LLM 调用次数。建议结合 `return_intermediate_steps=True` 来监控每一步的改进质量。
