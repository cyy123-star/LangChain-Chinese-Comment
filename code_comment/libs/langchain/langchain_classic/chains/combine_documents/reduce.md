# libs\langchain\langchain_classic\chains\combine_documents\reduce.py

此文档提供了 `libs\langchain\langchain_classic\chains\combine_documents\reduce.py` 文件的详细中文注释，该文件实现了通过递归缩减（Reducing）来合并大量文档的逻辑。

## 文件概述

`ReduceDocumentsChain` 是 Map-Reduce 策略中的核心组件，专门负责“归约”（Reduce）步骤。当需要处理的文档数量过多，无法一次性塞入 LLM 的上下文窗口时，该类通过递归的方式将文档分批合并，直到最终结果能适应窗口大小。

**核心逻辑**：
- **递归折叠**：如果文档总长度超过 `token_max`，则将其拆分为多个子集，分别进行“折叠”（Collapse）。
- **元数据合并**：在合并文档内容的同时，自动合并各文档的元数据。

---

## 核心类：`ReduceDocumentsChain`

### 1. 关键属性

| 属性 | 类型 | 描述 |
| :--- | :--- | :--- |
| `combine_documents_chain` | `BaseCombineDocumentsChain` | 最终执行合并的链（通常是 `StuffDocumentsChain`）。 |
| `collapse_documents_chain` | `BaseCombineDocumentsChain \| None` | 可选。用于中间递归步骤的“折叠”链。如果为 `None`，则使用 `combine_documents_chain`。 |
| `token_max` | `int` | 单次合并操作允许的最大 Token 数，默认为 3000。 |
| `collapse_max_retries` | `int \| None` | 最大折叠重试次数。防止因无限递归导致的死循环。 |

### 2. 核心方法

- **`combine_docs(docs, ...)`**: 递归地缩减文档列表。
    1. 检查当前所有文档的总 Token 数。
    2. 如果超过 `token_max`，调用 `_collapse` 逻辑进行一轮或多轮压缩。
    3. 最后调用 `combine_documents_chain` 生成最终字符串。

---

## 辅助函数

### 1. `split_list_of_docs`
根据 `token_max` 限制，将一个长文档列表拆分为多个子列表。每个子列表的总 Token 数都保证在限制范围内。

### 2. `collapse_docs`
执行折叠操作的关键函数。它不仅合并文本内容，还会处理元数据（Metadata）的合并逻辑：
- 如果元数据键重复，其值将以 `', '` 分隔并连接。

---

## 使用示例

```python
from langchain_classic.chains import StuffDocumentsChain, LLMChain, ReduceDocumentsChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI

# 1. 定义基础的合并逻辑（Stuff 策略）
prompt = PromptTemplate.from_template("请合并以下内容：{context}")
llm_chain = LLMChain(llm=OpenAI(), prompt=prompt)
combine_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="context")

# 2. 创建 Reduce 链，设置 Token 阈值为 4000
reduce_chain = ReduceDocumentsChain(
    combine_documents_chain=combine_chain,
    token_max=4000
)

# 3. 当传入 100 个文档时，reduce_chain 会自动分批折叠，直到最终合并
```

---

## 注意事项

1. **已弃用**：此类已弃用，建议迁移到 LCEL 实现的 Map-Reduce 模式。
2. **Token 计算**：该类依赖于 `combine_documents_chain` 提供的 `prompt_length` 方法来计算 Token。请确保底层链正确实现了此方法。
3. **元数据膨胀**：由于折叠操作会合并所有文档的元数据，如果文档极多，最终生成的 `Document` 对象的元数据字典可能会非常庞大。
4. **单文档超长**：如果单个文档本身的 Token 数就超过了 `token_max`，该链会抛出 `ValueError`，因为无法通过分批策略解决单文档超长问题。
