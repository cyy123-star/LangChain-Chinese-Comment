# Chat Models (聊天模型)

`chat_models` 模块是 LangChain v1 中使用聊天模型的入口点。它通过统一的工厂接口简化了跨提供商（OpenAI, Anthropic, Google 等）的模型实例化过程。

## 核心导出

- **[init_chat_model](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain_v1/langchain/chat_models/base.md)**: 推荐的工厂函数，用于根据名称和配置初始化模型。支持固定模型和运行时可配置模型。
- **BaseChatModel**: 所有聊天模型的基类（从 `langchain_core` 重新导出）。

## 主要优势

1. **统一接口**: 使用相同的函数初始化不同厂商的模型，无需手动导入 `ChatOpenAI` 或 `ChatAnthropic`。
2. **解耦逻辑**: 应用程序代码可以仅依赖模型名称，具体的集成包加载由工厂函数处理。
3. **强大的配置系统**: 支持通过 `RunnableConfig` 在运行时动态覆盖模型参数、切换模型甚至切换提供商。
4. **延迟加载**: 在可配置模式下，直到第一次调用 `invoke` 时才会加载并初始化真实的模型对象。

## 快速开始

```python
from langchain.chat_models import init_chat_model

# 快速初始化
model = init_chat_model("openai:gpt-4o", temperature=0)

# 结构化输出支持
structured_llm = model.with_structured_output(MySchema)
```

详情请参考 **[Base 模块文档](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain_v1/langchain/chat_models/base.md)**。
