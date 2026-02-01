# few_shot.py

## 文件概述
`few_shot.py` 模块定义了支持少样本（Few-Shot）示例的提示词模板。少样本学习是提示词工程中的核心技术，通过在提示词中包含少量示例，可以引导大语言模型（LLM）更好地理解任务要求并生成符合预期格式或风格的回复。

该模块提供了两种主要的模板类：
1. `FewShotPromptTemplate`：用于生成字符串格式的提示词，适用于传统的完成式模型（LLMs）。
2. `FewShotChatMessagePromptTemplate`：用于生成聊天消息列表，适用于对话式模型（Chat Models）。

---

## 导入依赖
- `pydantic`: 用于数据验证和设置配置。
- `langchain_core.example_selectors`: 提供示例选择器接口，用于从示例池中动态筛选最相关的示例。
- `langchain_core.messages`: 处理基础消息类型及消息缓冲区转换。
- `langchain_core.prompts.chat`, `langchain_core.prompts.message`, `langchain_core.prompts.prompt`: 导入基础模板类。
- `langchain_core.prompts.string`: 提供字符串格式化映射及模板校验工具。

---

## 类与函数详解

### 1. `_FewShotPromptTemplateMixin` (类)
少样本提示词模板的混入类，封装了示例管理的核心逻辑。

#### 属性说明
| 属性名 | 类型 | 默认值 | 是否必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `examples` | `list[dict] \| None` | `None` | 否 | 静态示例列表。与 `example_selector` 二选一。 |
| `example_selector` | `BaseExampleSelector \| None` | `None` | 否 | 动态示例选择器。与 `examples` 二选一。 |

#### 核心方法
- `check_examples_and_selector`: Pydantic 校验器，确保 `examples` 和 `example_selector` 仅提供其中之一。
- `_get_examples` / `_aget_examples`: 获取用于格式化的示例列表。如果是静态列表则直接返回，如果是选择器则根据输入参数进行筛选。

---

### 2. `FewShotPromptTemplate` (类)
字符串格式的少样本提示词模板。

#### 属性说明
| 属性名 | 类型 | 默认值 | 是否必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `example_prompt` | `PromptTemplate` | - | 是 | 用于格式化单个示例的模板。 |
| `suffix` | `str` | - | 是 | 示例之后的后缀内容（通常是用户的实际查询）。 |
| `prefix` | `str` | `""` | 否 | 示例之前的引导语或任务说明。 |
| `example_separator` | `str` | `"\n\n"` | 否 | 连接前缀、各个示例及后缀的分隔符。 |
| `template_format` | `Literal["f-string", "jinja2"]` | `"f-string"` | 否 | 模板语法格式。 |
| `validate_template` | `bool` | `False` | 否 | 是否在初始化时校验模板变量的合法性。 |

#### 核心逻辑
1. **合并变量**：合并 partial 变量和用户传入的变量。
2. **获取示例**：通过 `examples` 或 `example_selector` 获取示例数据。
3. **格式化单个示例**：使用 `example_prompt` 对每个示例字典进行格式化，生成字符串列表。
4. **组装模板**：将 `prefix`、格式化后的示例列表、`suffix` 使用 `example_separator` 拼接成完整的模板字符串。
5. **最终填充**：使用传入的变量填充拼接后的完整模板。

#### 使用示例
```python
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate

examples = [
    {"word": "happy", "antonym": "sad"},
    {"word": "tall", "antonym": "short"},
]

example_prompt = PromptTemplate(
    input_variables=["word", "antonym"],
    template="Word: {word}\nAntonym: {antonym}",
)

few_shot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="Give the antonym of every input",
    suffix="Word: {input}\nAntonym:",
    input_variables=["input"],
)

print(few_shot_prompt.format(input="big"))
# 输出:
# Give the antonym of every input
#
# Word: happy
# Antonym: sad
#
# Word: tall
# Antonym: short
#
# Word: big
# Antonym:
```

---

### 3. `FewShotChatMessagePromptTemplate` (类)
聊天格式的少样本提示词模板。

#### 属性说明
| 属性名 | 类型 | 默认值 | 是否必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `example_prompt` | `BaseMessagePromptTemplate \| BaseChatPromptTemplate` | - | 是 | 用于将单个示例格式化为消息列表的模板。 |
| `input_variables` | `list[str]` | `[]` | 否 | 传递给 `example_selector` 的变量名列表。 |

#### 核心逻辑
- `format_messages` / `aformat_messages`:
  1. 获取示例数据。
  2. 使用 `example_prompt.format_messages` 将每个示例字典转换为一组消息。
  3. 将所有消息展平并返回。
- `format` / `aformat`: 调用 `format_messages` 后，通过 `get_buffer_string` 将消息列表转换为人类可读的字符串（主要用于调试）。

#### 注意事项
- 产生的结构通常是消息列表：`[prefix_messages] + [example_1_messages, example_2_messages, ...] + [suffix_messages]`。
- 建议与 `ChatPromptTemplate.from_messages` 配合使用。

---

## 内部调用关系
- **继承关系**:
  - `FewShotPromptTemplate` 继承自 `StringPromptTemplate`。
  - `FewShotChatMessagePromptTemplate` 继承自 `BaseChatPromptTemplate`。
- **依赖关系**:
  - 依赖 `ExampleSelector` 进行动态示例选取。
  - `FewShotPromptTemplate` 内部持有一个 `PromptTemplate` 作为 `example_prompt`。
  - `FewShotChatMessagePromptTemplate` 内部持有一个消息类模板作为 `example_prompt`。

---

## 相关链接
- [LangChain 官方文档 - Few-shot prompt templates](https://python.langchain.com/docs/modules/model_io/prompts/few_shot_prompt_templates/)
- [LangChain 官方文档 - Few-shot chat messages](https://python.langchain.com/docs/modules/model_io/prompts/few_shot_chat_messages/)
- [langchain_core.example_selectors 源码](../example_selectors/base.py)

---
**对应源码版本**: LangChain Core v1.2.7
**最后更新时间**: 2026-01-29
