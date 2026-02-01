# MapReduceChain (Deprecated)

`MapReduceChain` 是一种专门处理长文本或大量文档的链。它通过“分而治之”的策略，将输入文本切分成较小的块，分别处理后再汇总。

> **警告**: 该类自 v0.2.13 起已弃用。建议参考 [LangGraph Map-Reduce 指南](https://langchain-ai.github.io/langgraph/how-tos/map-reduce/) 实现更现代、可并行且支持检查点的 Map-Reduce 流程。

## 核心流程

1. **切分 (Split)**: 使用 `text_splitter` 将长文本切分为多个 `Document` 块。
2. **映射 (Map)**: 对每个块独立调用 `llm_chain` 进行处理（例如：对每一段生成摘要）。
3. **汇总 (Reduce)**: 使用 `combine_documents_chain` 将所有块的处理结果合并为最终答案。

```python
# 核心逻辑 (简化)
def _call(self, inputs: dict[str, Any]) -> dict[str, Any]:
    # 1. 切分文本
    docs = self.text_splitter.create_documents([inputs[self.input_key]])
    # 2. 调用 Map-Reduce 组合链
    outputs = self.combine_documents_chain.combine_docs(docs)
    return {self.output_key: outputs[0]}
```

## 核心组件

| 参数 | 类型 | 说明 |
| :--- | :--- | :--- |
| `combine_documents_chain` | `BaseCombineDocumentsChain` | 负责将多个文档合并的链（通常是 `MapReduceDocumentsChain`）。 |
| `text_splitter` | `TextSplitter` | 用于切分输入文本的工具。 |

## 便捷构造方法

可以使用 `from_params` 快速创建一个 Map-Reduce 链：

```python
chain = MapReduceChain.from_params(
    llm=llm,
    prompt=prompt,
    text_splitter=text_splitter
)
```

## 迁移建议

在 LangGraph 中，Map-Reduce 可以通过 `Send` 对象实现动态并行：
- **可扩展性**: 能够处理成千上万个分片而不会超出单个节点的处理能力。
- **状态管理**: 可以在 Map 阶段和 Reduce 阶段之间保存中间状态。
- **错误恢复**: 如果某个分片的处理失败，可以只重试该分片。
