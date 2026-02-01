# Schema (接口定义与数据结构)

`schema` 模块定义了 LangChain 整个生态系统通用的基础数据结构和接口协议。它是确保不同组件（如不同的向量数据库、不同的 LLM）能够互相协作的基石。

## 核心消息类型 (Messages)

对话模型交互的基础单元：
- `BaseMessage`: 所有消息的基类。
- `HumanMessage`: 用户发送的消息。
- `AIMessage`: 模型生成的响应。
- `SystemMessage`: 系统提示/指令。
- `ChatMessage`: 带有任意角色名称的消息。
- `ToolMessage`: 包含工具调用结果的消息。

## 文档与存储 (Documents & Storage)

- `Document`: 包含 `page_content` (文本) 和 `metadata` (元数据) 的标准文档结构。
- `BaseStore`: 键值对存储接口（如用于 `ParentDocumentRetriever`）。
- `BaseChatMessageHistory`: 存储和检索对话历史的接口。

## 模型与检索接口

- `BaseLanguageModel`: 所有 LLM 和 ChatModel 的父类。
- `BaseRetriever`: 定义了 `get_relevant_documents` 方法的检索器基类。
- `Embeddings`: 文本嵌入接口。

## 输出解析 (Outputs)

- `Generation`: 单次文本生成的输出。
- `ChatGeneration`: 对话模型生成的输出。
- `LLMResult`: 包含多次生成结果和供应商特定元数据的容器。

## 回调与追踪 (Callbacks)

- `BaseCallbackHandler`: 监听组件生命周期的钩子接口。
- `BaseCallbackManager`: 管理和分发事件的处理器。

## 迁移说明

- **标准化**: 所有的 Schema 定义现在均由 `langchain-core` 统一管理。
- **不可变性**: 大部分核心对象（如 `Document`, `Message`）都是基于 Pydantic 的，支持序列化和反序列化。
- **解耦**: 开发者在实现自定义组件（如自定义检索器）时，只需继承 `schema` 中定义的基类即可保证与 LangChain 其他部分的兼容性。
