# ChatAgent

`ChatAgent` 是针对对话模型（Chat Models，如 GPT-3.5/4）优化的代理。与基于纯文本的 `ZeroShotAgent` 不同，它使用结构化的消息（System/Human/AI Message）来构建提示词。

> **注意**: 该代理已弃用。建议使用 `create_react_agent` 配合 `ChatPromptTemplate`。

## 核心特性

- **消息结构**: 使用 `SystemMessage` 存储指令和工具定义，使用 `HumanMessage` 存储用户输入。
- **Scratchpad 优化**: 它会自动将中间步骤（Intermediate Steps）格式化为一段特定的文本，并提醒 LLM 这些是之前的尝试。
- **容错处理**: 提供了更强的输出解析能力，以适应对话模型可能产生的格式偏差。

## 提示词模版结构

1. **System Message**:
   - 包含代理的身份说明。
   - 列出可用工具及其参数描述。
   - 规定响应格式（JSON 或特定文本格式）。
2. **Human Message**:
   - 包含用户的输入。
   - 包含 `agent_scratchpad`。

## 关键方法

| 方法 | 说明 |
| :--- | :--- |
| `_construct_scratchpad` | 将历史操作步骤转换为字符串。它会添加一段提示语，告诉模型之前的尝试仅供参考，最终答案必须重新生成。 |
| `create_prompt` | 构建包含 `SystemMessage` 和 `HumanMessage` 的 `ChatPromptTemplate`。 |

## 迁移方案

使用现代的 `create_react_agent` 配合 `langchain_openai` 等模型：

```python
from langchain.agents import create_react_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

model = ChatOpenAI()
prompt = ChatPromptTemplate.from_messages([
    ("system", "Instructions and {tools}"),
    ("human", "{input}"),
    ("ai", "{agent_scratchpad}")
])
agent = create_react_agent(model, tools, prompt)
```
