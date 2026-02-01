# llms.py

## 文件概述
`llms.py` 模块定义了传统大语言模型（LLM）的抽象基类 `BaseLLM`。与 `BaseChatModel` 不同，`BaseLLM` 的设计初衷是处理纯文本输入（Prompt）并返回纯文本输出（String）。

虽然现代开发更多地使用聊天模型，但 `BaseLLM` 仍然是 LangChain 框架中处理文本补全、指令遵循等任务的重要基础。它同样继承自 `BaseLanguageModel`，完整支持 LCEL、缓存和回调机制。

---

## 导入依赖
- `langchain_core.language_models.base`: 继承自 `BaseLanguageModel`。
- `langchain_core.outputs`: 定义 `LLMResult`, `Generation` 等输出结构。
- `langchain_core.prompt_values`: 处理不同类型的提示词输入。
- `tenacity`: 提供内置的重试装饰器逻辑。
- `langchain_core.caches`: 处理响应缓存。

---

## 类与函数详解

### 1. `BaseLLM` (类)
传统文本补全模型的抽象基类。

#### 核心方法
- **`_generate / _agenerate` (抽象方法)**: 
  - **功能**: 子类必须实现的底层逻辑，负责将字符串列表转换为 `LLMResult`。
  - **参数**: `prompts` (字符串列表), `stop`, `run_manager`, `**kwargs`。
- **`invoke / ainvoke`**:
  - **功能**: 接收输入（自动转换为字符串），返回模型生成的第一个文本候选项。
- **`batch / abatch`**:
  - **功能**: 批量处理多个输入。如果模型支持批量 API，则会优化调用；否则会并发处理。
- **`stream / astream`**:
  - **功能**: 流式返回文本块（`GenerationChunk`）。如果子类未实现 `_stream`，则一次性返回。

---

### 2. 辅助工具

#### `create_base_retry_decorator` (函数)
- **功能**: 为 LLM 调用创建一个基于 `tenacity` 的重试装饰器。
- **特点**: 支持指数退避算法，并能在重试前触发回调（`on_retry`），便于追踪失败原因。

#### `get_prompts` / `aget_prompts` (函数)
- **功能**: 在调用模型前，检查缓存中是否已经存在对应的结果。
- **返回值**: 返回已存在的缓存结果和仍需调用的缺失提示词。

---

## 核心逻辑解读

### 1. 输入转换逻辑 (`_convert_input`)
`BaseLLM` 虽然主打文本处理，但它具有很强的兼容性：
- 如果输入是 `ChatPromptValue`（消息列表），它会通过 `get_buffer_string` 将其转换为一段连贯的文本（通常带有角色前缀，如 "Human: ..."）。
- 这种机制保证了即使是专门为对话设计的 Prompt 也能在传统 LLM 上运行。

### 2. 缓存处理流程
1. **解析缓存**：通过 `_resolve_cache` 确定使用全局缓存还是实例级缓存。
2. **查找**：调用 `get_prompts` 批量检查输入。
3. **更新**：模型生成结果后，调用 `update_cache` 将新结果存入缓存。

### 3. 重试机制
LangChain 内置了对网络抖动或临时性错误的容错处理。开发者可以通过配置 `max_retries` 结合 `create_base_retry_decorator` 来增强应用的稳定性。

---

## 使用示例

### 1. 基础调用 (以 OpenAI 为例)
```python
from langchain_openai import OpenAI

llm = OpenAI(model="gpt-3.5-turbo-instruct")
# 简单调用
response = llm.invoke("谁是世界上最伟大的科学家？")
print(response)
```

### 2. 批量处理
```python
prompts = ["1+1=?", "2+2=?"]
# 批量获取结果列表
results = llm.batch(prompts)
for res in results:
    print(res)
```

---

## 注意事项
- **输出局限性**：`BaseLLM` 的 `invoke` 默认只返回 `generations[0][0].text`。如果模型配置了生成多个候选项（`n > 1`），建议使用 `generate_prompt` 获取完整结果。
- **向聊天模型迁移**：由于 OpenAI 等主流厂商已逐步淘汰纯补全模型，建议新项目优先考虑 `BaseChatModel`。
- **参数一致性**：`stop` 参数在 `invoke` 中传入会覆盖模型初始化时的默认停止词。

---

## 内部调用关系
- **依赖关系**: 依赖 `langchain_core.language_models.base` 的基础定义。
- **集成点**: 与 `langchain_core.runnables` 深度集成，作为链（Chain）的执行节点。

---

## 相关链接
- [LangChain 官方文档 - LLMs](https://python.langchain.com/docs/modules/model_io/llms/)
- [base.py 源码](./base.md)

---
**对应源码版本**: LangChain Core v1.2.7
**最后更新时间**: 2026-01-29
