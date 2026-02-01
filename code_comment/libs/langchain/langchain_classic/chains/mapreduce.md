# MapReduce Chain

`MapReduceChain` 是一个高级 Chain，专门用于处理长文本。它通过将长文本拆分为小块，分别处理（Map），然后再将结果合并（Reduce）来克服 LLM 的上下文窗口限制。

> **注意**：该 Chain 是对 `MapReduceDocumentsChain` 的高层封装，主要针对纯文本输入。

## 核心组件

- **combine_documents_chain**: 负责执行实际 Map-Reduce 逻辑的底层文档合并链。
- **text_splitter**: 用于将输入的长文本切割成文档块的工具。

## 参数说明

| 参数名 | 类型 | 默认值 | 描述 |
| :--- | :--- | :--- | :--- |
| `combine_documents_chain` | `BaseCombineDocumentsChain` | **必填** | 核心合并逻辑。 |
| `text_splitter` | `TextSplitter` | **必填** | 文本拆分器。 |
| `input_key` | `str` | `"input_text"` | 输入长文本的键名。 |
| `output_key` | `str` | `"output_text"` | 输出结果的键名。 |

## 执行逻辑 (Verbatim Snippet)

`MapReduceChain` 的 `_call` 方法展示了其处理流程：

```python
def _call(
    self,
    inputs: dict[str, Any],
    run_manager: CallbackManagerForChainRun | None = None,
) -> dict[str, str]:
    # 1. 提取长文本
    text = inputs[self.input_key]
    
    # 2. 使用 text_splitter 将文本拆分为 Document 对象列表
    docs = self.text_splitter.create_documents([text])
    
    # 3. 调用底层的 combine_documents_chain 处理文档列表
    # 这里会触发 Map (每块处理) 和 Reduce (汇总结果)
    outputs = self.combine_documents_chain.run(
        docs, callbacks=run_manager.get_child() if run_manager else None
    )
    
    # 4. 返回最终汇总结果
    return {self.output_key: outputs}
```

## 迁移指南 (LangGraph)

`MapReduceChain` 已被弃用。对于复杂的 Map-Reduce 任务，LangChain 官方强烈建议使用 **LangGraph**。

### 为什么选择 LangGraph？
1. **并行执行**：LangGraph 可以轻松实现真正的并行 Map 步骤。
2. **状态控制**：可以精细控制每一步的失败重试和中间结果保存。
3. **流式输出**：支持步骤级别的流式反馈。

### 迁移示例
详细的迁移步骤请参考 [官方迁移指南](https://python.langchain.com/docs/versions/migrating_chains/map_reduce_chain/)。

## 注意事项

- **Token 消耗**：Map-Reduce 会产生多次 LLM 调用，可能会消耗大量 Token。
- **拆分策略**：`text_splitter` 的 `chunk_size` 设置非常关键。太小会导致上下文丢失，太大可能导致 Reduce 阶段再次溢出。
- **Reduce 递归**：如果 Map 后的结果仍然太长，底层的 `ReduceDocumentsChain` 会自动执行递归折叠（Collapse）。

