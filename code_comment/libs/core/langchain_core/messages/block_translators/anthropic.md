# anthropic.py - Anthropic 内容块转换器

## 文件概述

`anthropic.py` 是 LangChain 消息内容转换系统的一部分，专门用于将 Anthropic 模型特定的内容格式（Content Blocks）转换为 LangChain 标准的 `v1` 内容块格式。

随着大语言模型（LLM）能力的增强，它们返回的内容不再仅仅是纯文本，还包括多模态数据（图片、文件）、思维链（Thinking）、工具调用（Tool Use）以及服务端工具结果。该文件通过一系列转换函数，确保 Anthropic 模型的异构输出能够以统一的方式在 LangChain 框架内流转。

## 导入依赖

| 模块 | 作用 |
| :--- | :--- |
| `json` | 用于处理部分工具调用参数的 JSON 解析。 |
| `collections.abc.Iterable` | 用于定义块迭代器的返回类型。 |
| `typing` | 提供类型注解支持（`Any`, `cast`, `list` 等）。 |
| `langchain_core.messages` | 导入 `AIMessage`, `AIMessageChunk` 等核心消息类。 |
| `langchain_core.messages.content` | 导入标准内容块类型定义（别名为 `types`）。 |

## 核心函数详解

### 1. translate_content
- **功能描述**: 将包含 Anthropic 内容的 `AIMessage` 转换为标准的 `ContentBlock` 列表。
- **参数说明**:
    | 参数名 | 类型 | 默认值 | 必填 | 描述 |
    | :--- | :--- | :--- | :--- | :--- |
    | `message` | `AIMessage` | - | 是 | 待转换的 Anthropic AI 消息。 |
- **返回值**: `list[ContentBlock]`。转换后的标准内容块列表。

### 2. translate_content_chunk
- **功能描述**: 将包含 Anthropic 内容的 `AIMessageChunk`（流式消息块）转换为标准的 `ContentBlock` 列表。
- **参数说明**:
    | 参数名 | 类型 | 默认值 | 必填 | 描述 |
    | :--- | :--- | :--- | :--- | :--- |
    | `message` | `AIMessageChunk` | - | 是 | 待转换的 Anthropic AI 消息块。 |

### 3. _convert_to_v1_from_anthropic (核心逻辑)
该函数负责实际的转换逻辑，处理以下类型的 Anthropic 块：
- **text**: 转换为标准文本块，支持引文（Citations/Annotations）。
- **thinking**: 转换为 `reasoning`（推理）内容块，保留思维过程。
- **tool_use**: 转换为 `tool_call`（工具调用）块。支持流式和非流式场景。
- **input_json_delta**: 处理流式输出中的工具参数增量。
- **server_tool_use**: 处理 Anthropic 内部工具（如代码执行 `code_execution`），映射为 `server_tool_call`。
- **mcp_tool_use**: 处理 MCP（Model Context Protocol）工具。
- **tool_result**: 将工具执行结果转换为 `server_tool_result`。

### 4. _convert_citation_to_v1
- **功能描述**: 将 Anthropic 的引文（Citation）格式转换为 LangChain 的标准 `Annotation` 格式。
- **支持类型**: 网页搜索结果、文档位置、字符位置等。

### 5. _populate_extras
- **功能描述**: 将 Anthropic 原始块中不属于标准字段的其他属性提取并存储到 `extras` 字典中，确保信息不丢失。

## 内部调用关系

- **注册机制**: 模块加载时会自动调用 `_register_anthropic_translator()`，将自身注册到全局转换器注册表（Registry）中，键名为 `"anthropic"`。
- **核心流**: 外部系统（如 `ChatAnthropic`）调用 `translate_content` -> 内部调用 `_convert_to_v1_from_anthropic` -> 针对每个块调用具体的子转换函数（如 `_convert_citation_to_v1`）。

## 使用示例

通常该转换器由 LangChain 内部集成，用户不需要手动调用。以下为模拟内部调用的示例：

```python
from langchain_core.messages import AIMessage
from langchain_core.messages.block_translators.anthropic import translate_content

# 模拟 Anthropic 格式的消息
anthropic_msg = AIMessage(
    content=[
        {"type": "text", "text": "Here is the code."},
        {"type": "thinking", "thinking": "The user wants a python script."},
        {"type": "tool_use", "id": "t1", "name": "python_interpreter", "input": {"code": "print(1)"}}
    ]
)

# 转换为标准格式
standard_blocks = translate_content(anthropic_msg)
for block in standard_blocks:
    print(f"Type: {block['type']}, Content: {block}")
```

## 注意事项

- **非标准块处理**: 对于无法识别的 Anthropic 块，会将其包装为 `type: "non_standard"`，并将原始数据保存在 `value` 字段中。
- **流式支持**: 针对 `AIMessageChunk` 进行了特殊处理，能够正确处理工具调用的中间状态（增量参数）。
- **字段映射**: 例如将 Anthropic 的 `code_execution` 自动映射为更通用的 `code_interpreter`。

## 相关链接

- [langchain_v0.py](./langchain_v0.md)
- [openai.py](./openai.md)

---
最后更新时间: 2026-01-29
对应源码版本: LangChain Core v1.2.7
