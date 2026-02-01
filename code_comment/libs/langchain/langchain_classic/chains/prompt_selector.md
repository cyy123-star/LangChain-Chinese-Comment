# Prompt Selector

`prompt_selector` 模块提供了一套机制，用于根据所使用的语言模型类型（如普通 LLM 或 Chat Model）自动选择最合适的提示词模板。这在构建跨模型兼容的 Chain 时非常有用。

## 核心类

### 1. BasePromptSelector
所有提示词选择器的抽象基类，定义了 `get_prompt(llm)` 接口。

### 2. ConditionalPromptSelector
最常用的实现类，它根据一组条件（Conditionals）来决定返回哪个 Prompt。

## 参数说明 (ConditionalPromptSelector)

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `default_prompt` | `BasePromptTemplate` | 如果没有任何条件匹配，则使用的默认提示词。 |
| `conditionals` | `list[tuple[Callable, BasePromptTemplate]]` | 一个列表，包含（判断函数, 提示词模板）元组。 |

## 执行逻辑 (Verbatim Snippet)

```python
def get_prompt(self, llm: BaseLanguageModel) -> BasePromptTemplate:
    """为给定的语言模型获取默认提示词。"""
    for condition, prompt in self.conditionals:
        # 如果满足条件（如 is_chat_model），则返回对应的 Prompt
        if condition(llm):
            return prompt
    # 否则返回默认值
    return self.default_prompt
```

## 辅助函数

- `is_llm(llm)`: 检查模型是否继承自 `BaseLLM`。
- `is_chat_model(llm)`: 检查模型是否继承自 `BaseChatModel`。

## 使用示例

```python
from langchain_classic.chains.prompt_selector import ConditionalPromptSelector, is_chat_model
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

# 定义不同的模板
llm_prompt = PromptTemplate.from_template("Summarize: {text}")
chat_prompt = ChatPromptTemplate.from_template("You are a helpful assistant. Summarize: {text}")

# 创建选择器
selector = ConditionalPromptSelector(
    default_prompt=llm_prompt,
    conditionals=[(is_chat_model, chat_prompt)]
)

# 使用
current_prompt = selector.get_prompt(some_llm)
```

## 迁移指南 (LCEL)

在 LCEL 中，推荐使用 `RunnableBranch` 或简单的 Python 逻辑来替代 `PromptSelector`，这使得逻辑更加显式：

```python
from langchain_core.runnables import RunnableBranch
from langchain_openai import ChatOpenAI, OpenAI

# 现代 LCEL 方式
chain = (
    RunnableBranch(
        (lambda x: isinstance(x["llm"], ChatOpenAI), chat_prompt),
        llm_prompt
    )
    | llm
)
```

