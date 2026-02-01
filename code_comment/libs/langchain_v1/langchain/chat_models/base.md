# Chat Models 基础 (Base)

`chat_models.base` 模块定义了 LangChain v1 中推荐的模型初始化机制。其核心是 `init_chat_model` 工厂函数，它提供了一个统一的接口来实例化不同提供商的聊天模型，并支持强大的运行时可配置性。

## 核心功能

### 1. `init_chat_model` 工厂函数
这是模型初始化的主要入口。它支持两种模式：
- **固定模型模式**: 直接返回指定提供商的模型实例。
- **可配置模型模式**: 返回一个 `_ConfigurableModel` 代理对象，允许在调用 `invoke` 时通过 `config` 动态决定模型、提供商及其他参数。

#### 参数说明
| 参数 | 类型 | 描述 |
| :--- | :--- | :--- |
| `model` | `str \| None` | 模型名称。支持 `provider:model` 格式（如 `openai:gpt-4o`）。如果未指定，则默认为可配置模式。 |
| `model_provider` | `str \| None` | 模型提供商。如果 `model` 中未包含且未指定此参数，将尝试从 `model` 名称推断。 |
| `configurable_fields` | `Literal["any"] \| list[str] \| None` | 运行时可配置的字段。`"any"` 表示所有字段均可配置（注意安全）；`None` 表示固定模型。 |
| `config_prefix` | `str \| None` | 运行时配置键的前缀，用于区分多个模型配置。 |
| `**kwargs` | `Any` | 传递给底层模型 `__init__` 方法的默认参数（如 `temperature`, `max_tokens`, `api_key` 等）。 |

### 2. 模型提供商推断
当不显式指定 `model_provider` 时，系统会根据模型名称前缀自动推断：
- `gpt-...`, `o1...`, `o3...` -> `openai`
- `claude...` -> `anthropic`
- `gemini...` -> `google_vertexai`
- `command...` -> `cohere`
- `mistral...`, `mixtral...` -> `mistralai`
- `deepseek...` -> `deepseek`
- `amazon...` -> `bedrock`
- `solar...` -> `upstage`
- `sonar...` -> `perplexity`

### 3. `_ConfigurableModel` (可配置代理)
当开启可配置模式时，返回此对象。它实现了 `Runnable` 接口，具有以下特性：
- **延迟加载**: 仅在真正调用 `invoke` 或 `stream` 时，才根据合并后的配置实例化真实的模型对象。
- **操作队列 (`queued_declarative_operations`)**: 支持在代理对象上预先调用 `bind_tools` 或 `with_structured_output`。这些操作会被记录并应用到最终生成的模型实例上。
- **运行时覆盖**: 通过 `config={"configurable": {"model": "...", "temperature": ...}}` 动态修改模型行为。

## 安全警告
⚠️ **不要对不受信任的配置使用 `configurable_fields="any"`**。
这允许调用者在运行时修改 `api_key` 或 `base_url`，可能导致请求被重定向到恶意服务。对于多租户或暴露 API 的应用，请务必显式列出允许配置的字段，例如 `configurable_fields=("model", "temperature")`。

## 代码参考
- [init_chat_model](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/langchain_v1/langchain/chat_models/base.py#L194): 核心工厂函数实现。
- [_ConfigurableModel](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/langchain_v1/langchain/chat_models/base.py#L584): 动态配置代理类实现。
- [_SUPPORTED_PROVIDERS](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/langchain_v1/langchain/chat_models/base.py#L38): 支持的提供商注册表。

## 使用示例

### 1. 固定模型初始化
```python
from langchain.chat_models import init_chat_model

# 自动推断提供商为 openai
model = init_chat_model("gpt-4o", temperature=0)
response = model.invoke("你好")
```

### 2. 运行时动态切换模型
```python
# 初始化时不指定模型，开启可配置
model = init_chat_model(temperature=0)

# 调用时指定为 OpenAI
res1 = model.invoke("Hi", config={"configurable": {"model": "openai:gpt-4o"}})

# 调用时指定为 Anthropic
res2 = model.invoke("Hi", config={"configurable": {"model": "anthropic:claude-3-5-sonnet-20240620"}})
```

### 3. 带前缀的多模型配置
```python
model = init_chat_model("gpt-4o", config_prefix="assistant_a")

# 通过前缀覆盖特定模型的参数
model.invoke("Hi", config={"configurable": {"assistant_a_temperature": 0.8}})
```
