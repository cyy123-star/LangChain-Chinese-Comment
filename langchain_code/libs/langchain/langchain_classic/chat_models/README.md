# Chat Models (对话模型)

`chat_models` 模块包含了对各种对话式大语言模型的抽象和实现。与传统的 `llms` 模块不同，对话模型采用“消息进，消息出”的模式，能够更好地处理多轮对话和复杂的角色设定。

## 核心接口

### `BaseChatModel`
所有对话模型的抽象基类。它定义了处理消息列表并返回 `AIMessage` 的标准化接口。

## 统一初始化：`init_chat_model`

LangChain 提供了一个强大的工厂函数 `init_chat_model`，允许开发者通过统一的参数初始化不同供应商的模型：

```python
from langchain.chat_models import init_chat_model

# 初始化 OpenAI 模型
gpt4 = init_chat_model("gpt-4o", model_provider="openai", temperature=0)

# 初始化 Claude 模型
claude = init_chat_model("claude-3-5-sonnet-20240620", model_provider="anthropic")
```

## 核心功能

1. **结构化输出**: 通过 `.with_structured_output(Schema)` 轻松获取 JSON 或 Pydantic 对象。
2. **工具调用 (Tool Calling)**: 现代对话模型原生支持调用外部工具（使用 `.bind_tools(tools)`）。
3. **流式传输**: 支持 `stream` 和 `astream` 接口，提供更佳的用户体验。

## 常见模型实现

| 供应商 | 实现类 | 备注 |
| :--- | :--- | :--- |
| **OpenAI** | `ChatOpenAI` | 行业标准，支持最完整的工具调用和结构化输出。 |
| **Anthropic** | `ChatAnthropic` | 强大的推理能力和超长上下文窗口。 |
| **Google** | `ChatVertexAI` / `ChatGoogleGenerativeAI` | 接入 Gemini 系列模型。 |
| **Local** | `ChatOllama` / `ChatLlamaCpp` | 在本地运行开源对话模型。 |

## 迁移与集成

- **集成分离**: 具体的模型实现现在主要位于 `langchain-openai`, `langchain-anthropic` 等特定集成包中。
- **推荐实践**: 即使在 `langchain_classic` 语境下，也建议通过 `init_chat_model` 或直接从集成包导入，以获得最新的功能支持。
