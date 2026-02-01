# loading.py

## 文件概述
`loading.py` 模块负责从配置文件（JSON 或 YAML）或配置字典中加载提示词模板。它实现了提示词的持久化与反序列化逻辑，允许开发者将提示词与其代码逻辑分离，存储在独立的文件中。

该模块支持加载多种类型的提示词，包括基础提示词、少样本（Few-shot）提示词以及聊天提示词，并能自动处理外部文件引用（如从 `.txt` 文件加载模板内容）。

---

## 导入依赖
- `json`, `yaml`: 用于解析配置文件。
- `pathlib.Path`: 用于处理文件路径。
- `langchain_core.prompts`: 导入各种基础提示词模板类。
- `langchain_core.output_parsers`: 用于加载关联的输出解析器。

---

## 核心函数详解

### 1. `load_prompt` (函数)
从本地文件系统加载提示词模板的统一入口。
- **参数**:
    - `path`: 配置文件路径（`.json`, `.yaml` 或 `.yml`）。
    - `encoding`: 文件编码。
- **核心逻辑**:
    - 检查路径是否以 `lc://` 开头（已废弃的 GitHub Hub 协议），若是则抛出错误。
    - 调用 `_load_prompt_from_file` 读取文件内容并转换为字典。
    - 调用 `load_prompt_from_config` 根据字典内容实例化对象。

### 2. `load_prompt_from_config` (函数)
根据配置字典加载提示词对象。
- **参数**: `config` (dict)
- **核心逻辑**:
    - 识别 `_type` 字段（默认为 `prompt`）。
    - 根据类型在 `type_to_loader_dict` 中查找对应的加载函数。
    - 目前支持的类型：`prompt`, `few_shot`, `chat`。

### 3. 内部加载辅助函数
- `_load_template`: 如果配置中包含 `template_path`，则从对应的 `.txt` 文件读取模板字符串。
- `_load_examples`: 如果少样本配置中包含 `examples` 路径，则从 `.json` 或 `.yaml` 文件加载示例列表。
- `_load_output_parser`: 加载提示词关联的输出解析器（目前仅支持默认的 `StrOutputParser`）。

---

## 类型加载映射 (`type_to_loader_dict`)
| 类型键 (_type) | 处理函数 | 描述 |
| :--- | :--- | :--- |
| `prompt` | `_load_prompt` | 加载标准的 `PromptTemplate`。 |
| `few_shot` | `_load_few_shot_prompt` | 加载 `FewShotPromptTemplate`，包含前缀、后缀、示例及示例模板。 |
| `chat` | `_load_chat_prompt` | 加载 `ChatPromptTemplate`（目前实现较为简易）。 |

---

## 安全性设计与约束
- **禁用 Jinja2**: 由于安全性风险（可能导致任意代码执行），通过配置文件加载时已禁用 `jinja2` 格式，建议迁移至 `f-string`。
- **弃用 Hub 协议**: 不再支持通过 `lc://` 从旧版 GitHub Hub 加载提示词，引导用户使用新的 [LangSmith Hub](https://smith.langchain.com/hub)。
- **文件后缀校验**: 模板文件必须是 `.txt`，数据文件必须是 `.json` 或 `.yaml`。

---

## 内部调用关系
- **依赖关系**: 依赖于 `prompt.py`, `few_shot.py`, `chat.py` 等模块提供的具体类实现。
- **调用流**: `load_prompt` -> `_load_prompt_from_file` -> `load_prompt_from_config` -> `具体类型的 _load 函数`。

---

## 相关链接
- [LangChain 官方文档 - Serialization](https://python.langchain.com/docs/modules/model_io/prompts/prompt_templates/serialization)
- [LangSmith Hub](https://smith.langchain.com/hub)

---
**对应源码版本**: LangChain Core v1.2.7
**最后更新时间**: 2026-01-29
