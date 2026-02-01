# LangChain 提示词模板基类 (Base Prompt Template) 规范

## 文件概述

`base.py` 定义了 LangChain 提示词模板系统的核心抽象基类 `BasePromptTemplate`。提示词模板是连接用户输入与大语言模型（LLM）的关键桥梁，负责将结构化数据（通常是字典）转换为模型可理解的提示词值（`PromptValue`）。

该文件不仅定义了模板的基本接口，还实现了输入验证、部分变量填充（Partialing）、序列化、持久化以及与 LangChain 表达式语言（LCEL）的深度集成。

---

## 导入依赖

| 模块 | 作用 |
| :--- | :--- |
| `abc` | 提供抽象基类支持（`ABC`, `abstractmethod`）。 |
| `pydantic` | 用于数据校验、配置管理及模型定义。 |
| `langchain_core.runnables` | 继承 `RunnableSerializable`，使提示词模板具备可调用性和可序列化性。 |
| `langchain_core.prompt_values` | 定义模板生成的最终输出类型（如 `StringPromptValue`, `ChatPromptValue`）。 |
| `langchain_core.load` | 提供序列化工具 `dumpd`。 |

---

## 类与函数详解

### 1. BasePromptTemplate
**功能描述**: 所有提示词模板的抽象基类。它将输入映射（字典）转换为 `PromptValue`。

| 字段名 | 类型 | 默认值 | 必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `input_variables` | `list[str]` | - | 是 | 模板所需的变量名列表。 |
| `optional_variables` | `list[str]` | `[]` | 否 | 可选变量名列表（如占位符）。 |
| `partial_variables` | `Mapping[str, Any]` | `{}` | 否 | 预填充的变量及其值或生成函数。 |
| `output_parser` | `BaseOutputParser` | `None` | 否 | 关联的输出解析器，用于处理模型生成的响应。 |

#### 核心方法
- **`invoke / ainvoke`**: 实现 Runnable 接口，允许提示词模板作为链的第一步被调用。
- **`format_prompt / aformat_prompt`**: 抽象方法，负责将输入变量填充到模板中并返回 `PromptValue` 对象。
- **`format / aformat`**: 抽象方法，返回格式化后的具体输出类型（通常是字符串或消息列表）。
- **`partial`**: 创建一个预填充了部分变量的新模板实例。
- **`save`**: 将模板配置保存为 JSON 或 YAML 文件。

---

### 2. 辅助函数

#### `format_document`
**功能描述**: 根据提示词模板将 `Document` 对象（包含 `page_content` 和 `metadata`）格式化为字符串。常用于 RAG 场景中处理检索到的文档块。

---

## 核心逻辑

1. **输入验证**: 在格式化前，模板会检查传入的变量是否匹配 `input_variables`。如果缺少变量且未转义（使用 `{{}}`），将抛出异常。
2. **LCEL 集成**: 由于继承了 `RunnableSerializable`，提示词模板可以自动生成 Pydantic 输入模型，并在链式调用中处理元数据和标签。
3. **部分变量 (Partialing)**: 允许在创建模板时或运行前绑定某些变量（如当前日期）。这些变量可以是静态值，也可以是返回字符串的可调用对象。
4. **序列化**: 模板支持完整的序列化，允许通过 `save` 和 `load` 在不同环境间迁移。

---

## 使用示例

### 1. 基础格式化
```python
from langchain_core.prompts import PromptTemplate

template = PromptTemplate.from_template("你好，{name}！")
prompt_value = template.invoke({"name": "LangChain"})
print(prompt_value.to_string()) # 输出: 你好，LangChain！
```

### 2. 部分变量填充
```python
import datetime

def get_current_time():
    return str(datetime.datetime.now())

template = PromptTemplate.from_template("当前时间是：{time}。用户消息：{text}")
partial_template = template.partial(time=get_current_time)

# 调用时只需传入 text
print(partial_template.invoke({"text": "你好"}).to_string())
```

---

## 注意事项

- **保留关键字**: 不能使用名为 `stop` 的变量，因为它是 LLM 推理的内部参数。
- **变量冲突**: `input_variables` 和 `partial_variables` 不能有重叠。
- **转义**: 如果模板中需要包含字面意义的大括号（如代码块），必须使用双大括号（例如 `{{variable}}`）。
- **安全**: 保存模板时，如果包含 `partial_variables` 会抛出错误，因为动态生成的值（如函数）无法直接序列化为静态配置。

---

## 内部调用关系

- **`PromptValue`**: 模板生成的标准化对象，可进一步传递给 `LLM`（字符串）或 `ChatModel`（消息列表）。
- **`Runnable`**: 模板作为链的起点，其 `invoke` 结果通常作为下游组件（如模型）的输入。
- **`Document`**: 通过 `format_document` 与文档对象交互。

---

## 相关链接

- [LangChain 官方文档 - 提示词模板](https://python.langchain.com/docs/concepts/prompt_templates/)
- [LangChain 概念指南 - 序列化](https://python.langchain.com/docs/how_to/serialization/)

---

**最后更新时间**: 2026-01-29
**对应源码版本**: LangChain Core v1.2.7
