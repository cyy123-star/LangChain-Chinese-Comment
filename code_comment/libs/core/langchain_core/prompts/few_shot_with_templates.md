# few_shot_with_templates.py

## 文件概述
`few_shot_with_templates.py` 模块定义了 `FewShotPromptWithTemplates` 类。它是 `FewShotPromptTemplate` 的进阶版本，主要区别在于：它的 `prefix`（前缀）和 `suffix`（后缀）不再是简单的静态字符串，而是完整的 `StringPromptTemplate` 对象。

这种设计允许前缀和后缀本身也具备动态格式化的能力，极大地增强了少样本提示词模板的灵活性和表达能力。

---

## 导入依赖
- `langchain_core.example_selectors`: 用于动态选择示例。
- `langchain_core.prompts.prompt`: 导入基础 `PromptTemplate` 类。
- `langchain_core.prompts.string`: 继承自 `StringPromptTemplate` 并使用其格式化引擎。

---

## 类与函数详解

### 1. `FewShotPromptWithTemplates` (类)
支持模板化前缀和后缀的少样本提示词模板。

#### 属性说明
| 属性名 | 类型 | 默认值 | 是否必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `prefix` | `StringPromptTemplate \| None` | `None` | 否 | 前缀模板。 |
| `suffix` | `StringPromptTemplate` | - | 是 | 后缀模板。 |
| `example_prompt` | `PromptTemplate` | - | 是 | 格式化单个示例的模板。 |
| `examples` | `list[dict] \| None` | `None` | 否 | 静态示例列表。 |
| `example_selector` | `BaseExampleSelector \| None` | `None` | 否 | 动态示例选择器。 |
| `example_separator` | `str` | `"\n\n"` | 否 | 连接各部分的字符串。 |

#### 核心逻辑 (format 方法)
1. **获取示例**：通过 `examples` 或 `example_selector` 准备数据。
2. **格式化示例**：使用 `example_prompt` 将示例数据转换为字符串列表。
3. **格式化前缀**：如果提供了 `prefix` 模板，则从传入的变量中提取所需部分进行格式化。
4. **格式化后缀**：从剩余变量中提取 `suffix` 模板所需的变量并进行格式化。
5. **拼接与二次格式化**：将前缀、格式化后的示例、后缀拼接在一起，并对最终生成的字符串进行最后一次变量填充。

#### 使用场景
当你需要前缀或后缀也根据输入动态变化时，例如：
- 前缀需要包含当前的日期或用户的历史偏好。
- 后缀需要根据不同的查询任务调整指令。

---

## 注意事项
- **变量分发**：在格式化过程中，传入的参数会自动分发给 `prefix` 和 `suffix`。如果多个模板共用同名变量，需要注意其一致性。
- **序列化限制**：目前暂不支持保存包含 `example_selector` 的此类对象。

---

## 内部调用关系
- **继承关系**: `FewShotPromptWithTemplates` -> `StringPromptTemplate` -> `BasePromptTemplate`。
- **组合关系**: 内部持有多个 `StringPromptTemplate` 的实例，形成一种“模板套模板”的结构。

---

## 相关链接
- [LangChain 官方文档 - Prompt Templates](https://python.langchain.com/docs/modules/model_io/prompts/prompt_templates/)
- [few_shot.py 源码](./few_shot.md)

---
**对应源码版本**: LangChain Core v1.2.7
**最后更新时间**: 2026-01-29
