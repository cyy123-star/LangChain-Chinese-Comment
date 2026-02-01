# json.py

## 文件概述
`json.py` 模块定义了 `JsonOutputParser` 类，它是 LangChain 中最常用且最可靠的输出解析器之一。该解析器的主要职责是将语言模型生成的文本（通常包含在 Markdown JSON 代码块中）解析为 Python 字典或列表。

与简单的字符串解析不同，它支持：
1. **Markdown 提取**：自动从 ` ```json ` 块中提取内容。
2. **流式部分解析**：在模型还在生成时，实时解析并返回已完成的 JSON 部分。
3. **Pydantic 验证**：支持关联 Pydantic 模型，自动生成符合 Schema 的格式指令。

---

## 导入依赖
- `json`: 用于标准 JSON 解析和序列化。
- `pydantic`: 支持数据模型验证（兼容 v1 和 v2）。
- `jsonpatch`: 用于流式输出时计算 JSON 补丁（Diff）。
- `langchain_core.utils.json`: 提供了核心的 Markdown JSON 解析工具函数（如 `parse_json_markdown`）。

---

## 类与函数详解

### 1. `JsonOutputParser` (类)
将 LLM 输出解析为 JSON 对象的解析器。

#### 属性说明
| 属性名 | 类型 | 默认值 | 是否必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `pydantic_object` | `type[BaseModel] \| None` | `None` | 否 | 用于验证的 Pydantic 模型类。如果提供，解析器将根据其生成 Schema 指令。 |

#### 核心方法
- **`parse` / `parse_result`**:
  - **功能**: 执行核心解析逻辑。它会清理文本两端的空白，并尝试提取 JSON 内容。
  - **异常**: 如果文本不是有效的 JSON 格式，抛出 `OutputParserException`。
- **`get_format_instructions`**:
  - **功能**: 生成提示语，告知模型应该返回何种结构的 JSON。如果绑定了 `pydantic_object`，则会包含精简后的 JSON Schema。
- **`stream` (继承自基类)**:
  - **功能**: 支持流式解析。它利用 `parse_partial_json` 在 JSON 尚未闭合时尝试解析已有的键值对。

---

## 核心逻辑解读

### 1. Markdown 健壮性
该解析器并不直接调用 `json.loads`，而是使用 `parse_json_markdown`。这意味着即使模型返回了类似下面的内容，它也能正确工作：
> 好的，这是你要的结果：
> ```json
> {"name": "Alice"}
> ```

### 2. 流式部分解析 (Incremental Parsing)
这是 `JsonOutputParser` 的杀手锏。在流式传输模式下，它能产生中间结果。例如：
- 文本：`{"a": 1, "b":` -> 输出：`{"a": 1}`
- 文本：`{"a": 1, "b": 2}` -> 输出：`{"a": 1, "b": 2}`

### 3. JSON Patch 支持
如果开启了 `diff=True`，解析器不会返回完整的对象，而是返回 `jsonpatch` 格式的操作指令，这在需要精确观察对象变化细节的场景中非常有用。

---

## 使用示例

### 1. 基础用法
```python
from langchain_core.output_parsers import JsonOutputParser

parser = JsonOutputParser()
result = parser.parse('```json\n{"answer": "42"}\n```')
print(result) # {'answer': '42'}
```

### 2. 结合 Pydantic 验证
```python
from pydantic import BaseModel, Field

class User(BaseModel):
    name: str = Field(description="用户姓名")
    age: int = Field(description="用户年龄")

parser = JsonOutputParser(pydantic_object=User)
# 获取自动生成的指令
print(parser.get_format_instructions())
```

---

## 注意事项
- **非 JSON 文本**: 如果模型在 JSON 块之外返回了大量干扰文本，解析器可能会失败。建议配合明确的 `format_instructions` 使用。
- **性能**: 部分解析涉及频繁的正则匹配和尝试性解析，对于极大的 JSON 对象，流式解析可能会有一定的计算开销。
- **版本兼容**: 同时支持 Pydantic v1 和 v2，但在内部会统一处理 Schema 获取逻辑。

---

## 内部调用关系
- **继承体系**: `JsonOutputParser` -> `BaseCumulativeTransformOutputParser` -> `BaseOutputParser`。
- **工具依赖**: 严重依赖 `langchain_core.utils.json` 中的解析算法。

---

## 相关链接
- [LangChain 官方文档 - JSON 解析器](https://python.langchain.com/docs/modules/model_io/output_parsers/types/json/)
- [Pydantic 官方文档](https://docs.pydantic.dev/)

---
**对应源码版本**: LangChain Core v1.2.7
**最后更新时间**: 2026-01-29
