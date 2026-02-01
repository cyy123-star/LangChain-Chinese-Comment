# string.py

## 文件概述
`string.py` 模块是 LangChain 提示词系统的核心组件，专门负责字符串格式提示词的模板引擎逻辑、变量提取、合法性校验以及安全性控制。它支持多种主流模板格式，包括 Python 原生的 `f-string`、功能强大的 `jinja2` 以及简洁的 `mustache`。

该模块定义了 `StringPromptTemplate` 基类，并提供了一系列底层工具函数，确保提示词在生成过程中的准确性和安全性。

---

## 导入依赖
- `jinja2`: 用于处理复杂的模板逻辑（如循环、条件判断），使用沙箱环境（`SandboxedEnvironment`）以增强安全性。
- `pydantic`: 用于动态创建数据模型（`mustache_schema`）。
- `langchain_core.prompt_values`: 定义格式化后的提示词返回值类型。
- `langchain_core.utils.mustache`: LangChain 内部实现的 Mustache 渲染引擎。
- `langchain_core.utils.formatting`: 封装了基础的 f-string 格式化工具。

---

## 核心概念与常量

### 1. `PromptTemplateFormat` (类型别名)
定义了支持的模板格式：`"f-string"`, `"mustache"`, `"jinja2"`。

### 2. 映射注册表
- `DEFAULT_FORMATTER_MAPPING`: 建立格式名称与渲染函数之间的映射。
- `DEFAULT_VALIDATOR_MAPPING`: 建立格式名称与变量校验函数之间的映射。

---

## 类与函数详解

### 1. 格式化函数

#### `jinja2_formatter` (函数)
使用 Jinja2 渲染模板。
- **安全性**：强制使用 `SandboxedEnvironment`。禁止访问对象属性（`.attr`）和调用方法（`.method()`），仅允许简单的变量替换。
- **警告**：不应处理来自不可信来源的模板。

#### `mustache_formatter` (函数)
使用 Mustache 渲染模板，适用于需要跨语言兼容性的场景。

---

### 2. 变量提取与校验

#### `get_template_variables` (函数)
根据指定的格式从模板字符串中提取所有待填充的变量名。
- **f-string 特殊逻辑**：
    - 禁止使用包含点号（`.`）或中括号（`[]`）的变量名，防止属性访问攻击。
    - 禁止使用纯数字变量名，防止位置参数混淆。

#### `check_valid_template` (函数)
校验模板字符串是否有效，以及声明的 `input_variables` 是否与模板中的占位符匹配。如果存在缺失或多余变量，会抛出 `ValueError` 或发出警告。

---

### 3. `StringPromptTemplate` (类)
所有生成字符串提示词的模板类的抽象基类。

#### 核心方法
| 方法名 | 返回类型 | 描述 |
| :--- | :--- | :--- |
| `format_prompt` | `PromptValue` | 调用 `format` 后将结果包装为 `StringPromptValue` 对象。 |
| `format` | `str` (抽象) | 核心格式化方法，需由子类实现。 |
| `pretty_repr` | `str` | 返回带颜色的、易于阅读的模板预览。 |

---

## 安全性设计 (Security)
该模块高度重视提示词注入（Prompt Injection）和任意代码执行（RCE）风险：
- **Jinja2 沙箱**：限制了模板访问 Python 运行时的能力。
- **f-string 限制**：通过 `get_template_variables` 中的逻辑，切断了利用 Python 格式化字符串漏洞访问敏感对象的路径。

---

## 内部调用关系
- **继承体系**: `StringPromptTemplate` 继承自 `BasePromptTemplate`。
- **下游依赖**: `PromptTemplate`（在 `prompt.py` 中）是其最主要的实现类。
- **底层依赖**: 依赖 `langchain_core.utils.formatting` 处理基础的字符串操作。

---

## 相关链接
- [LangChain 官方文档 - Prompt Templates](https://python.langchain.com/docs/modules/model_io/prompts/prompt_templates/)
- [Jinja2 官方文档 - Sandbox](https://jinja.palletsprojects.com/en/3.1.x/sandbox/)
- [Mustache 官方文档](https://mustache.github.io/)

---
**对应源码版本**: LangChain Core v1.2.7
**最后更新时间**: 2026-01-29
