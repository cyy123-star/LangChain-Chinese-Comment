# Ernie Functions Chains

`ernie_functions` 子模块提供了一系列工具，用于利用文心一言（Ernie）模型的函数调用（Function Calling）能力来生成结构化输出。

## 核心功能

该子模块主要作为 `langchain_community.chains.ernie_functions.base` 的代理，提供以下核心功能：

| 函数 | 说明 |
| :--- | :--- |
| `create_ernie_fn_chain` | 创建一个利用 Ernie 函数调用的 LLMChain。 |
| `create_ernie_fn_runnable` | 创建一个利用 Ernie 函数调用的 LCEL Runnable。 |
| `create_structured_output_chain` | 创建一个返回结构化输出（如 Pydantic 对象）的 Chain。 |
| `convert_to_ernie_function` | 将函数或 Pydantic 模型转换为 Ernie 函数定义。 |

## 弃用说明

此模块中的所有功能均已迁移至 `langchain_community`。

| 弃用属性 | 迁移目标 |
| :--- | :--- |
| `create_ernie_fn_chain` | `langchain_community.chains.ernie_functions.base.create_ernie_fn_chain` |
| `create_structured_output_chain` | `langchain_community.chains.ernie_functions.base.create_structured_output_chain` |

## 迁移指南 (LCEL)

建议直接使用 `langchain_community` 中的实现，或者使用更现代的 `with_structured_output` 方法（如果模型支持）。

### 示例：
```python
from langchain_community.chains.ernie_functions import create_ernie_fn_runnable
from langchain_community.chat_models import ErnieBotChat

llm = ErnieBotChat(...)
runnable = create_ernie_fn_runnable(functions=[...], llm=llm)
```
