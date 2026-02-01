# libs\langchain_v1\langchain\agents\structured_output.py

`structured_output.py` 模块定义了代理如何生成结构化输出（如 JSON 或 Pydantic 对象）的策略和异常处理机制。

## 核心策略 (`ResponseFormat`)

代理支持多种结构化输出策略，通过不同的子类实现：

### 1. `ToolStrategy`
使用模型的 **工具调用 (Tool Calling)** 能力来实现结构化输出。
- **原理**: 代理会自动创建一个隐藏的工具，其参数 Schema 即为要求的输出格式。当模型调用该工具时，其参数被解析为最终结果。
- **适用场景**: 适用于支持工具调用的模型（如 GPT-4, Claude 3, Gemini 1.5）。
- **错误处理**: 支持通过 `handle_errors` 参数配置重试逻辑。如果解析失败，会将错误信息发回模型进行修正。

### 2. `ProviderStrategy`
使用模型供应商提供的 **原生结构化输出** 接口（如 OpenAI 的 `response_format={"type": "json_schema", ...}`）。
- **原理**: 直接调用供应商的 API 参数来强制模型按 Schema 输出。
- **适用场景**: 仅适用于支持原生结构化输出的供应商和模型。
- **优点**: 通常比工具调用更严格，延迟更低。

### 3. `AutoStrategy`
**自动选择策略**。根据所选模型的供应商和能力，自动在 `ToolStrategy` 和 `ProviderStrategy` 之间切换。

## 异常处理

模块定义了专门的异常类来处理结构化输出过程中的各种错误：

| 异常类 | 描述 |
| :--- | :--- |
| `StructuredOutputError` | 结构化输出异常的基类。包含导致错误的 `ai_message`。 |
| `MultipleStructuredOutputsError` | 当预期只有一个结构化输出，但模型返回了多个工具调用时触发。 |
| `StructuredOutputValidationError` | 当模型返回的数据无法通过 Schema 验证（如 Pydantic 验证失败）时触发。 |

## 辅助组件

### `_SchemaSpec`
内部使用的 Schema 描述类，负责将 Pydantic 模型、Dataclass、TypedDict 或 JSON Schema 统一转换为代理可识别的格式，并提取名称和描述。

## 使用示例

```python
from pydantic import BaseModel
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy

class SearchResponse(BaseModel):
    answer: str
    sources: list[str]

# 使用 ToolStrategy 强制输出 SearchResponse 格式
agent = create_agent(
    model="gpt-4o",
    tools=[...],
    response_format=SearchResponse # 内部会自动转换为 AutoStrategy 或 ToolStrategy
)
```

## 注意事项
- **模型支持**: 并非所有模型都支持结构化输出。如果模型不支持，代理可能会退化为普通的文本输出，或者在初始化时报错。
- **严格模式 (`strict`)**: 对于支持 OpenAI `strict` 模式的模型，`ProviderStrategy` 会尽量利用该特性以确保 100% 的 Schema 遵从性。
