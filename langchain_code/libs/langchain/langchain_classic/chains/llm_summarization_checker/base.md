# LLMSummarizationCheckerChain (Deprecated)

`LLMSummarizationCheckerChain` 专门用于对摘要（Summary）进行自我验证。它通过提取摘要中的事实并检查其真实性，最后生成一份更准确的修正版摘要。

> **警告**: 该类自 v0.2.13 起已弃用。建议使用 [LangGraph](https://langchain-ai.github.io/langgraph/) 实现更灵活的摘要反思流。

## 执行流程

该链内部由一个 `SequentialChain` 驱动，分为四个核心阶段：

1. **事实提取 (Create Facts)**: 从给定的摘要中提取所有独立的断言或事实。
2. **事实核查 (Check Facts)**: 检查提取出的事实是否在原文中有所体现或是否逻辑自洽。
3. **摘要修正 (Revise Summary)**: 根据核查结果，重写摘要以纠正任何错误。
4. **最终确认 (Are All True)**: 确认修正后的摘要是否所有断言均为真。

```python
# 核心逻辑 (简化)
def _load_sequential_chain(llm, prompts):
    return SequentialChain(
        chains=[
            LLMChain(prompt=create_assertions_prompt), # 1. 提炼事实
            LLMChain(prompt=check_assertions_prompt),  # 2. 检查事实
            LLMChain(prompt=revised_summary_prompt),   # 3. 修正摘要
            LLMChain(prompt=are_all_true_prompt),      # 4. 最终确认
        ],
        input_variables=["summary"],
        output_variables=["all_true", "revised_summary"]
    )
```

## 核心组件

| 参数 | 类型 | 说明 |
| :--- | :--- | :--- |
| `sequential_chain` | `SequentialChain` | 封装了上述四个步骤的有序执行链。 |
| `llm` | `BaseLanguageModel` | 执行推理的模型。 |

## 使用场景

- **防止摘要幻觉**: 确保摘要内容完全基于原文，不添加虚假信息。
- **高质量内容审核**: 在发布摘要前进行自动化的事实核对。

## 迁移方案

对于摘要验证，推荐使用 LangGraph 构建包含“原文对比”步骤的节点，并利用结构化输出来获取事实列表。
