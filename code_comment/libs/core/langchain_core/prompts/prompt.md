# libs\core\langchain_core\prompts\prompt.py

## 文件概述
`prompt.py` 定义了 LangChain 中最基础且最常用的提示词模板类 `PromptTemplate`。它是 `StringPromptTemplate` 的具体实现，主要负责处理基于字符串的提示词生成。该模块支持多种模板格式（如 f-string, jinja2, mustache），并提供了灵活的实例化方式（如从字符串或文件加载）、变量校验以及模板组合功能。

## 导入依赖
- `pathlib.Path`: 用于处理文件路径，支持从文件中加载模板。
- `pydantic.BaseModel`, `model_validator`: 用于数据验证和 Pydantic 模型的预处理。
- `langchain_core.prompts.string`: 提供了字符串模板的基础抽象类 `StringPromptTemplate` 以及模板格式化工具。

## 类与函数详解

### PromptTemplate
`PromptTemplate` 是语言模型提示词模板的核心类。它封装了模板字符串及其相关的元数据和逻辑。

#### 属性说明
| 属性名 | 类型 | 默认值 | 是否必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `template` | `str` | - | 是 | 提示词模板字符串。 |
| `template_format` | `PromptTemplateFormat` | `"f-string"` | 否 | 模板语法格式。支持 `'f-string'`, `'mustache'`, `'jinja2'`。 |
| `validate_template` | `bool` | `False` | 否 | 是否在初始化时校验模板变量与 `input_variables` 的一致性。 |

#### 核心方法

##### format
- **功能描述**: 使用提供的输入变量填充模板，生成最终的提示词字符串。
- **参数说明**:
  - `**kwargs`: 包含模板中定义的所有变量及其对应的值。
- **返回值**: 格式化后的提示词字符串。

##### from_template (classmethod)
- **功能描述**: 推荐的实例化方法。自动从模板字符串中提取变量名并创建 `PromptTemplate` 对象。
- **参数说明**:
  - `template`: 模板字符串。
  - `template_format`: 模板格式（默认 `"f-string"`）。
  - `partial_variables`: 部分预填充变量。
- **返回值**: `PromptTemplate` 实例。

##### from_file (classmethod)
- **功能描述**: 从指定路径的文件中读取内容并创建提示词模板。
- **参数说明**:
  - `template_file`: 文件路径。
  - `encoding`: 文件编码格式。
- **返回值**: `PromptTemplate` 实例。

##### __add__ (operator override)
- **功能描述**: 重载 `+` 运算符，允许将两个提示词模板拼接在一起。
- **要求**: 两个模板的 `template_format` 必须一致，且不能有冲突的 `partial_variables`。

## 核心逻辑
1. **自动变量提取**: 在 `from_template` 或 `pre_init_validation` 阶段，系统会根据 `template_format` 自动解析模板中的占位符，并将其填充到 `input_variables` 中。
2. **安全性校验 (Jinja2)**: 针对 `jinja2` 模板，LangChain 默认使用沙箱环境（SandboxedEnvironment）进行渲染，以降低执行恶意 Python 代码的风险。但仍建议仅对受信任的源使用 `jinja2`。
3. **部分填充**: 支持 `partial_variables`，允许在运行 `format` 之前预先设置一部分变量的值（如当前日期、默认上下文等）。

## 使用示例

```python
from langchain_core.prompts import PromptTemplate

# 1. 使用 from_template 快速创建
prompt = PromptTemplate.from_template("请用中文回答关于 {topic} 的问题。")
result = prompt.format(topic="量子力学")
print(result) # 输出: 请用中文回答关于 量子力学 的问题。

# 2. 模板拼接
greeting = PromptTemplate.from_template("你好，{name}！")
question = PromptTemplate.from_template("请问 {question}")
full_prompt = greeting + "\n" + question
print(full_prompt.format(name="小明", question="今天天气怎么样？"))

# 3. 使用 Jinja2 模板（支持更复杂的逻辑）
jinja_prompt = PromptTemplate.from_template(
    "用户列表：{% for user in users %}- {{ user }}{% endfor %}",
    template_format="jinja2"
)
print(jinja_prompt.format(users=["Alice", "Bob"]))
```

## 注意事项
- **安全性**: **严禁**接收来自不受信任源的 `jinja2` 模板，因为它可能导致任意代码执行。
- **变量冲突**: 使用 `+` 运算符组合模板时，如果两个模板定义了同名的 `partial_variables` 但值不同，会抛出 `ValueError`。
- **Mustache 校验**: `mustache` 模板格式不支持初始化时的自动化变量校验。

## 内部调用关系
- **继承关系**: 继承自 `StringPromptTemplate`，间接继承自 `BasePromptTemplate` 和 `RunnableSerializable`。
- **格式化引擎**: 依赖 `langchain_core.prompts.string` 中的 `DEFAULT_FORMATTER_MAPPING` 来执行实际的渲染逻辑。

## 相关链接
- [LangChain 官方文档 - Prompt Templates](https://python.langchain.com/docs/concepts/prompt_templates/)
- [Jinja2 官方文档](https://jinja.palletsprojects.com/)

---
最后更新时间: 2026-01-29
对应源码版本: LangChain Core v1.2.7