# Prompts (提示词工程)

`prompts` 模块是 LangChain 提示词工程的核心，提供了定义、管理和动态组合提示词的工具。

## 核心概念

### 1. `PromptTemplate`
最基础的模板类，使用 Python 的 `str.format` 语法进行变量替换。
- **输入**: 包含 `{variable}` 的字符串。
- **输出**: 替换变量后的最终提示词。

### 2. `ChatPromptTemplate`
专为对话模型设计，由一系列消息模板（`SystemMessagePromptTemplate`, `HumanMessagePromptTemplate` 等）组成。

### 3. `FewShotPromptTemplate`
支持少样本（Few-Shot）学习的模板，可以包含示例列表，并支持示例选择器（Example Selector）。

## 关键组件

### Example Selectors (示例选择器)
当示例数量过多时，动态选择最相关的示例：
- `SemanticSimilarityExampleSelector`: 基于向量相似度选择示例。
- `LengthBasedExampleSelector`: 根据长度限制选择示例。
- `MaxMarginalRelevanceExampleSelector`: 在相关性和多样性之间平衡。

## 使用示例

### 基础模板
```python
from langchain_core.prompts import PromptTemplate

template = PromptTemplate.from_template("Tell me a {adjective} joke about {content}.")
prompt = template.format(adjective="funny", content="chickens")
```

### 对话模板
```python
from langchain_core.prompts import ChatPromptTemplate

chat_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI bot. Your name is {name}."),
    ("human", "Hello, how are you?"),
    ("ai", "I'm doing well, thanks!"),
    ("human", "{user_input}"),
])

messages = chat_template.format_messages(name="Bob", user_input="What is your name?")
```

## 提示词组合 (PipelinePrompt)
允许将多个小模板组合成一个大的提示词。

## 迁移与集成
- **LCEL**: 提示词模板现在是 LCEL 链的第一环，支持通过 `|` 与模型连接：`prompt | llm`。
- **LangSmith**: 建议在 LangSmith 中管理复杂的提示词，并使用 `hub.pull` 进行加载。
