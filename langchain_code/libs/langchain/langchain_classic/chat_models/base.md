# Chat Models (对话模型)

`chat_models` 模块包含了对各种对话式大语言模型（如 GPT-4, Claude, Llama 等）的抽象和实现。

## 核心抽象

### 1. `BaseChatModel`
所有对话模型的基类。它要求模型接收一系列消息（`BaseMessage` 对象）并返回一个 `BaseMessage` 作为响应。

### 2. `SimpleChatModel`
一个简化的基类，开发者只需实现接收字符串并返回字符串的逻辑，它会自动处理消息对象的转换。

## 统一初始化：`init_chat_model`

这是现代 LangChain 推荐的一种极其方便的模型加载方式。它允许你通过一个统一的接口加载不同厂商的模型。

### 优势
- **厂商无关**: 只需要更改字符串（如 `gpt-4o` -> `claude-3-opus`），无需更改大量导入语句。
- **可配置性**: 支持在运行时通过 `config` 动态切换模型。

### 示例代码

```python
from langchain_classic.chat_models import init_chat_model

# 1. 加载特定模型
gpt = init_chat_model("gpt-4o", model_provider="openai", temperature=0)
claude = init_chat_model("claude-3-5-sonnet-20240620", model_provider="anthropic")

# 2. 统一调用
response = gpt.invoke("What is LCEL?")
```

## 核心方法

| 方法 | 说明 |
| :--- | :--- |
| `invoke(input)` | 发送消息并获取响应。 |
| `stream(input)` | 流式获取响应内容。 |
| `bind_tools(tools)` | 将工具（Tools/Functions）绑定到模型。 |
| `with_structured_output(schema)` | 强制模型按照指定的 Schema（如 Pydantic 类）输出结果。 |

## 消息类型

对话模型处理的是消息流，常见的消息类型包括：
- `SystemMessage`: 系统指令。
- `HumanMessage`: 用户输入。
- `AIMessage`: 模型响应。
- `ToolMessage`: 工具执行结果。

## 迁移指南

虽然 `langchain_classic` 提供了这些类的入口，但实际的实现已经移到了各个集成包中：
- OpenAI: `pip install langchain-openai`
- Anthropic: `pip install langchain-anthropic`
- Google: `pip install langchain-google-genai`

建议在新项目中直接从这些特定包中导入模型类。
