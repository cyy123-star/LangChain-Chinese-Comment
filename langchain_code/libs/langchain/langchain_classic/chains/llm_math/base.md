# LLMMathChain (Deprecated)

`LLMMathChain` 用于解决复杂的数学问题。它不直接让 LLM 计算结果（因为 LLM 容易算错），而是让 LLM 生成一段 Python 代码（通常使用 `numexpr` 库），然后在本地安全地执行该代码并返回计算结果。

> **警告**: 该类自 v0.2.13 起已弃用，建议使用 [LangGraph](https://langchain-ai.github.io/langgraph/) 或带有工具调用（Tool Calling）功能的智能体实现。

## 核心组件

| 参数 | 类型 | 说明 |
| :--- | :--- | :--- |
| `llm_chain` | `LLMChain` | 用于将自然语言问题转换为数学表达式的链。 |
| `prompt` | `BasePromptTemplate` | 引导 LLM 输出特定格式（如 ```text 5 + 5 ```）代码的提示词模板。 |

## 执行逻辑

1. **生成表达式**: LLM 根据问题生成 Python 数学表达式。
2. **提取代码**: 使用正则匹配提取 `llm_output` 中的代码块。
3. **安全计算**: 使用 `numexpr.evaluate` 在受限环境下执行计算。
4. **格式化输出**: 将计算结果拼接成最终回答。

```python
# 核心逻辑 (简化)
def _process_llm_result(self, llm_output: str) -> dict[str, str]:
    # 1. 正则提取代码块
    text_match = re.search(r"^```text(.*?)```", llm_output, re.DOTALL)
    if text_match:
        expression = text_match.group(1)
        # 2. 调用 numexpr 计算
        output = self._evaluate_expression(expression)
        return {self.output_key: "Answer: " + output}
```

## 依赖要求

使用该链需要安装 `numexpr` 库：
```bash
pip install numexpr
```

## 迁移方案 (LangGraph)

现代做法是定义一个 `calculator` 工具，并使用支持工具调用的模型。

```python
@tool
def calculator(expression: str) -> str:
    """使用 Python 的 numexpr 库计算数学表达式。"""
    local_dict = {"pi": math.pi, "e": math.e}
    return str(numexpr.evaluate(expression.strip(), local_dict=local_dict))

# 然后将该工具绑定到模型并构建 ReAct 智能体
model_with_tools = model.bind_tools([calculator])
```

这种方式的优势在于：
- **可靠性**: 利用模型原生的工具调用能力，不再依赖不稳定的正则匹配。
- **灵活性**: 智能体可以在一个对话中多次调用计算器，或与其他工具结合使用。
