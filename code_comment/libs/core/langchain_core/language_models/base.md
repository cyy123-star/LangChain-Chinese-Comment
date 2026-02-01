# base.py

## 文件概述
`base.py` 定义了 LangChain 中所有语言模型的抽象基类 `BaseLanguageModel`。它是连接不同厂商（如 OpenAI, Anthropic, HuggingFace 等）语言模型的核心抽象层，为开发者提供了统一的接口来与 LLM 或聊天模型进行交互。

该类通过继承 `RunnableSerializable` 深度集成了 LangChain 表达式语言（LCEL），支持缓存、回调、追踪及跨模型的统一调用方式。

---

## 导入依赖
- `abc`: 用于定义抽象基类 `BaseLanguageModel`。
- `langchain_core.caches`: 提供 `BaseCache` 接口用于响应缓存。
- `langchain_core.callbacks`: 处理运行过程中的回调逻辑。
- `langchain_core.messages`: 处理 `BaseMessage` 及其子类。
- `langchain_core.prompt_values`: 定义统一的提示词输入包装器 `PromptValue`。
- `langchain_core.runnables`: 继承 `RunnableSerializable` 以支持 LCEL。
- `transformers` (可选): 用于默认的 token 计数（GPT-2 分词器）。

---

## 类与函数详解

### 1. `BaseLanguageModel` (类)
所有语言模型包装器的抽象基类。

#### 属性说明
| 属性名 | 类型 | 默认值 | 是否必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `cache` | `BaseCache \| bool \| None` | `None` | 否 | 是否缓存响应。`True` 使用全局缓存；`BaseCache` 实例使用指定缓存。 |
| `verbose` | `bool` | 全局配置 | 否 | 是否打印响应文本。 |
| `callbacks` | `Callbacks` | `None` | 否 | 添加到运行追踪中的回调函数列表。 |
| `tags` | `list[str] \| None` | `None` | 否 | 添加到运行追踪中的标签，便于在 LangSmith 中过滤。 |
| `metadata` | `dict[str, Any] \| None` | `None` | 否 | 添加到运行追踪中的元数据。 |
| `custom_get_token_ids` | `Callable \| None` | `None` | 否 | 可选的自定义 token 编码器，用于精确计算 token 数。 |

#### 核心方法
- **`generate_prompt / agenerate_prompt` (抽象方法)**: 
  - **功能**: 接收 `PromptValue` 列表并返回 `LLMResult`。这是最底层的生成接口，支持批量调用和多候选项输出。
  - **参数**: `prompts`, `stop` (停止词), `callbacks`, `**kwargs`。
- **`invoke / ainvoke`**:
  - **功能**: LCEL 的核心入口。将输入转换为模型输出。
  - **输入**: `str`, `PromptValue` 或 `list[BaseMessage]`。
  - **输出**: `BaseMessage` (聊天模型) 或 `str` (LLM)。
- **`predict / apredict`**:
  - **功能**: 接收字符串输入，返回字符串输出。主要用于传统的文本补全场景。
- **`predict_messages / apredict_messages`**:
  - **功能**: 接收消息列表，返回单条消息。主要用于聊天场景。
- **`get_num_tokens / get_num_tokens_from_messages`**:
  - **功能**: 计算文本或消息列表的 token 数量。默认使用 GPT-2 分词器。

---

## 核心逻辑解读
1. **输入自适应**：`BaseLanguageModel` 能够识别多种输入格式（字符串、消息、`PromptValue`），并根据具体子类（LLM 或 ChatModel）的需求进行转换。
2. **LCEL 集成**：通过实现 `invoke` 等方法，模型可以像普通函数一样在 `chain = prompt | model | parser` 中无缝流动。
3. **缓存机制**：在生成响应前，会检查 `cache` 配置。如果命中缓存且非流式模式，则直接返回缓存结果，减少 API 调用开销。
4. **Token 计数兜底**：如果没有提供 `custom_get_token_ids`，系统会尝试加载 `transformers` 库中的 GPT-2 分词器作为通用估算方案。

---

## 使用示例

### 1. 作为 LCEL 链的一部分
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI # 假设使用此实现

prompt = ChatPromptTemplate.from_template("讲一个关于 {topic} 的笑话")
model = ChatOpenAI()

chain = prompt | model
response = chain.invoke({"topic": "熊"})
print(response.content)
```

### 2. 使用缓存
```python
from langchain.globals import set_llm_cache
from langchain_community.cache import InMemoryCache

set_llm_cache(InMemoryCache())
# 第一次调用会访问 API
model.invoke("你好")
# 第二次相同调用将直接从内存返回
model.invoke("你好")
```

---

## 注意事项
- **流式不支持缓存**：目前 LangChain 的流式传输（Streaming）接口通常会跳过缓存逻辑。
- **精度提醒**：默认的 GPT-2 分词器仅用于估算 token。对于像 Claude 或 Llama 这样有特定分词规则的模型，建议通过 `custom_get_token_ids` 传入对应厂商的工具。
- **异步支持**：在生产环境中，强烈建议使用 `ainvoke` 或 `agenerate_prompt` 以提高并发性能。

---

## 内部调用关系
- **继承关系**: `BaseLanguageModel` -> `RunnableSerializable` -> `Runnable`。
- **子类实现**:
  - `BaseLLM` (位于 `llms.py`): 针对纯文本补全模型的特化。
  - `BaseChatModel` (位于 `chat_models.py`): 针对对话式消息模型的特化。

---

## 相关链接
- [LangChain 概念指南 - 语言模型](https://python.langchain.com/docs/concepts/#language-models)
- [langchain_core.runnables 源码](../runnables/base.py)

---
**对应源码版本**: LangChain Core v1.2.7
**最后更新时间**: 2026-01-29
