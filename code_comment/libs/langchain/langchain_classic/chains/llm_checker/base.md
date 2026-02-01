# LLM Checker Chain

`LLMCheckerChain` 是一个用于带有自我验证功能的问答链。它通过多个步骤来验证回答的准确性，从而减少幻觉（Hallucinations）。

## 核心组件

该链内部由一个 `SequentialChain` 驱动，包含四个主要的步骤：

1.  **Draft Answer (草稿)**: 生成对问题的初始回答。
2.  **List Assertions (断言列表)**: 从草稿中提取出需要验证的事实断言。
3.  **Check Assertions (验证断言)**: 对提取的断言逐一进行核实。
4.  **Revised Answer (修正回答)**: 根据核实后的结果，生成最终的修正回答。

## 参数表

| 参数 | 类型 | 说明 |
| :--- | :--- | :--- |
| `llm` | `BaseLanguageModel` | 用于所有子步骤的语言模型。 |
| `input_key` | `str` | 输入键名，默认为 `"query"`。 |
| `output_key` | `str` | 输出键名，默认为 `"result"`。 |
| `create_draft_answer_prompt` | `PromptTemplate` | 生成草稿的提示词模板。 |
| `list_assertions_prompt` | `PromptTemplate` | 提取断言的提示词模板。 |
| `check_assertions_prompt` | `PromptTemplate` | 验证断言的提示词模板。 |
| `revised_answer_prompt` | `PromptTemplate` | 生成修正回答的提示词模板。 |

## 执行逻辑 (Verbatim Snippet)

### 顺序链加载逻辑
```python
def _load_question_to_checked_assertions_chain(
    llm: BaseLanguageModel,
    ...
) -> SequentialChain:
    # 步骤 1: 生成草稿
    create_draft_answer_chain = LLMChain(llm=llm, prompt=..., output_key="statement")
    # 步骤 2: 提取断言
    list_assertions_chain = LLMChain(llm=llm, prompt=..., output_key="assertions")
    # 步骤 3: 验证断言
    check_assertions_chain = LLMChain(llm=llm, prompt=..., output_key="checked_assertions")
    # 步骤 4: 生成修正后的回答
    revised_answer_chain = LLMChain(llm=llm, prompt=..., output_key="revised_statement")
    
    chains = [
        create_draft_answer_chain,
        list_assertions_chain,
        check_assertions_chain,
        revised_answer_chain,
    ]
    return SequentialChain(
        chains=chains,
        input_variables=["question"],
        output_variables=["revised_statement"],
        verbose=True,
    )
```

### 调用入口
```python
def _call(
    self,
    inputs: dict[str, Any],
    run_manager: CallbackManagerForChainRun | None = None,
) -> dict[str, str]:
    _run_manager = run_manager or CallbackManagerForChainRun.get_noop_manager()
    question = inputs[self.input_key]

    # 调用内部的 SequentialChain
    output = self.question_to_checked_assertions_chain(
        {"question": question},
        callbacks=_run_manager.get_child(),
    )
    # 返回最终修正后的陈述
    return {self.output_key: output["revised_statement"]}
```

## 迁移指南 (LangGraph)

官方推荐使用 **LangGraph** 来实现更灵活的自我反思（Self-Reflection）和纠错（Corrective）策略。`LLMCheckerChain` 的固定流程较为死板，而 LangGraph 允许根据验证结果动态决定是否需要重新生成或修正。

你可以参考 [LangGraph Self-RAG 教程](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_self_rag/) 来实现类似的逻辑。
