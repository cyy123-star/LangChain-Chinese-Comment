# LangChain Standard Tests (langchain-tests) 技术文档

`langchain-tests` 是一个专门用于标准化测试的工具包。它为 LangChain 的各类组件（如 ChatModel, VectorStore, Embeddings）提供了一套标准的测试基类。任何新的集成（Partner 包）都应该继承这些基类，以确保其行为符合 LangChain 框架的预期。

---

## **1. 核心功能与主要 API**

### **核心功能**
- **接口一致性检查**：验证组件是否正确实现了 `langchain-core` 中定义的抽象方法。
- **行为规范验证**：测试组件在各种边缘情况（如空输入、超长文本、并发调用）下的表现。
- **快照测试支持**：利用 `syrupy` 进行输出快照对比，防止非预期的回归。
- **录制与回放**：集成 `vcrpy`，支持录制真实的 API 交互并在后续测试中回放，减少对真实环境的依赖。

### **主要 API 概览**

| 测试基类 | 适用对象 | 验证内容 |
| :--- | :--- | :--- |
| `ChatModelUnitTests` | `BaseChatModel` 的实现类 | 验证 `invoke`, `stream`, `batch` 等方法的正确性及消息格式转换。 |
| `EmbeddingsUnitTests` | `Embeddings` 的实现类 | 验证 `embed_documents` 和 `embed_query` 的维度及返回格式。 |
| `VectorStoreUnitTests` | `VectorStore` 的实现类 | 验证增删改查（CRUD）逻辑及相似度搜索的准确性。 |
| `ToolUnitTests` | `BaseTool` 的实现类 | 验证工具的输入模式（Schema）及调用逻辑。 |

### **配置参数**
在继承标准测试类时，通常需要通过类属性进行配置：
- `model_class`: 待测试的具体组件类。
- `init_from_env`: 是否从环境变量初始化。
- `has_tool_calling`: (针对 ChatModel) 该模型是否支持工具调用。
- `has_structured_output`: (针对 ChatModel) 该模型是否支持结构化输出。

### **使用示例**

```python
from langchain_tests.unit_chat_models import ChatModelUnitTests
from langchain_openai import ChatOpenAI

class TestOpenAIStandard(ChatModelUnitTests):
    @property
    def chat_model_class(self) -> type[ChatOpenAI]:
        # 指定要测试的类
        return ChatOpenAI

    @property
    def chat_model_params(self) -> dict:
        # 指定初始化参数
        return {"model": "gpt-3.5-turbo"}
```

---

## **2. 整体架构分析**

### **内部模块划分**
- **`unit/`**：单元测试模块，侧重于逻辑和协议的验证，通常会 Mock 掉真实的网络请求。
- **`integration/`**：集成测试模块，侧重于与真实服务或数据库的交互验证。
- **`base.py`**：定义了所有测试基类的通用逻辑。

### **依赖关系**
- **核心依赖**：`langchain-core`（提供接口定义）、`pytest`（测试框架）。
- **工具依赖**：`syrupy`（快照测试）、`vcrpy`（网络录制）、`httpx`（异步 HTTP 客户端）。

### **设计模式**
- **模版方法模式**：基类定义了一系列以 `test_` 开头的测试方法，子类只需提供必要的属性（如 `model_class`）即可运行整套测试流程。
- **多重继承**：支持通过混合（Mixin）类来灵活组合测试能力。

### **数据流转机制**
1. **测试发现**：Pytest 扫描继承了标准测试类的子类。
2. **环境准备**：根据子类提供的参数实例化待测组件。
3. **用例执行**：基类自动运行一系列测试用例（如 `test_invoke_success`, `test_stream_output`）。
4. **断言验证**：基类使用标准断言检查组件输出的类型、结构和内容。
5. **结果上报**：汇总所有标准用例的执行情况。

---

## **3. 注意事项**
- **强制约束**：标准测试不仅仅是建议，它们定义了 LangChain 组件的“最小可行行为”。如果无法通过标准测试，该组件可能无法在复杂的 Chain 或 Agent 中正常工作。
- **网络隔离**：在运行单元测试时，`pytest-socket` 会默认禁用网络，确保测试的纯净性。
- **异步支持**：所有标准测试均原生支持 `asyncio`。
