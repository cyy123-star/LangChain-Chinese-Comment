# [bedrock_converse.py](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/core/langchain_core/messages/block_translators/bedrock_converse.py)

该模块负责将 Amazon Bedrock Converse API 的消息格式转换为 LangChain 标准的 `ContentBlock` 格式。Bedrock Converse 是 AWS 提供的一种统一的消息接口，支持文本、文档（如 PDF）、图像以及推理内容（Reasoning）和引文（Citations）。

## 导入依赖

| 依赖项 | 来源 | 作用 |
| :--- | :--- | :--- |
| `base64` | 标准库 | 用于将 Bedrock 返回的二进制数据转换为 base64 字符串。 |
| `AIMessage`, `AIMessageChunk` | `langchain_core.messages` | 定义了 AI 消息及其数据块的类型。 |
| `types` | `langchain_core.messages.content` | 包含标准的内容块类型定义。 |

## 函数详解

### `_bytes_to_b64_str`

**功能描述**：
实用工具函数，将字节数据转换为 UTF-8 编码的 Base64 字符串。

---

### `_convert_to_v1_from_converse_input`

**功能描述**：
将 Bedrock Converse 格式的输入块转换为 v1 格式。它会解包标记为 `non_standard` 的块，并尝试识别以下类型：
- **文本**：直接映射。
- **文档**：支持 `pdf`（映射为 `file`）和 `txt`（映射为 `text-plain`）。
- **图像**：根据格式映射为 `image` 块，并转换字节为 Base64。

**参数说明**：
| 参数名 | 类型 | 默认值 | 必填 | 描述 |
| :--- | :--- | :--- | :--- | :--- |
| `content` | `list[types.ContentBlock]` | - | 是 | 需要处理的内容块列表。 |

---

### `_convert_citation_to_v1`

**功能描述**：
将 Bedrock Converse 的引文格式转换为标准的 `Citation` 结构。它会合并 `source_content` 中的所有文本片段作为 `cited_text`。

---

### `_convert_to_v1_from_converse`

**功能描述**：
Bedrock Converse 到 v1 格式的核心转换函数。处理以下核心逻辑：
1. **文本与引文**：处理带有 `citations` 数组的文本块。
2. **推理内容**：转换 `reasoning_content`（如模型的思考过程、签名等）。
3. **工具使用**：处理 `tool_use` 块。如果是流式块且包含工具调用片段，则转换为 `tool_call_chunk`；否则转换为完整的 `tool_call`。
4. **工具增量**：处理流式输出中的 `input_json_delta`。

**参数说明**：
| 参数名 | 类型 | 默认值 | 必填 | 描述 |
| :--- | :--- | :--- | :--- | :--- |
| `message` | `AIMessage` / `AIMessageChunk` | - | 是 | 需要转换的消息对象。 |

---

### `translate_content` / `translate_content_chunk`

**功能描述**：
导出到翻译器注册中心的公开接口。

## 核心逻辑

Bedrock Converse API 的输出结构较为复杂，尤其是它对多模态和推理内容的支持。

**多模态处理**：
对于文档和图像，Bedrock 返回的是原始字节。本模块负责识别这些多媒体块，并将其封装为 LangChain 标准的格式，同时包含正确的 MIME 类型。

**推理内容 (Reasoning)**：
Bedrock 支持输出模型的“思考过程”。代码将其映射为 `type="reasoning"` 的块，并保留了 `signature` 等元数据。

**工具调用 (Tool Use)**：
Bedrock Converse 的工具调用块名为 `tool_use`。在流式传输中，它可能以 `tool_use` 开始，后续跟着 `input_json_delta`。本模块能够识别这些不同的片段，并根据当前消息是 `AIMessage`（已聚合）还是 `AIMessageChunk`（流式）来决定输出 `tool_call` 还是 `tool_call_chunk`。

## 使用示例

```python
from langchain_core.messages import AIMessage
from langchain_core.messages.block_translators.bedrock_converse import translate_content

# 模拟一个带有引文和推理的 Bedrock Converse 响应
msg = AIMessage(
    content=[
        {
            "type": "reasoning_content",
            "reasoning_content": {"text": "我应该根据文档回答这个问题..."}
        },
        {
            "type": "text",
            "text": "根据资料，LangChain 是...",
            "citations": [
                {
                    "source_content": [{"text": "LangChain 简介..."}],
                    "title": "文档 A"
                }
            ]
        }
    ]
)

blocks = translate_content(msg)
```

## 注意事项

- **Base64 转换**：所有二进制数据（图像、PDF）都会在内存中转换为 Base64 字符串，处理大文件时需注意内存消耗。
- **非标准块**：无法识别的块会被包装为 `type="non_standard"`，其原始值存储在 `value` 字段中，以保证数据不丢失。

## 内部调用关系

- 使用 `_populate_extras` 处理供应商特有的额外字段。
- 注册到 `langchain_core.messages.block_translators` 注册中心，键名为 `"bedrock_converse"`。

## 相关链接

- [AWS Bedrock Converse API 参考](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html)

---
**最后更新时间**: 2026-01-29
**对应源码版本**: LangChain Core v1.2.7