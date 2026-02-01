# fake.py - 用于测试的虚假大语言模型 (Fake LLMs)

## 文件概述
`fake.py` 提供了一组用于单元测试和集成测试的虚假大语言模型（LLM）实现。这些模型不调用任何真实的外部 API，而是根据预设的列表返回响应。这使得开发者可以在不产生费用、不依赖网络的情况下测试 LangChain 链（Chains）和逻辑。

---

## 导入依赖
- **`asyncio`**: 支持异步测试。
- **`time`**: 用于模拟响应延迟。
- **`langchain_core.language_models.llms`**: 继承自 `LLM` 基类。
- **`langchain_core.runnables`**: 支持 LCEL 运行配置。

---

## 类与函数详解

### 1. FakeListLLM
**功能描述**: 一个简单的 LLM，按顺序循环返回预设的响应列表。

#### 核心属性
| 参数名 | 类型 | 默认值 | 描述 |
| :--- | :--- | :--- | :--- |
| `responses` | `list[str]` | 必填 | 预设的响应字符串列表。 |
| `sleep` | `float \| None` | `None` | 模拟响应前的延迟时间（秒）。 |
| `i` | `int` | `0` | 内部计数器，记录当前返回到第几个响应。 |

#### 关键方法
- **`_call`**: 同步返回列表中的下一个响应。
- **`_acall`**: 异步返回列表中的下一个响应。
- **`_identifying_params`**: 返回包含 `responses` 的字典，用于追踪。

---

### 2. FakeStreamingListLLM
**功能描述**: 继承自 `FakeListLLM`，支持流式输出测试。它会将完整的响应字符串拆分为单个字符，逐个 yield 出来。

#### 核心属性
| 参数名 | 类型 | 默认值 | 描述 |
| :--- | :--- | :--- | :--- |
| `error_on_chunk_number` | `int \| None` | `None` | 如果设置，将在流式输出到指定序号的块时抛出异常。 |

#### 关键方法
- **`stream`**: 模拟同步流式输出，支持 `sleep` 间隔。
- **`astream`**: 模拟异步流式输出，支持 `asyncio.sleep` 间隔。

---

## 核心逻辑解读
1. **循环响应**: `FakeListLLM` 使用内部变量 `i` 跟踪当前响应。当达到列表末尾时，它会重置为 0，从而实现循环返回。
2. **流式模拟**: `FakeStreamingListLLM` 通过将 `invoke` 的结果进行迭代（字符串迭代即字符迭代），模拟了流式传输的过程。
3. **异常模拟**: 通过 `error_on_chunk_number`，可以非常方便地测试链在处理流式异常时的鲁棒性。

---

## 使用示例

### 基础用法
```python
from langchain_core.language_models.fake import FakeListLLM

responses = ["你好！", "我是 LangChain 助手。", "有什么可以帮您的？"]
llm = FakeListLLM(responses=responses)

print(llm.invoke("Hi"))  # 输出: 你好！
print(llm.invoke("Who are you?"))  # 输出: 我是 LangChain 助手。
```

### 流式测试
```python
from langchain_core.language_models.fake import FakeStreamingListLLM

llm = FakeStreamingListLLM(responses=["Hello World"], sleep=0.1)

for chunk in llm.stream("test"):
    print(chunk, end="|", flush=True)
# 输出: H|e|l|l|o| |W|o|r|l|d|
```

---

## 注意事项
- **非线程安全**: 内部计数器 `i` 在并发调用时可能不会按预期顺序增加。
- **参数忽略**: 传入的 `prompt` 实际上被忽略了，模型仅根据顺序返回结果。
- **测试专用**: 严禁在生产环境中使用这些类。

---

## 内部调用关系
- **`LLM`**: 继承自 `langchain_core.language_models.llms.LLM`，实现了所需的最小接口。
- **`CallbackManager`**: 尽管是 Fake LLM，它仍然会触发标准的回调事件。

---

## 相关链接
- [LangChain 官方文档 - Testing](https://python.langchain.com/docs/modules/model_io/llms/custom_llm)
- [langchain_core.language_models.llms 源码](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/core/langchain_core/language_models/llms.py)

---

## 元信息
- **最后更新时间**: 2026-01-29
- **对应源码版本**: LangChain Core v1.2.7
