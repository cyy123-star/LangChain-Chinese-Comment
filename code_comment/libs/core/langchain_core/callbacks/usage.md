# UsageMetadataCallbackHandler

## 文件概述
`usage.py` 提供了用于跟踪和汇总大语言模型（LLM）Token 使用情况（Usage Metadata）的工具。它定义了一个回调处理器 `UsageMetadataCallbackHandler` 和一个上下文管理器 `get_usage_metadata_callback`，允许开发者在复杂的链式调用中，自动统计不同模型消耗的 Token 数量（包括输入、输出、总计及详细分类）。

## 导入依赖
- `threading.Lock`: 确保在并发环境下（如并发运行多个 Chain）更新 Token 计数时的线程安全性。
- `contextvars.ContextVar`: 用于在异步上下文中存储和传播回调处理器实例。
- `langchain_core.messages.ai.add_usage`: 用于将两个 `UsageMetadata` 对象进行数值累加的工具函数。
- `langchain_core.tracers.context.register_configure_hook`: 用于将上下文变量注册到 LangChain 的配置机制中，实现自动继承。

## 类与函数详解
### 1. UsageMetadataCallbackHandler
**功能描述**: 汇总 `AIMessage` 中携带的 `usage_metadata`。它会根据模型名称（Model Name）对 Token 使用情况进行分类统计。

#### 核心属性
| 属性名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `usage_metadata` | `dict[str, UsageMetadata]` | 存储统计结果。键为模型名称，值为该模型的累计 Token 使用情况。 |

#### 核心方法
- **`on_llm_end(response, **kwargs)`**: 
    - **逻辑**: 从 `LLMResult` 中提取第一条生成的 `ChatGeneration`，获取其中的 `AIMessage`。
    - **处理**: 提取 `usage_metadata`（Token 计数）和 `model_name`。
    - **汇总**: 使用线程锁（Lock）保护共享状态，通过 `add_usage` 将本次消耗累加到该模型的总额中。

---

### 2. get_usage_metadata_callback
**功能描述**: 一个便捷的上下文管理器（Context Manager），用于在特定代码块内自动追踪 Token 使用。

#### 参数说明
| 参数名 | 类型 | 默认值 | 详细用途 |
| :--- | :--- | :--- | :--- |
| `name` | `str` | `"usage_metadata_callback"` | 内部使用的 ContextVar 名称。 |

#### 返回值
- 返回一个 `UsageMetadataCallbackHandler` 实例。

#### 使用示例
```python
from langchain_core.callbacks import get_usage_metadata_callback
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

with get_usage_metadata_callback() as cb:
    llm.invoke("Hello")
    llm.invoke("How are you?")
    
    # 打印汇总后的 Token 使用情况
    print(cb.usage_metadata)
    # 输出示例: {'gpt-4o-mini': {'input_tokens': 16, 'output_tokens': 20, 'total_tokens': 36, ...}}
```

#### 注意事项
- **版本要求**: 该功能是在 `langchain-core 0.3.49` 中引入的。
- **模型支持**: 依赖于底层 Chat Model 必须正确填充 `AIMessage.usage_metadata`。大多数主流模型（OpenAI, Anthropic, Google 等）的新版本均已支持。

## 内部调用关系
- **组件交互**: 通过 `register_configure_hook` 与 LangChain 的 `RunnableConfig` 机制深度集成。
- **逻辑依赖**: 使用 `add_usage` 递归地合并嵌套的 Token 详情（如 Reasoning Tokens, Cache Tokens 等）。

## 相关链接
- [LangChain 官方文档 - Token Usage](https://python.langchain.com/docs/modules/model_io/models/chat/token_usage_tracking/)
- [源码文件](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/core/langchain_core/callbacks/usage.py)

---
最后更新时间: 2026-01-29
对应源码版本: LangChain Core v1.2.7
