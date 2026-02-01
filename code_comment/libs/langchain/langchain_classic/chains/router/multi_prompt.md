# libs\langchain\langchain_classic\chains\router\multi_prompt.py

## 文件概述

`multi_prompt.py` 定义了 `MultiPromptChain`，这是一种非常实用的路由链实现。它允许系统根据用户输入的语义，从多个预定义的提示词模板中选择最合适的一个进行回答。例如，一个助手可以根据问题属于“数学”、“历史”还是“编程”来切换不同的专业提示词。

## 核心类：MultiPromptChain (已弃用)

### 功能描述

`MultiPromptChain` 继承自 `MultiRouteChain`。它自动构建一个 `LLMRouterChain` 作为决策器，并为每个预定义的提示词模板创建一个 `LLMChain` 作为目标链。

### 核心构造方法：from_prompts

这是最常用的实例化方法，它简化了路由链的创建过程。

#### 参数说明

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `llm` | `BaseLanguageModel` | 用于路由决策和最终回答的语言模型。 |
| `prompt_infos` | `list[dict]` | 包含提示词信息的列表。每个 dict 应包含 `name`, `description`, `prompt_template`。 |
| `default_chain` | `Chain` | [可选] 默认链。如果不提供，默认创建一个 `ConversationChain`。 |

#### 内部逻辑

1. **构建路由模板**：利用 `MULTI_PROMPT_ROUTER_TEMPLATE`，将所有 `prompt_infos` 中的名称和描述嵌入到路由提示词中。
2. **初始化路由器**：创建一个 `LLMRouterChain`，其 `output_parser` 为 `RouterOutputParser`。
3. **创建目标链**：遍历 `prompt_infos`，为每个模板创建一个 `LLMChain`。
4. **封装**：返回一个配置好的 `MultiPromptChain` 实例。

## 使用示例

```python
from langchain_openai import OpenAI
from langchain_classic.chains.router import MultiPromptChain

llm = OpenAI()

prompt_infos = [
    {
        "name": "math",
        "description": "适用于回答数学问题",
        "prompt_template": "你是一个数学老师，请回答：{input}"
    },
    {
        "name": "physics",
        "description": "适用于回答物理问题",
        "prompt_template": "你是一个物理学家，请回答：{input}"
    }
]

chain = MultiPromptChain.from_prompts(llm, prompt_infos, verbose=True)

# 自动路由到 math 模板
res = chain.invoke({"input": "什么是勾股定理？"})
```

## 注意事项

1. **描述的重要性**：`description` 字段非常关键，因为它直接影响 LLM 路由的准确性。描述应清晰、互斥。
2. **输入键限制**：`MultiPromptChain` 默认期望输入键为 `input`。
3. **现代替代**：由于该类已弃用，建议使用 `LangGraph` 或 LCEL 配合结构化输出实现更稳健的路由。

