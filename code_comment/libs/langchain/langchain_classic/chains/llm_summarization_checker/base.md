# LLM Summarization Checker Chain

`LLMSummarizationCheckerChain` 是一个专门用于摘要验证的链。它通过迭代核实摘要中的事实断言，确保摘要的准确性和客观性。

## 核心组件

该链内部由一个 `SequentialChain` 驱动，并包含一个 `while` 循环进行多次迭代校验（默认为 2 次）：

1.  **Create Assertions (创建断言)**: 从摘要中提取事实断言。
2.  **Check Assertions (核实断言)**: 核实提取的断言是否真实。
3.  **Revise Summary (修正摘要)**: 根据核实结果重新编写摘要。
4.  **Are All True (是否全部真实)**: 判断当前摘要中的断言是否已全部为真。

## 参数表

| 参数 | 类型 | 说明 |
| :--- | :--- | :--- |
| `llm` | `BaseLanguageModel` | 用于所有子步骤的语言模型。 |
| `max_checks` | `int` | 最大检查次数（循环次数），默认为 `2`。 |
| `input_key` | `str` | 输入键名，默认为 `"query"`。 |
| `output_key` | `str` | 输出键名，默认为 `"result"`。 |
| `create_assertions_prompt` | `PromptTemplate` | 创建断言的提示词。 |
| `check_assertions_prompt` | `PromptTemplate` | 核实断言的提示词。 |
| `revised_summary_prompt` | `PromptTemplate` | 修正摘要的提示词。 |
| `are_all_true_prompt` | `PromptTemplate` | 判断是否全部真实的提示词。 |

## 执行逻辑 (Verbatim Snippet)

### 循环验证逻辑
```python
def _call(
    self,
    inputs: dict[str, Any],
    run_manager: CallbackManagerForChainRun | None = None,
) -> dict[str, str]:
    _run_manager = run_manager or CallbackManagerForChainRun.get_noop_manager()
    all_true = False
    count = 0
    output = None
    chain_input = inputs[self.input_key]
    
    # 核心迭代循环
    while not all_true and count < self.max_checks:
        # 执行内部顺序链
        output = self.sequential_chain(
            {"summary": chain_input},
            callbacks=_run_manager.get_child(),
        )
        count += 1

        # 如果模型认为全部真实，则跳出循环
        if output["all_true"].strip() == "True":
            break

        # 否则，将修正后的摘要作为下一次迭代的输入
        chain_input = output["revised_summary"]

    return {self.output_key: output["revised_summary"].strip()}
```

## 迁移指南 (LangGraph)

与 `LLMCheckerChain` 类似，官方推荐使用 **LangGraph** 来实现此类具有循环迭代逻辑的任务。LangGraph 的状态机模型非常适合处理“验证 -> 失败 -> 修正 -> 再次验证”的循环流。

你可以参考 [LangGraph Self-RAG 教程](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_self_rag/)，只需将 RAG 的生成逻辑替换为摘要修正逻辑即可。
