# google_genai.py - Google GenAI 内容块转换器

## 文件概述

`google_genai.py` 专门负责将 Google AI (GenAI/Gemini) 模型特定的内容格式转换为 LangChain 标准的 `v1` 内容块格式。

Google Gemini 模型支持丰富的多模态能力，包括文本、图片、音频、文件、代码执行（Code Execution）以及搜索结果引文（Grounding Metadata）。该转换器确保这些复杂的输出能够被标准化为 LangChain 的统一表示，方便在不同模型和组件之间保持一致的开发体验。

## 导入依赖

| 模块 | 作用 |
| :--- | :--- |
| `base64` | 用于将字节数据编码为 Base64 字符串。 |
| `re` | 用于解析 Data URI（如 `data:image/png;base64,...`）。 |
| `filetype` | （可选）用于根据字节流猜测文件的 MIME 类型。 |
| `langchain_core.messages` | 导入 `AIMessage`, `AIMessageChunk` 等核心消息类。 |
| `langchain_core.messages.content` | 导入标准内容块类型定义（`Citation`, `ContentBlock` 等）。 |

## 核心函数详解

### 1. translate_grounding_metadata_to_citations
- **功能描述**: 将 Google AI 的接地元数据（Grounding Metadata）转换为 LangChain 的标准 `Citation` 内容块。
- **核心逻辑**:
    - 解析 `web_search_queries`（搜索查询）。
    - 遍历 `grounding_supports`，结合 `grounding_chunks` 提取引用的 URL、标题和原文片段。
    - 包含 Gemini 2.0+ 的置信度分数（虽然在更高版本中可能为空）。

### 2. _convert_to_v1_from_genai
- **功能描述**: `google_genai` 到 `v1` 格式的核心转换逻辑。
- **处理类型**:
    - **文本 (Text)**: 转换为标准文本块，并附加引文。
    - **图片 (Image)**: 支持 Data URI 解析或原始 Base64 数据，自动检测 MIME 类型。
    - **文件 (File)**: 处理 `file_data` (URI) 或 Base64 格式的文件（如 PDF, TXT）。
    - **音频 (Audio)**: 将二进制音频数据转换为 Base64。
    - **思维链 (Thinking)**: 转换为 `reasoning` 块，保留模型思考过程。
    - **工具调用 (Tool Call)**: 将 Google 的 `function_call` 映射为标准 `tool_call`。
    - **代码执行 (Code Execution)**: 将 `executable_code` 映射为 `code_interpreter` 的 `server_tool_call`。
    - **执行结果**: 将 `code_execution_result` 转换为 `server_tool_result`。

### 3. translate_content / translate_content_chunk
- **功能描述**: 导出到翻译器注册中心的公开接口，分别处理完整消息和消息块。

## 内部调用关系

- **注册机制**: 模块加载时会自动注册为 `"google_genai"` 转换器。
- **递归转换**: 针对复杂的内容列表，递归处理每个元素并进行类型映射。
- **错误处理**: 对于无法识别的块类型，将其包装为 `non_standard` 块以避免数据丢失。

## 使用示例

通常该转换器由 LangChain 内部集成，以下为模拟转换逻辑的示例：

```python
from langchain_core.messages import AIMessage
from langchain_core.messages.block_translators.google_genai import translate_content

# 模拟 Google GenAI 格式的消息（包含代码执行结果）
google_msg = AIMessage(
    content=[
        {"type": "text", "text": "计算结果是 42。"},
        {
            "type": "code_execution_result",
            "tool_call_id": "exec_1",
            "outcome": 1,
            "code_execution_result": "42"
        }
    ]
)

# 转换为标准格式
standard_blocks = translate_content(google_msg)
for block in standard_blocks:
    print(f"类型: {block['type']}, 状态: {block.get('status', 'N/A')}")
```

## 注意事项

- **MIME 类型检测**: 如果环境中未安装 `filetype` 库，对于没有明确提供 MIME 类型的 Base64 数据，系统可能无法准确标记。
- **引文位置**: 引文通常被附加到消息中的第一个文本块上。
- **安全性**: 处理本地文件路径时需谨慎，该转换器主要处理已加载的数据。

## 相关链接

- [google_vertexai.py](./google_vertexai.md)
- [anthropic.py](./anthropic.md)

---
最后更新时间: 2026-01-29
对应源码版本: LangChain Core v1.2.7
