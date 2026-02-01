# pydantic.py

## 文件概述
`pydantic.py` 模块定义了 `PydanticOutputParser` 类。它是 `JsonOutputParser` 的增强版本，专门用于将模型输出解析为 Pydantic 类的实例。

相比于基础的 JSON 解析，该解析器增加了 **强类型校验**：
- 它不仅检查输出是否为合法的 JSON，还会检查 JSON 内容是否完全符合 Pydantic 模型定义的字段、类型以及约束条件。
- 它是构建生产级、类型安全的应用（如提取特定实体信息）的首选解析器。

---

## 导入依赖
- `json`: 用于 JSON 字符串的处理。
- `pydantic`: 核心校验库（支持 v1 和 v2）。
- `langchain_core.output_parsers`: 继承自 `JsonOutputParser`。
- `langchain_core.exceptions`: 提供了详细的解析异常处理。

---

## 类与函数详解

### 1. `PydanticOutputParser` (类)
使用 Pydantic 模型进行解析和校验的解析器。

#### 属性说明
| 属性名 | 类型 | 默认值 | 是否必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `pydantic_object` | `type[TBaseModel]` | - | 是 | 用于解析和验证的目标 Pydantic 模型类。 |

#### 核心方法
- **`parse` / `parse_result`**:
  - **步骤 1**: 调用父类 `JsonOutputParser` 将文本转换为 Python 字典。
  - **步骤 2**: 调用 `_parse_obj` 使用 Pydantic 模型对字典进行验证并实例化。
  - **异常**: 如果 JSON 格式错误或验证失败（字段缺失、类型不匹配等），抛出包含详细错误的 `OutputParserException`。
- **`get_format_instructions`**:
  - **功能**: 返回详细的 Prompt 指令。它不仅包含 JSON Schema，还包含了一个如何根据 Schema 生成对象的具体示例，以引导模型产生更准确的结果。

---

## 核心逻辑解读

### 1. 跨版本兼容性
`PydanticOutputParser` 内部实现了对 Pydantic v1 和 v2 的兼容处理：
- 对于 v1 模型，使用 `parse_obj`。
- 对于 v2 模型，使用 `model_validate`。
这保证了在不同环境下的稳定性。

### 2. 详细的错误报告
当验证失败时，`_parser_exception` 会捕获 Pydantic 的原始错误，并将其与导致错误的 JSON 字符串一起包装在异常中。这对于调试和设置“自我纠错”链（Self-correction chains）至关重要。

### 3. 类型安全
由于使用了 Python 的泛型（`Generic[TBaseModel]`），在使用 `invoke` 或 `batch` 时，IDE 可以提供准确的类型补全。

---

## 使用示例

### 1. 定义模型并解析
```python
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser

# 1. 定义结构
class Actor(BaseModel):
    name: str = Field(description="演员姓名")
    film_names: list[str] = Field(description="代表作列表")

# 2. 初始化解析器
parser = PydanticOutputParser(pydantic_object=Actor)

# 3. 模拟模型输出
json_text = '{"name": "Tom Hanks", "film_names": ["Forrest Gump", "Cast Away"]}'
actor = parser.parse(json_text)

print(actor.name) # Tom Hanks
print(type(actor)) # <class '__main__.Actor'>
```

---

## 注意事项
- **模型指令的重要性**: 务必将 `parser.get_format_instructions()` 加入到 Prompt 中，否则模型很难生成完全符合 Schema 要求的 JSON。
- **验证失败的处理**: 建议配合 `RetryOutputParser` 或 `OutputFixingParser` 使用，当模型生成的格式有细微偏差时进行自动修复。
- **性能**: 相比纯 JSON 解析，Pydantic 验证会有额外的计算开销，尤其是当模型非常复杂或包含大量嵌套时。

---

## 内部调用关系
- **继承体系**: `PydanticOutputParser` -> `JsonOutputParser` -> `BaseOutputParser`。
- **依赖工具**: 依赖 `langchain_core.utils.pydantic` 进行模型识别。

---

## 相关链接
- [LangChain 官方文档 - Pydantic 解析器](https://python.langchain.com/docs/modules/model_io/output_parsers/types/pydantic/)
- [Pydantic 官方文档](https://docs.pydantic.dev/)

---
**对应源码版本**: LangChain Core v1.2.7
**最后更新时间**: 2026-01-29
