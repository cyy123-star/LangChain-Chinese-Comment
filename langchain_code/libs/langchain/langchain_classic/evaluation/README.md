# Evaluation (评估系统)

`evaluation` 模块提供了一套用于衡量 LLM 应用输出质量的工具。它涵盖了从简单的字符串匹配到复杂的基于 LLM 的评估逻辑。

## 评估维度

### 1. 字符串评估 (String Evaluators)
- **Exact Match**: 完全匹配参考答案。
- **Regex Match**: 通过正则表达式验证输出格式。
- **String Distance**: 计算编辑距离（Levenshtein）或相似度。

### 2. 问答评估 (QA Evaluators)
- **QA**: 评估模型回答是否与参考答案在语义上一致（通常使用 LLM 作为评判者）。
- **Context QA**: 结合提供的上下文，评估回答的准确性。

### 3. 轨迹评估 (Trajectory Evaluators)
- **Agent Trajectory**: 评估 Agent 在解决问题过程中的步骤是否合理、工具调用是否正确。

### 4. 标准/准则评估 (Criteria Evaluators)
根据预定义的准则（如：是否有害、是否简洁、是否幽默）对输出进行打分。

## 核心组件

- `load_evaluator`: 便捷函数，用于根据名称加载预定义的评估器。
- `EvaluatorType`: 枚举类，定义了所有支持的评估器类型。

## 使用示例

```python
from langchain.evaluation import load_evaluator

evaluator = load_evaluator("labeled_qa")

# 评估
result = evaluator.evaluate_strings(
    input="Who is the CEO of OpenAI?",
    prediction="Sam Altman is the CEO.",
    reference="Sam Altman"
)

print(result["score"]) # 返回 0 到 1 之间的分数
```

## 现代方案：LangSmith

虽然本地评估器在自动化测试中很有用，但对于复杂的生产级应用，推荐使用 **LangSmith**：
- **可视化**: 直接在界面上对比不同版本的输出。
- **数据集管理**: 轻松管理海量的测试用例。
- **协同评估**: 支持人工标注和多模型交叉评估。
