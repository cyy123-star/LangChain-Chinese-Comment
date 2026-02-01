# libs\langchain\langchain_classic\llms\base.py

此文档提供了 `libs\langchain\langchain_classic\llms\base.py` 文件的详细中文注释。该文件是一个向后兼容的模块，用于导出核心语言模型（LLM）类。

## 文件概述

该文件主要负责将 `langchain_core` 中的核心 LLM 接口重新导出，以便旧版本的 LangChain 用户可以继续从 `langchain.llms` 路径导入这些基础类。

## 导出的核心类

### 1. `LLM`
- **来源**: 重定向自 `langchain_core.language_models.llms.LLM`。
- **作用**: 用户实现自定义 LLM 的推荐抽象基类。它简化了接口，只需要实现 `_call` 方法即可。

### 2. `BaseLLM`
- **来源**: 重定向自 `langchain_core.language_models.llms.BaseLLM`。
- **作用**: 所有 LLM 实现的基础抽象类。提供了更底层的控制，如 `_generate` 方法。

### 3. `BaseLanguageModel`
- **来源**: 重定向自 `langchain_core.language_models.BaseLanguageModel`。
- **作用**: LLM 和聊天模型的公共基类，定义了统一的调用接口。

## 注意事项

1. **兼容性**: 该模块的存在完全是为了保持 API 的稳定性。
2. **建议**: 对于新开发的组件，建议直接从 `langchain_core.language_models` 导入相应的类。
3. **区别**: 在 LangChain 中，`LLM` 通常指代纯文本输入/输出的模型，而 `ChatModel` 指代基于消息（Messages）的模型。虽然它们都继承自 `BaseLanguageModel`，但在处理输入输出格式上有所不同。

