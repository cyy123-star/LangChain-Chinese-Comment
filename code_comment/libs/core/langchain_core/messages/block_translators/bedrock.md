# [bedrock.py](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/core/langchain_core/messages/block_translators/bedrock.py)

该模块负责将 Amazon Bedrock 平台（特别是通过 Bedrock 调用的 Anthropic Claude 模型）的消息格式转换为 LangChain 标准的 `ContentBlock` 格式。它主要基于 Anthropic 的转换逻辑，并针对 Bedrock 的响应特性（如元数据处理和工具调用同步）进行了适配。

## 导入依赖

| 依赖项 | 来源 | 作用 |
| :--- | :--- | :--- |
| `AIMessage`, `AIMessageChunk` | `langchain_core.messages` | 定义了 AI 消息及其数据块的类型。 |
| `types` | `langchain_core.messages.content` | 包含标准的内容块类型定义。 |
| `_convert_to_v1_from_anthropic` | `langchain_core.messages.block_translators.anthropic` | 复用 Anthropic 的转换逻辑。 |

## 函数详解

### `_convert_to_v1_from_bedrock`

**功能描述**：
将 Bedrock 消息内容转换为 v1 格式。
1. 首先调用 `_convert_to_v1_from_anthropic` 处理基础内容转换。
2. 遍历 `message.tool_calls`，如果某个工具调用在内容块中缺失，则手动补全为 `tool_call` 块。

**参数说明**：
| 参数名 | 类型 | 默认值 | 必填 | 描述 |
| :--- | :--- | :--- | :--- | :--- |
| `message` | `AIMessage` | - | 是 | 需要转换的消息。 |

**返回值解释**：
返回补全后的 `list[types.ContentBlock]` 列表。

---

### `_convert_to_v1_from_bedrock_chunk`

**功能描述**：
处理 Bedrock 消息块（Chunk）的转换。
1. 过滤掉仅包含响应元数据的空数据块。
2. 调用 `_convert_to_v1_from_anthropic` 处理基础块转换。
3. 针对流式输出中的工具调用块进行特殊处理，确保 `tool_call_chunk` 被正确包含。

**参数说明**：
| 参数名 | 类型 | 默认值 | 必填 | 描述 |
| :--- | :--- | :--- | :--- | :--- |
| `message` | `AIMessageChunk` | - | 是 | 需要转换的消息块。 |

**返回值解释**：
返回转换后的内容块列表。

---

### `translate_content` / `translate_content_chunk`

**功能描述**：
导出到翻译器注册中心的公开接口。`translate_content` 会检查 `model_name` 确保是 Claude 模型，否则会抛出 `NotImplementedError` 以触发后备解析逻辑。

**参数说明**：
| 参数名 | 类型 | 默认值 | 必填 | 描述 |
| :--- | :--- | :--- | :--- | :--- |
| `message` | `AIMessage` / `AIMessageChunk` | - | 是 | 待翻译的消息或数据块。 |

---

### `_register_bedrock_translator`

**功能描述**：
将 Bedrock 翻译器注册到全局注册中心。

## 核心逻辑

Bedrock 翻译器的核心在于它对 Anthropic 逻辑的继承。由于 Bedrock 托管的 Claude 模型输出格式与 Anthropic 原生 API 非常接近，代码通过导入 `_convert_to_v1_from_anthropic` 来处理大部分转换工作。

**补全机制**：
在非流式场景下，Bedrock 可能会在 `tool_calls` 字段中提供工具调用，但在 `content` 中未明确体现。`_convert_to_v1_from_bedrock` 会检查两者的一致性，通过 `content_tool_call_ids` 集合识别缺失的调用，并根据 `message.tool_calls` 中的信息重建 `ToolCall` 块，确保下游应用能看到完整的工具使用记录。

## 使用示例

```python
from langchain_core.messages import AIMessage
from langchain_core.messages.block_translators.bedrock import translate_content

# 模拟一个来自 Bedrock 的 Claude 消息
msg = AIMessage(
    content="好的，我来查一下。",
    response_metadata={"model_name": "anthropic.claude-3-sonnet-20240229-v1:0"},
    tool_calls=[{
        "name": "get_weather",
        "args": {"city": "Shanghai"},
        "id": "call_123"
    }]
)

blocks = translate_content(msg)
# 输出将包含文本块和补全的工具调用块
```

## 注意事项

- **模型限制**：当前 `translate_content` 仅显式支持 `claude` 模型。对于 Bedrock 上的其他模型（如 Titan, Llama 等），目前会抛出 `NotImplementedError`。
- **元数据过滤**：Bedrock 经常会发送一些只包含消耗 Token 数等元数据的空块，这些块在转换时会被忽略。

## 内部调用关系

- 依赖于 `anthropic` 翻译模块提供的基础转换能力。
- 注册到 `langchain_core.messages.block_translators` 注册中心。

## 相关链接

- [Amazon Bedrock 官方文档](https://aws.amazon.com/bedrock/)
- [Anthropic Claude 消息格式](https://docs.anthropic.com/claude/reference/messages_post)

---
**最后更新时间**: 2026-01-29
**对应源码版本**: LangChain Core v1.2.7