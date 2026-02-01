# LLMs (大语言模型 - 文本补全)

`llms` 模块包含了对传统大语言模型（即“文本进，文本出”的补全模型）的抽象和实现。与 `chat_models` 不同，这些模型不区分角色（System, Human, AI），而是处理单一的提示词字符串。

## 核心抽象

### 1. `LLM`
所有传统 LLM 的基类。开发者只需实现 `_call` 方法，接收一个提示词并返回生成的字符串。

### 2. `BaseLLM`
更底层的基类，支持批处理（Batching）和生成多个候选答案（n-generation）。

## 核心功能

- **文本补全**: 给定一段文字，模型预测接下来的内容。
- **Token 统计**: 大部分 LLM 实现都支持通过回调追踪 Token 使用。
- **异步支持**: 提供 `ainvoke` 和 `agenerate` 方法。

## 常见模型实现

| 模型 | 说明 |
| :--- | :--- |
| `OpenAI` | OpenAI 的文本补全模型（如 `gpt-3.5-turbo-instruct`）。 |
| `HuggingFacePipeline` | 在本地通过 Hugging Face 运行模型。 |
| `LlamaCpp` | 通过 llama.cpp 绑定运行本地 GGUF 模型。 |
| `Ollama` | 接入本地运行的 Ollama 服务。 |
| `Anthropic` | Anthropic 的传统补全接口（现已推荐使用 Chat 接口）。 |

## 使用示例

```python
from langchain_openai import OpenAI

llm = OpenAI(model="gpt-3.5-turbo-instruct", temperature=0)

# 直接调用
response = llm.invoke("Once upon a time,")
print(response)
```

## 与 Chat Models 的区别

| 特性 | LLMs | Chat Models |
| :--- | :--- | :--- |
| **输入** | 纯字符串 (String) | 消息列表 (List of BaseMessage) |
| **输出** | 纯字符串 (String) | 消息对象 (AIMessage) |
| **适用场景** | 文本续写、简单指令执行 | 对话、复杂角色扮演、工具调用 |

## 迁移指南

虽然传统的 `LLM` 接口依然可用，但在现代开发中，**Chat Models** 已经成为主流。
- **建议**: 优先使用 `langchain_classic.chat_models` 或直接从 `langchain_openai`, `langchain_anthropic` 等包中导入 `ChatOpenAI`, `ChatAnthropic` 等类。
- **集成**: 实际的模型实现现在主要位于 `langchain-community` 和各个厂商的特定包中。
