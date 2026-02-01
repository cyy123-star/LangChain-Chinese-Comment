# Smith (LangSmith 集成)

`smith` 模块是 LangChain 与 **LangSmith** 平台的集成层。它提供了便捷的工具，用于将应用运行数据同步到 LangSmith，并利用平台的能力进行调试、评估和监控。

## 核心职责

1. **评估器集成**: 允许在本地运行 LangSmith 兼容的评估逻辑。
2. **测试运行器**: 提供工具（如 `run_on_dataset`）来在 LangSmith 数据集上批量运行 Chain 或 Agent。
3. **进度追踪**: 在批量运行测试时提供进度条和实时反馈。

## 关键功能

- **`RunEvalConfig`**: 配置评估参数，如使用哪个模型作为评判者、评估哪些指标。
- **数据集加载**: 方便地从 LangSmith 平台下载测试数据集。

## 使用示例

```python
from langchain.smith import RunEvalConfig, run_on_dataset
from langsmith import Client

client = Client()
eval_config = RunEvalConfig(
    evaluators=["qa"],
    prediction_key="output"
)

# 在数据集上运行评估
# run_on_dataset(
#     client=client,
#     dataset_name="my-test-set",
#     llm_or_chain_factory=my_chain,
#     evaluation=eval_config
# )
```

## 注意事项

- **环境变量**: 使用本模块前，通常需要设置 `LANGCHAIN_TRACING_V2=true` 和 `LANGCHAIN_API_KEY`。
- **生产级监控**: 虽然 `evaluation` 模块可以进行本地评估，但 `smith` 模块结合 LangSmith 平台提供了更强大的持久化和可视化能力。
