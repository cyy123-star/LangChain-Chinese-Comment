# 快速入门教程

本教程将引导你快速上手 LangChain，并了解如何利用本项目的中文注释深入学习。

## 1. 核心概念：Runnable
LangChain 的核心是 `Runnable` 接口。几乎所有组件都实现了这个接口。
- **阅读建议**: 先查看 [Runnable 基础文档](../code_comment/libs/core/langchain_core/runnables/base.md)。

## 2. 构建第一个链 (LCEL)
LCEL 是 LangChain 的灵魂。它允许你像搭积木一样组合组件。

### 示例代码
推荐使用 `init_chat_model` 工厂函数来快速切换不同的模型提供商：

```python
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. 准备组件
# 使用 init_chat_model 可以轻松切换模型，如 "gpt-4o", "claude-3-5-sonnet-20240620" 等
model = init_chat_model("gpt-3.5-turbo", temperature=0)
prompt = ChatPromptTemplate.from_template("告诉我一个关于 {topic} 的冷知识")
output_parser = StrOutputParser()

# 2. 组合成链
# 逻辑：输入 -> Prompt -> LLM -> 提取文本
chain = prompt | model | output_parser

# 3. 运行
response = chain.invoke({"topic": "南极洲"})
print(response)
```

## 3. 深入源码
当你对某个组件（如 `ChatPromptTemplate`）的内部实现感到好奇时：
1. 在 `langchain_code/` 中找到对应的 `.py` 文件。
2. 在 `code_comment/` 对应的路径下找到 `.md` 文件，查看详细的中文功能描述、参数解释和注意事项。

## 4. 下一步学习
- **Prompt 工程**: 学习如何使用 `FewShotPromptTemplate`。
- **RAG (检索增强生成)**: 学习 `VectorStores` 和 `Retrievers`。
- **Agents**: 学习如何让 LLM 自主决定调用哪些工具。
