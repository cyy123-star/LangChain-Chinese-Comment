# JSON 实用工具模块文档

## 文件概述
`json.py` 是 LangChain 中处理 JSON 数据的核心实用工具模块。它不仅提供了标准的 JSON 解析功能，还专门针对 LLM 输出中常见的“不完整 JSON”、“Markdown 格式嵌套 JSON”以及“包含未转义换行符的 JSON”等异常情况提供了强大的鲁棒性解析方案。

## 导入依赖
- `json`: 标准 JSON 处理库。
- `re`: 正则表达式库，用于处理 Markdown 提取和字符串预处理。
- `langchain_core.exceptions`: 引入 `OutputParserException` 用于报告解析错误。

---

## 核心函数详解

### 1. parse_partial_json
**功能描述**: 解析可能不完整的 JSON 字符串。当 LLM 的输出被截断或流式输出尚未完成时，该函数会尝试自动补全缺失的闭合括号（`}` 或 `]`）并修复常见的转义错误。
- **参数说明**:
    | 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
    | :--- | :--- | :--- | :--- | :--- |
    | `s` | `str` | - | 是 | 待解析的 JSON 字符串。 |
    | `strict` | `bool` | `False` | 否 | 是否使用严格解析模式。 |
- **核心逻辑**:
    1. 尝试直接解析。
    2. 若失败，扫描字符串，使用栈（Stack）记录未闭合的结构。
    3. 处理字符串内部的换行符和转义符。
    4. 自动补全后缀，并从后往前尝试截断解析，直到成功或字符耗尽。

### 2. parse_json_markdown
**功能描述**: 从 Markdown 文本中提取并解析 JSON 块。它能够识别 ```json ... ``` 包裹的内容。
- **参数说明**:
    | 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
    | :--- | :--- | :--- | :--- | :--- |
    | `json_string` | `str` | - | 是 | 包含 JSON 的 Markdown 字符串。 |
    | `parser` | `Callable` | `parse_partial_json` | 否 | 底层使用的 JSON 解析函数。 |
- **返回值**: `Any` - 解析后的 Python 字典或列表。

### 3. parse_and_check_json_markdown
**功能描述**: 在解析 Markdown JSON 的基础上，进一步检查结果是否包含预期的键。
- **参数说明**:
    | 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
    | :--- | :--- | :--- | :--- | :--- |
    | `text` | `str` | - | 是 | 原始文本。 |
    | `expected_keys` | `list[str]` | - | 是 | 结果中必须包含的键名列表。 |
- **异常抛出**: `OutputParserException` - 如果 JSON 格式错误、不是字典或缺少必需键。

---

## 辅助逻辑详解

### `_custom_parser`
针对 LLM 在 `action_input` 字段中经常输出未转义换行符的问题进行专项修复。它会查找特定的模式并手动将 `\n` 替换为 `\\n`，以符合 JSON 规范。

---

## 使用示例

### 1. 解析不完整的 JSON
```python
from langchain_core.utils.json import parse_partial_json

partial_json = '{"name": "LangChain", "features": ["LLM", "Chain"'
# 自动补全为 {"name": "LangChain", "features": ["LLM", "Chain"]}
result = parse_partial_json(partial_json)
print(result)
```

### 2. 从 Markdown 中提取 JSON
```python
from langchain_core.utils.json import parse_json_markdown

md_text = """
这是模型返回的答案：
```json
{"answer": "42"}
```
"""
result = parse_json_markdown(md_text)
print(result["answer"]) # 输出: 42
```

## 注意事项
- **鲁棒性 vs. 准确性**: 虽然 `parse_partial_json` 尽力修复错误，但在输入极度混乱的情况下，返回的结果可能与模型原始意图有偏差。
- **性能**: 对于非常大的、严重损坏的字符串，递归尝试解析可能会有一定的计算开销。
- **换行符**: JSON 标准要求字符串内部的换行符必须转义。该模块会自动处理这些常见的 LLM 错误。

## 相关链接
- [JSON 标准 (RFC 8259)](https://datatracker.ietf.org/doc/html/rfc8259)
- [Open Interpreter 解析逻辑参考](https://github.com/KillianLucas/open-interpreter)

---
**最后更新时间**: 2026-01-29
**对应源码版本**: LangChain Core v1.2.7
