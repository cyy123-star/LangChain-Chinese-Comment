# format_instructions.py

## 文件概述
`format_instructions.py` 定义了 LangChain 框架中用于指导模型生成特定格式输出（如 JSON）的标准提示词模板。这些指令确保模型能够按照预期的结构和约束返回结果，以便后续的解析器（如 `JsonOutputParser`）能够准确处理。

## 导入依赖
该文件目前不依赖外部模块，仅定义常量字符串。

## 类与函数详解
该文件主要定义了以下常量：

### 1. JSON_FORMAT_INSTRUCTIONS
**功能描述**: 提供给大语言模型（LLM）的标准 JSON 格式生成指令。它通过详细的规则和示例，强制要求模型返回纯净的、符合特定 JSON Schema 的结果。

#### 核心指令内容
- **严格格式要求**:
    - 仅返回符合 Schema 的 JSON 值。
    - 不包含额外的解释文本、标题或分隔符。
    - 不使用 Markdown 代码块（即不包含 ``` 或 ```json）。
    - 响应必须是单个顶层 JSON 值。
- **示例引导**:
    - 通过具体示例（如 properties, items 等）说明正确的 JSON 实例与错误的嵌套结构的对比。
- **Schema 占位符**:
    - 使用 `{schema}` 占位符，在实际使用时会被动态替换为具体的 JSON Schema 定义。

## 使用示例
虽然该文件仅定义字符串，但它通常由 `JsonOutputParser` 等解析器内部使用：

```python
from langchain_core.output_parsers.format_instructions import JSON_FORMAT_INSTRUCTIONS

# 模拟 JsonOutputParser 的内部使用
schema_definition = '{"properties": {"name": {"type": "string"}}, "required": ["name"]}'
instructions = JSON_FORMAT_INSTRUCTIONS.format(schema=schema_definition)

print(instructions)
```

## 注意事项
- **提示词敏感性**: 修改这些指令可能会直接影响模型的输出质量和解析成功率。
- **No Markdown**: 明确要求模型不要返回 Markdown 代码块，这是为了简化解析逻辑并减少冗余字符。
- **单值要求**: 要求模型返回单个顶层 JSON 值，避免多重嵌套导致的解析复杂性。

## 内部调用关系
- **被调用**: 主要被 `langchain_core.output_parsers.json.JsonOutputParser` 及其子类调用，用于生成 `get_format_instructions()` 的返回值。

## 相关链接
- [JSON Schema 官方标准](https://json-schema.org/)
- [LangChain JSON 解析器指南](https://python.langchain.com/docs/how_to/output_parser_json/)

---
最后更新时间: 2026-01-29
对应源码版本: LangChain Core v1.2.7
