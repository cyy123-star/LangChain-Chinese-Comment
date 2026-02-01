# Embeddings 基础 (Base)

`embeddings.base` 模块提供了 LangChain v1 中推荐的嵌入模型初始化方式。其核心是 `init_embeddings` 工厂函数，旨在为开发者提供一个统一、简洁的接口来实例化不同提供商的文本嵌入模型。

## 核心功能

### 1. `init_embeddings` 工厂函数
该函数是嵌入模型实例化的标准入口。它支持通过单一字符串或显式参数指定提供商和模型。

#### 参数说明
| 参数 | 类型 | 描述 |
| :--- | :--- | :--- |
| `model` | `str` | 模型名称。支持 `provider:model` 格式（如 `openai:text-embedding-3-small`）。**必填**。 |
| `provider` | `str \| None` | 显式指定提供商。如果 `model` 参数不包含冒号，则必须提供此参数。 |
| `**kwargs` | `Any` | 传递给底层嵌入类构造函数的额外参数（如 `api_key`, `base_url`, `dimensions` 等）。 |

#### 支持的提供商
| 提供商 ID | 对应的类 | 所需集成包 |
| :--- | :--- | :--- |
| `openai` | `OpenAIEmbeddings` | `langchain-openai` |
| `azure_openai` | `AzureOpenAIEmbeddings` | `langchain-openai` |
| `bedrock` | `BedrockEmbeddings` | `langchain-aws` |
| `cohere` | `CohereEmbeddings` | `langchain-cohere` |
| `google_genai` | `GoogleGenerativeAIEmbeddings` | `langchain-google-genai` |
| `google_vertexai` | `VertexAIEmbeddings` | `langchain-google-vertexai` |
| `huggingface` | `HuggingFaceEmbeddings` | `langchain-huggingface` |
| `mistralai` | `MistralAIEmbeddings` | `langchain-mistralai` |
| `ollama` | `OllamaEmbeddings` | `langchain-ollama` |

### 2. 解析逻辑
- **格式校验**: `model` 字符串通常应遵循 `provider:model-name` 格式。
- **推断机制**: 如果提供了 `provider` 参数，则 `model` 被视为纯模型名；否则，系统会解析 `model` 字符串中的冒号前缀作为提供商。
- **延迟加载**: 只有在调用 `init_embeddings` 时，才会根据需要动态导入对应的集成模块（如 `import langchain_openai`），从而减少了不必要的依赖开销。

## 代码参考
- [init_embeddings](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/langchain_v1/langchain/embeddings/base.py#L178): 核心工厂函数实现。
- [_SUPPORTED_PROVIDERS](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/langchain_v1/langchain/embeddings/base.py#L15): 提供商配置注册表。

## 使用示例

### 1. 使用模型字符串初始化 (推荐)
```python
from langchain.embeddings import init_embeddings

# 格式为 provider:model
model = init_embeddings("openai:text-embedding-3-small")
vector = model.embed_query("什么是向量数据库？")
```

### 2. 显式指定提供商
```python
# 适用于模型名不包含冒号的情况
model = init_embeddings(model="text-embedding-ada-002", provider="openai")
```

### 3. 传递额外参数
```python
# 例如指定嵌入维度
model = init_embeddings(
    "openai:text-embedding-3-small", 
    dimensions=512,
    api_key="your-api-key"
)
```
