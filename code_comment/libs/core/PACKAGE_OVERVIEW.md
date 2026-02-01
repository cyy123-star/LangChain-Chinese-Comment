# LangChain Core (langchain-core) 技术文档

`langchain-core` 是整个 LangChain 生态系统的基石，定义了构建大语言模型（LLM）应用的基础抽象、接口和通用调用协议（Runnables）。

---

## **1. 核心功能与主要 API**

### **核心功能**
- **标准化接口**：定义了 LLMs、聊天模型（Chat Models）、向量存储（Vector Stores）、检索器（Retrievers）等核心组件的标准接口。
- **LCEL (LangChain Expression Language)**：通过 `Runnable` 协议实现组件的可组合性，支持链式调用、并行执行、异步处理等。
- **消息与提示词管理**：统一的消息对象模型（Human, AI, System）和提示词模板系统。
- **回调与追踪**：提供基础的回调系统，支持对执行过程进行监控和日志记录（深度集成 LangSmith）。
- **序列化与加载**：提供跨语言、跨版本的组件序列化与反序列化机制。

### **主要 API 概览**

| 模块 | 核心类/函数 | 功能描述 |
| :--- | :--- | :--- |
| **Runnables** | `Runnable`, `RunnableSequence`, `RunnableParallel` | LCEL 的核心协议，定义了 `invoke`, `batch`, `stream` 等通用方法。 |
| **Messages** | `BaseMessage`, `HumanMessage`, `AIMessage`, `SystemMessage` | 定义了与模型交互的标准消息模型。 |
| **Prompts** | `BasePromptTemplate`, `ChatPromptTemplate` | 将原始输入转换为模型可接受的提示词格式。 |
| **Models** | `BaseLanguageModel`, `BaseChatModel`, `BaseLLM` | 定义了语言模型和聊天模型的抽象接口。 |
| **Outputs** | `BaseOutputParser`, `JsonOutputParser` | 将模型输出解析为结构化数据或特定格式。 |
| **Tools** | `BaseTool`, `tool` 装饰器 | 定义了模型可以调用的外部工具接口。 |
| **Vector Stores** | `VectorStore` | 向量数据库的抽象基类。 |

### **配置参数**
在 `langchain-core` 中，大多数组件通过 `Pydantic` 进行配置。常见全局或通用参数包括：
- `tags`: 用于追踪的标签列表。
- `metadata`: 与运行关联的元数据字典。
- `callbacks`: 回调处理器列表。
- `configurable`: 运行时可配置的参数字典。

### **使用示例**

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# 1. 定义提示词模板
prompt = ChatPromptTemplate.from_template("告诉我关于 {topic} 的一个笑话")

# 2. 模拟模型输出（实际使用时需配合 langchain-openai 等集成包）
# model = ChatOpenAI() 
output_parser = StrOutputParser()

# 3. 使用 LCEL 构建链
chain = (
    {"topic": RunnablePassthrough()} 
    | prompt 
    # | model 
    | output_parser
)

# 4. 调用
# result = chain.invoke("冰淇淋")
# print(result)
```

---

## **2. 整体架构分析**

### **内部模块划分**
- **`runnables/`**：整个包的灵魂，实现了组件之间的管道符号 (`|`) 操作逻辑。
- **`language_models/`**：抽象了模型调用逻辑，确保不同厂商的模型（OpenAI, Anthropic 等）具有一致的行为。
- **`messages/` & `outputs/`**：定义了数据流的输入输出标准，确保组件间数据对接无误。
- **`callbacks/` & `tracers/`**：横向切面模块，负责监控数据流。
- **`utils/`**：包含 Pydantic 增强、异步迭代处理等底层工具。

### **依赖关系**
- **轻量化设计**：`langchain-core` 严格限制第三方依赖，不包含任何具体的模型集成（如 OpenAI SDK）。
- **主要依赖**：
    - `pydantic`: 核心数据模型验证。
    - `langsmith`: 官方追踪平台集成。
    - `tenacity`: 重试逻辑。
    - `jsonpatch`: 用于状态更新和补丁。

### **设计模式**
- **策略模式 (Strategy Pattern)**：通过定义 `BaseLanguageModel` 等基类，允许在运行时切换不同的具体实现。
- **命令模式 (Command Pattern)**：`Runnable` 协议本质上是将操作封装为对象。
- **装饰器模式 (Decorator Pattern)**：利用 `tool` 等装饰器简化组件定义。
- **组合模式 (Composite Pattern)**：LCEL 允许将小组件组合成复杂的处理链。

### **数据流转机制**
1. **输入阶段**：数据通过 `Runnable.invoke()` 进入。
2. **转换阶段**：数据在链中流动，每一层可能是 `Prompt` (转换格式)、`Model` (生成内容) 或 `OutputParser` (解析结果)。
3. **协议保障**：`RunnableSequence` 确保前一个组件的输出类型与后一个组件的输入类型匹配。
4. **横向监控**：在每个组件执行前后，`CallbackManager` 会触发相应的钩子函数，将数据发送给 `Tracers`。

---

## **3. 注意事项**
- **版本兼容性**：作为底层包，其 API 的变更会影响所有上层包（如 `langchain`）。
- **异步支持**：几乎所有核心方法（`invoke`, `stream`, `batch`）都有对应的异步版本（`ainvoke`, `astream`, `abatch`）。
- **线程安全**：在编写自定义 `Runnable` 或回调时，需注意并发环境下的状态安全性。
