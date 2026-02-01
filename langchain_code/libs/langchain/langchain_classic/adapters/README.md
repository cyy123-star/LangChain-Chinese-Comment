# Adapters (适配器)

`adapters` 模块提供了一套工具，用于在 LangChain 和其他流行的 AI SDK（如 OpenAI SDK）之间进行格式转换和接口适配。

## 核心价值

很多开发者习惯于使用特定厂商的 SDK（如 OpenAI 的 Python 库）。`adapters` 允许你保持原有的编码习惯，同时无缝享用 LangChain 提供的功能（如多模型切换、追踪、回调等）。

## OpenAI 适配器 (`openai`)

这是目前最常用的适配器，它提供了与 OpenAI 官方 SDK 几乎一致的调用接口，但在底层将其转换为 LangChain 的 `ChatModel` 调用。

### 核心功能
- **消息格式转换**: 提供 `convert_dict_to_message` 和 `convert_message_to_dict` 等工具，在 OpenAI 的字典格式和 LangChain 的 `Message` 对象之间转换。
- **微调适配**: `convert_messages_for_finetuning` 帮助将对话历史转换为 OpenAI 微调所需的 JSONL 格式。
- **接口仿真**: 提供一个 `chat` 对象，模仿 `openai.ChatCompletion.create` 的行为。

## 使用示例

```python
from langchain.adapters import openai as lc_openai

# 使用类似 OpenAI SDK 的方式调用
response = lc_openai.chat.completions.create(
    messages=[{"role": "user", "content": "Hi"}],
    model="gpt-4",
    temperature=0
)

# 但这实际上是在运行一个 LangChain 链
print(response.choices[0].message.content)
```

## 适用场景

1. **渐进式迁移**: 你的代码库大量使用了 OpenAI SDK，想在不重写所有代码的情况下引入 LangChain 的追踪（LangSmith）。
2. **多模型统一**: 通过适配器，你可以用 OpenAI 的调用方式去调用 Anthropic 或本地 Llama 模型，只需更改底层配置。

## 迁移指南

- **集成分离**: 适配器的具体实现现在已迁移至 `langchain-community`。
- **推荐方案**: 除非有强烈的 SDK 兼容性需求，否则建议直接使用 LangChain 标准的 `ChatModel` 和 LCEL 接口，这能提供更强大的灵活性和更清晰的代码结构。
