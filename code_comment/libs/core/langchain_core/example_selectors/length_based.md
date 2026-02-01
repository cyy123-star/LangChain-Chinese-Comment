# langchain_core.example_selectors.length_based

`langchain_core.example_selectors.length_based` 模块提供了一个基于长度的示例选择器。它根据提示词的总长度限制，动态地选择尽可能多的示例，以确保最终生成的提示词不会超过模型的上下文窗口限制。

## 文件概述

- **角色**: 基于长度的动态示例选择器。
- **主要职责**: 测量示例和输入的文本长度，并按顺序选择示例，直到达到设定的最大长度阈值。
- **所属模块**: `langchain_core.example_selectors`

## 导入依赖

- `re`: 用于通过正则表达式分割文本以计算长度。
- `pydantic`: 提供 `BaseModel` 支持和数据验证。
- `langchain_core.example_selectors.base`: 导入 `BaseExampleSelector` 基类。
- `langchain_core.prompts.prompt`: 导入 `PromptTemplate` 用于格式化示例。

## 类与函数详解

### 1. LengthBasedExampleSelector
- **功能描述**: 根据文本长度选择示例。它会预先计算每个示例格式化后的长度，并在运行时根据输入的长度计算剩余空间，从而决定包含哪些示例。
- **参数说明**:
  | 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
  | :--- | :--- | :--- | :--- | :--- |
  | `examples` | `list[dict]` | - | 是 | 候选示例列表。 |
  | `example_prompt` | `PromptTemplate` | - | 是 | 用于格式化单个示例的模板。 |
  | `get_text_length` | `Callable` | `_get_length_based` | 否 | 计算文本长度的函数。默认为按单词/换行符计数。 |
  | `max_length` | `int` | `2048` | 否 | 提示词允许的最大总长度（单位由 `get_text_length` 决定）。 |

### 2. _get_length_based(text: str) -> int
- **功能描述**: 默认的长度计算函数。它使用正则表达式 `\n| ` 将文本分割，并返回分割后的片段数量（大致对应单词数）。

## 核心逻辑

- **初始化预计算**: 在对象创建后，它会遍历所有初始示例，使用 `example_prompt` 将其格式化为字符串，并调用 `get_text_length` 记录每个示例的长度。
- **动态选择策略**: 
  1. 计算当前用户输入（`input_variables`）的总长度。
  2. 计算剩余可用空间：`max_length - input_length`。
  3. 按顺序遍历示例库，如果当前示例的长度小于等于剩余空间，则将其加入结果集，并减去相应空间。
  4. 一旦遇到空间不足，立即停止选择。

## 使用示例

```python
from langchain_core.example_selectors import LengthBasedExampleSelector
from langchain_core.prompts import PromptTemplate

examples = [
    {"input": "happy", "output": "sad"},
    {"input": "tall", "output": "short"},
    {"input": "energetic", "output": "lethargic"},
]

example_prompt = PromptTemplate(
    input_variables=["input", "output"],
    template="Input: {input}\nOutput: {output}",
)

example_selector = LengthBasedExampleSelector(
    examples=examples,
    example_prompt=example_prompt,
    max_length=25, # 设置一个非常小的限制
)

# 当输入较短时，可能会包含更多示例
print(example_selector.select_examples({"adjective": "big"}))

# 当输入很长时，示例会被切断以防超出限制
```

## 注意事项

- **顺序敏感**: 该选择器是按示例列表的原始顺序进行选择的。如果你希望优先包含某些示例，请将它们放在列表前端。
- **单位一致性**: `max_length` 的单位必须与 `get_text_length` 返回的单位一致。如果是按字符计数，则 `max_length` 应设为字符数限制。
- **Token 限制**: 虽然默认实现是按单词计数，但实际应用中，建议自定义 `get_text_length` 使用模型对应的 Tokenizer 进行精确计数。

## 内部调用关系

- **PromptTemplate**: 使用 `example_prompt.format` 将字典转换为可测量长度的字符串。

## 相关链接
- [LangChain 官方文档 - 基于长度的选择器](https://python.langchain.com/docs/modules/model_io/prompts/example_selectors/length_based/)

---
- **最后更新时间**: 2026-01-29
- **对应源码版本**: LangChain Core v1.2.7
