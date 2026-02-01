# LangChain Partners (libs/partners) 技术文档

`libs/partners` 目录是 LangChain 生态中用于托管第三方集成（Integrations）的专用空间。为了保证核心库的轻量化，LangChain 将具体的模型商（如 OpenAI, Anthropic）和工具商（如 Chroma, Pinecone）的实现剥离到独立的包中。

---

## **1. 整体架构与设计原则**

### **核心原则**
- **解耦**：核心库 `langchain-core` 仅定义接口，`partners` 目录下各包实现接口。
- **独立发布**：每个 partner 包（如 `langchain-openai`）都有独立的版本号、`pyproject.toml` 和依赖管理。
- **标准化结构**：所有 partner 包遵循统一的目录结构，便于维护和自动化测试。

### **统一目录结构**
每个 partner 包通常包含以下内容：
- `langchain_<partner_name>/`：源代码目录。
    - `chat_models.py`：实现 `BaseChatModel`。
    - `llms.py`：实现 `BaseLLM`（如果适用）。
    - `embeddings.py`：实现 `Embeddings`。
    - `vectorstores.py`：实现 `VectorStore`（针对数据库商）。
- `tests/`：包含单元测试和集成测试。
- `pyproject.toml`：定义包元数据及特定依赖（如 `openai` SDK）。

---

## **2. 依赖关系与数据流**

### **依赖关系**
1. **向下依赖**：所有 partner 包都依赖 `langchain-core`。
2. **外部依赖**：依赖对应厂商的官方 SDK（如 `openai` 库, `anthropic` 库）。
3. **互不依赖**：`partners` 目录下的各包之间原则上不应产生直接依赖。

### **数据流转**
1. **配置注入**：用户通过 API Key 等参数初始化 partner 包中的类。
2. **请求转换**：Partner 包将 LangChain 标准的 `BaseMessage` 转换为厂商 SDK 要求的格式。
3. **API 调用**：通过官方 SDK 发起网络请求。
4. **结果映射**：将 SDK 返回的原始响应映射回 LangChain 标准的 `ChatResult` 或 `AIMessage`。

---

## **3. 开发者指南**

### **如何使用 Partner 包**
用户应直接安装对应的集成包，而不是安装整个 `langchain`：
```bash
pip install langchain-openai
```

### **主要 API 调用示例（以 OpenAI 为例）**
```python
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4", api_key="...")
# 内部会调用 openai 官方 SDK 并处理 LangChain 协议
response = model.invoke("你好")
```

---

## **4. 注意事项**
- **版本对齐**：当 `langchain-core` 更新时，partner 包通常需要同步发布新版本以支持新特性。
- **凭证管理**：绝大多数 partner 包依赖环境变量（如 `OPENAI_API_KEY`）进行身份验证。
- **性能差异**：不同 partner 的实现受限于其官方 SDK 的性能和并发限制。
