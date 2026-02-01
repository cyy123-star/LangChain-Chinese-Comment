# Elasticsearch Database Chain

`ElasticsearchDatabaseChain` 是一个经典的 Chain，用于根据自然语言问题生成 Elasticsearch DSL 查询，并根据查询结果生成答案。

## 核心组件

| 组件 | 类型 | 说明 |
| :--- | :--- | :--- |
| `query_chain` | `Runnable` | 用于根据输入问题生成 Elasticsearch DSL 查询的链。 |
| `answer_chain` | `Runnable` | 用于根据查询结果和原始问题生成最终自然语言回答的链。 |
| `database` | `Elasticsearch` | Elasticsearch 客户端实例。 |

## 参数表格

| 参数 | 类型 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- |
| `top_k` | `int` | `10` | 检索时返回的文档数量。 |
| `ignore_indices` | `list[str] \| None` | `None` | 要忽略的索引列表。 |
| `include_indices` | `list[str] \| None` | `None` | 要包含的索引列表。 |
| `input_key` | `str` | `"question"` | 输入字典中问题的键名。 |
| `output_key` | `str` | `"result"` | 输出字典中答案的键名。 |
| `sample_documents_in_index_info` | `int` | `3` | 在索引信息中包含的示例文档数量。 |
| `return_intermediate_steps` | `bool` | `False` | 是否返回中间步骤（如生成的 DSL）。 |

## 执行逻辑 (Verbatim Snippet)

以下是 `ElasticsearchDatabaseChain._call` 的核心执行逻辑：

```python
def _call(
    self,
    inputs: dict[str, Any],
    run_manager: CallbackManagerForChainRun | None = None,
) -> dict[str, Any]:
    _run_manager = run_manager or CallbackManagerForChainRun.get_noop_manager()
    input_text = f"{inputs[self.input_key]}\nESQuery:"
    
    # 1. 获取索引信息
    indices = self._list_indices()
    indices_info = self._get_indices_infos(indices)
    
    # 2. 生成 DSL 查询
    query_inputs = {
        "input": input_text,
        "top_k": str(self.top_k),
        "indices_info": indices_info,
        "stop": ["\nESResult:"],
    }
    es_cmd = self.query_chain.invoke(query_inputs)
    
    # 3. 执行搜索
    result = self._search(indices=indices, query=es_cmd)
    
    # 4. 生成回答
    answer_inputs = {"data": result, "input": input_text}
    final_result = self.answer_chain.invoke(answer_inputs)
    
    return {self.output_key: final_result}
```

## 迁移指南 (LCEL)

`ElasticsearchDatabaseChain` 已被弃用。建议使用 LCEL 构建更灵活的查询流程，或者使用 `langchain-elasticsearch` 包中的现代工具。

### 迁移建议：
1. 使用 `langchain-elasticsearch` 包提供的 `ElasticsearchRetriever`。
2. 使用 LCEL 组合 Prompt 和 Model 来生成 DSL，并使用 Elasticsearch 客户端执行。
