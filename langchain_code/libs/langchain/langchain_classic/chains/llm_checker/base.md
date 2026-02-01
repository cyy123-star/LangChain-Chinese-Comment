# LLMCheckerChain (Deprecated)

`LLMCheckerChain` 是一种基于“自验证”机制的问答链。它通过多个步骤对 LLM 生成的初始答案进行拆解、验证和修正，以减少幻觉（Hallucination）。

> **警告**: 该类自 v0.2.13 起已弃用。建议参考 [LangGraph Self-RAG](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_self_rag/) 实现更现代的反思（Reflection）和纠错策略。

## 执行流程

`LLMCheckerChain` 内部封装了一个 `SequentialChain`，包含四个子步骤：

1. **草稿生成 (Draft)**: 生成初始答案。
2. **断言提取 (List Assertions)**: 将初始答案拆解为一系列独立的断言/事实。
3. **断言验证 (Check Assertions)**: 对每个断言进行独立验证，判断其是否准确。
4. **最终修正 (Final Revision)**: 根据验证结果，重写最终答案，剔除错误信息。

```python
# 核心逻辑 (简化)
def _load_chain(llm, prompts):
    return SequentialChain(
        chains=[
            create_draft_answer_chain,    # 1. 生成草稿
            list_assertions_chain,        # 2. 提取事实
            check_assertions_chain,       # 3. 逐一检查
            revised_answer_chain,         # 4. 修正总结
        ],
        input_variables=["question"],
        output_variables=["revised_statement"]
    )
```

## 核心组件

| 参数 | 类型 | 说明 |
| :--- | :--- | :--- |
| `llm` | `BaseLanguageModel` | 执行所有推理和验证步骤的基础模型。 |
| `create_draft_answer_prompt` | `PromptTemplate` | 生成初始草稿的提示词。 |
| `list_assertions_prompt` | `PromptTemplate` | 用于拆解事实的提示词。 |
| `check_assertions_prompt` | `PromptTemplate` | 用于验证事实真伪的提示词。 |
| `revised_answer_prompt` | `PromptTemplate` | 综合验证结果生成最终回答的提示词。 |

## 迁移方案 (LangGraph)

使用 LangGraph 可以构建更强大的循环验证流：
- **条件路由**: 如果验证不通过，可以打回重写。
- **结构化输出**: 使用 `with_structured_output` 确保断言提取的准确性。
- **外部验证**: 可以在验证步骤中集成搜索引擎或数据库查询。
