# libs\langchain\langchain_classic\chains\llm_math\base.py

`LLMMathChain` 是一个专门用于解决数学问题的链。它不直接让 LLM 计算结果（因为 LLM 经常算错），而是让 LLM 将数学问题转化为 Python 代码（使用 `numexpr` 库），然后由本地 Python 环境执行计算。

## 功能描述

该模块定义了 `LLMMathChain`。其核心逻辑是：
1.  **代码生成**：使用 LLM 将自然语言数学问题（如 "551368 除以 82 是多少"）转化为特定格式的 Python 代码块（包裹在 ```text ``` 中）。
2.  **表达式提取**：从 LLM 的输出中提取出 Python 表达式。
3.  **安全计算**：使用 `numexpr` 库安全地执行提取出的表达式，并返回计算结果。
4.  **格式化输出**：将计算结果包装成 "Answer: [结果]" 的形式。

## 参数说明

### LLMMathChain

| 参数名 | 类型 | 默认值 | 描述 |
| :--- | :--- | :--- | :--- |
| `llm_chain` | `LLMChain` | **必填** | 负责将问题转化为 Python 代码的底层 LLM 链。 |
| `llm` | `BaseLanguageModel` | `None` | [已弃用] 用于初始化的 LLM。建议使用 `from_llm` 方法。 |
| `prompt` | `BasePromptTemplate` | `PROMPT` | [已弃用] 使用的提示词模板。默认模板会引导 LLM 输出 ```text ``` 格式。 |
| `input_key` | `str` | `"question"` | 输入字典中数学问题的键名。 |
| `output_key` | `str` | `"answer"` | 输出字典中答案的键名。 |

## 执行逻辑 (Verbatim Snippet)

### 1. 核心处理流程 (`_process_llm_result`)

```python
def _process_llm_result(
    self,
    llm_output: str,
    run_manager: CallbackManagerForChainRun,
) -> dict[str, str]:
    llm_output = llm_output.strip()
    # 使用正则匹配 ```text ... ``` 中的表达式
    text_match = re.search(r"^```text(.*?)```", llm_output, re.DOTALL)
    if text_match:
        expression = text_match.group(1)
        # 执行计算
        output = self._evaluate_expression(expression)
        answer = "Answer: " + output
    elif llm_output.startswith("Answer:"):
        answer = llm_output
    elif "Answer:" in llm_output:
        answer = "Answer: " + llm_output.split("Answer:")[-1]
    else:
        raise ValueError(f"unknown format from LLM: {llm_output}")
    return {self.output_key: answer}
```

### 2. 表达式计算 (`_evaluate_expression`)

```python
def _evaluate_expression(self, expression: str) -> str:
    import numexpr
    try:
        # 限制全局变量，仅允许数学常数 pi 和 e
        local_dict = {"pi": math.pi, "e": math.e}
        output = str(
            numexpr.evaluate(
                expression.strip(),
                global_dict={},  # 限制全局访问
                local_dict=local_dict,  # 提供常用数学常数
            ),
        )
    except Exception as e:
        raise ValueError(f'LLMMathChain._evaluate("{expression}") raised error: {e}.')
    return re.sub(r"^\[|\]$", "", output) # 去除数组括号
```

## 迁移建议 (LangGraph)

`LLMMathChain` 已被弃用。官方建议使用 LangGraph 结合工具调用（Tool Calling）来实现，这样更安全、更易扩展。

### 现代替代方案示例

```python
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
import numexpr

@tool
def calculator(expression: str) -> str:
    """计算数学表达式。"""
    return str(numexpr.evaluate(expression))

llm = ChatOpenAI(model="gpt-4o-mini")
tools = [calculator]
agent = create_react_agent(llm, tools)

# 调用
response = agent.invoke({"messages": [("user", "551368 除以 82 是多少？")]})
```

## 注意事项

1.  **依赖库**：必须安装 `numexpr` 库 (`pip install numexpr`)，否则会报错。
2.  **安全性**：虽然使用了 `numexpr` 且限制了 `global_dict`，但仍然涉及代码执行。确保 LLM 的提示词不会被恶意利用来执行非法计算。
3.  **计算范围**：`numexpr` 主要针对数值计算，不支持复杂的符号运算（如求导、积分）。对于此类需求，应使用专门的工具（如 `SymPy`）。
4.  **格式敏感**：如果 LLM 没有按预期输出 ```text ``` 块，链会尝试解析 "Answer:" 关键字。

