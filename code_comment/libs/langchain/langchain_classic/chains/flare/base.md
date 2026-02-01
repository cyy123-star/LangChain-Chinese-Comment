# libs\langchain\langchain_classic\chains\flare\base.py

`FlareChain` (Forward-Looking Active REtrieval) 是一种先进的 RAG 策略。与传统的“检索一次，生成一次”模式不同，FLARE 会在生成过程中动态判断是否需要进行检索，从而解决模型生成过程中出现的由于知识匮乏导致的“幻觉”问题。

## 功能描述

FLARE 算法的核心思想是：在生成回答时，如果模型生成的某个片段置信度较低（Log-probs 较小），则将该片段转化为一个搜索查询，检索相关文档后重新生成该部分。

其工作流程如下：
1.  **初始生成**：模型开始尝试回答问题。
2.  **置信度检测**：检查生成文本中每个 Token 的对数概率（Log-probs）。
3.  **识别低置信度区间**：找出概率低于阈值（`min_prob`）的文本区间。
4.  **生成查询**：利用 `question_generator_chain` 将这些低置信度区间转化为具体的搜索问题。
5.  **主动检索**：在生成的过程中实时调用 `retriever` 获取补充信息。
6.  **迭代优化**：结合检索到的背景知识重新生成内容，直到满足结束条件或达到最大迭代次数（`max_iter`）。

## 核心组件

### 1. `FlareChain`
主控链，协调检索器、问题生成器和响应生成器。

### 2. `QuestionGeneratorChain`
负责将模型感到“不确定”的文本片段转化为有效的检索查询。

## 参数说明

| 参数名 | 类型 | 默认值 | 描述 |
| :--- | :--- | :--- | :--- |
| `retriever` | `BaseRetriever` | **必填** | 用于获取背景知识的检索器。 |
| `min_prob` | `float` | `0.2` | 判定为“低置信度”的概率阈值。低于此值的 Token 会触发检索。 |
| `max_iter` | `int` | `10` | 最大迭代生成次数。 |
| `min_token_gap` | `int` | `5` | 两个低置信度区间之间的最小 Token 间隔，用于合并相邻的模糊点。 |
| `num_pad_tokens` | `int` | `2` | 在低置信度区间前后额外包含的 Token 数量，以提供更多上下文。 |
| `start_with_retrieval` | `bool` | `True` | 是否在开始生成前先进行一次初始检索。 |

## 执行逻辑 (Verbatim Snippet)

识别低置信度区间的核心逻辑如下：

```python
def _low_confidence_spans(
    tokens: Sequence[str],
    log_probs: Sequence[float],
    min_prob: float,
    min_token_gap: int,
    num_pad_tokens: int,
) -> list[str]:
    # 1. 找到所有概率低于 min_prob 的索引
    _low_idx = [
        idx for idx, log_prob in enumerate(log_probs)
        if math.exp(log_prob) < min_prob
    ]
    # 2. 合并相邻或相近的索引形成区间 (Span)
    # ... (合并逻辑)
    # 3. 返回这些区间的文本内容
    return ["".join(tokens[start:end]) for start, end in spans]
```

## 使用示例

```python
from langchain_openai import ChatOpenAI
from langchain_classic.chains import FlareChain
from langchain_community.vectorstores import Chroma

# 注意：FLARE 需要模型返回 logprobs，因此必须配置对应的 LLM
llm = ChatOpenAI(model="gpt-4o", model_kwargs={"logprobs": True})
retriever = Chroma(...).as_retriever()

flare = FlareChain.from_llm(
    llm=llm,
    retriever=retriever,
    max_iter=5
)

response = flare.run("Explain the quantum entanglement in detail.")
```

## 注意事项

1.  **模型要求**：LLM 必须支持返回 `logprobs`（如 OpenAI 的 Chat 模型）。
2.  **性能与成本**：由于可能发生多次迭代检索和生成，FLARE 的延迟和 Token 消耗通常高于标准的 RAG。
3.  **适用场景**：适用于需要高度事实准确性、且问题较为复杂、无法通过单次检索覆盖所有知识点的长文本生成任务。
