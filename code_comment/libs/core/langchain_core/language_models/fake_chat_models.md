# fake_chat_models.py - 用于测试的虚假聊天模型 (Fake Chat Models)

## 文件概述
`fake_chat_models.py` 提供了一系列用于测试聊天模型接口的虚假实现。这些模型不调用真实 API，而是返回预定义的消息。它们涵盖了同步生成、异步生成、流式传输以及回调函数测试等多种场景。

---

## 导入依赖
- **`asyncio`**: 用于异步模拟。
- **`langchain_core.language_models.chat_models`**: 继承自 `BaseChatModel` 和 `SimpleChatModel`。
- **`langchain_core.messages`**: 使用 `AIMessage`, `AIMessageChunk`, `BaseMessage` 等消息类。
- **`langchain_core.outputs`**: 定义生成结果结构（`ChatResult`, `ChatGeneration`）。

---

## 类与函数详解

### 1. FakeMessagesListChatModel
**功能描述**: 一个基础的虚假聊天模型，循环返回预设的消息对象列表。

| 参数名 | 类型 | 默认值 | 描述 |
| :--- | :--- | :--- | :--- |
| `responses` | `list[BaseMessage]` | 必填 | 预设的消息对象（如 `AIMessage`）列表。 |
| `sleep` | `float \| None` | `None` | 模拟响应延迟。 |

---

### 2. FakeListChatModel
**功能描述**: 继承自 `SimpleChatModel`，返回字符串列表并支持流式模拟。它会将字符串拆分为字符块进行流式输出。

#### 关键方法
- **`_call`**: 同步返回下一个字符串。
- **`_stream / _astream`**: 模拟流式输出，将响应字符串拆分为 `AIMessageChunk` 逐个 yield。
- **`batch / abatch`**: 手动重写批量处理，确保顺序执行而不使用并发，便于预测测试结果。

---

### 3. GenericFakeChatModel
**功能描述**: 一个功能更全的虚假聊天模型，旨在模拟更真实的聊天场景。

#### 核心特性
- **消息生成**: 接收一个消息迭代器（`Iterator`），每次调用返回迭代器的下一个值。
- **流式模拟**: 接收生成的消息后，使用正则表达式 `(\s)` 将文本按空格和单词拆分为块，模拟真实的 Token 生成过程。
- **回调触发**: 在流式输出过程中会主动调用 `run_manager.on_llm_new_token`。
- **工具调用模拟**: 支持解析并流式输出 `additional_kwargs` 中的 `function_call` 信息。

---

### 4. ParrotFakeChatModel
**功能描述**: “复读机”模型，始终将用户输入的最后一条消息原样返回。常用于测试输入输出管道。

---

## 核心逻辑解读
1. **流式拆分逻辑**: 在 `GenericFakeChatModel._stream` 中，通过 `re.split(r"(\s)", content)` 能够保留空格并将其作为独立的块输出，这更接近真实模型流式返回单词的效果。
2. **状态维护**: 大多数 Fake 模型使用内部计数器 `i` 配合取模运算（通过判断 `i < len - 1`）来实现循环。
3. **Chunk 标记**: 在流式输出的最后一个块上，会自动设置 `chunk_position="last"`，用于测试流式结束标记逻辑。

---

## 使用示例

### 模拟流式单词生成
```python
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage

# 创建一个预设消息的迭代器
messages = iter([AIMessage(content="Hello world from LangChain!")])
model = GenericFakeChatModel(messages=messages)

# 测试流式输出
for chunk in model.stream("hi"):
    print(f"'{chunk.content}'", end="|")
# 输出: 'Hello'|' '|'world'|' '|'from'|' '|'LangChain'|'!'|
```

### 复读机模型测试
```python
from langchain_core.language_models.fake_chat_models import ParrotFakeChatModel
from langchain_core.messages import HumanMessage

model = ParrotFakeChatModel()
response = model.invoke([HumanMessage(content="复读这段话")])
print(response.content) # 输出: 复读这段话
```

---

## 注意事项
- **迭代器耗尽**: `GenericFakeChatModel` 使用的是迭代器，一旦遍历完所有预设消息，再次调用将抛出 `StopIteration`。
- **异步支持**: 虽然提供了 `_astream`，但大多实现内部仍依赖同步方法或简单的 `await asyncio.sleep`。

---

## 内部调用关系
- **`BaseChatModel`**: 所有虚假聊天模型都遵循 `BaseChatModel` 的标准生命周期。
- **`ChatGenerationChunk`**: 用于封装流式输出的块。

---

## 相关链接
- [LangChain 官方文档 - Chat Models](https://python.langchain.com/docs/modules/model_io/chat/)
- [langchain_core.messages 源码](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/core/langchain_core/messages/base.py)

---

## 元信息
- **最后更新时间**: 2026-01-29
- **对应源码版本**: LangChain Core v1.2.7
