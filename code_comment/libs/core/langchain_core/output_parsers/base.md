# langchain_core.output_parsers.base

## 文件概述
`base.py` 定义了 LangChain 中所有输出解析器（Output Parsers）的基础抽象类。输出解析器的核心职责是将语言模型（LLM/ChatModel）生成的非结构化文本或消息转换为结构化的数据格式（如 JSON、Python 对象、布尔值等）。

这些基类定义了解析逻辑的标准接口，并确保了解析器可以作为 `Runnable` 对象集成到 LCEL（LangChain Expression Language）链中。

---

## 导入依赖
| 模块 | 作用 |
| :--- | :--- |
| `abc` | 提供 `ABC` 和 `abstractmethod` 用于定义抽象基类。 |
| `typing` | 提供类型注解支持（`Any`, `Generic`, `TypeVar` 等）。 |
| `langchain_core.language_models` | 导入 `LanguageModelOutput` 类型定义。 |
| `langchain_core.messages` | 导入消息基类 `BaseMessage`。 |
| `langchain_core.outputs` | 导入模型输出包装类 `Generation` 和 `ChatGeneration`。 |
| `langchain_core.runnables` | 导入 `Runnable` 及其相关配置类，使解析器具备可运行特性。 |

---

## 类与函数详解

### 1. BaseLLMOutputParser
**功能描述**: 所有模型输出解析器的最底层抽象基类。它定义了处理 `Generation` 对象列表的核心接口。

#### 核心方法
- **`parse_result` (抽象方法)**:
    - **功能**: 将模型生成的多个候选结果（`Generation` 列表）解析为目标格式。
    - **参数**: `result: list[Generation]` (模型输出列表), `partial: bool = False` (是否进行部分解析)。
    - **返回值**: `T` (解析后的结构化数据)。
- **`aparse_result`**: `parse_result` 的异步版本，默认在线程池中运行同步方法。

---

### 2. BaseGenerationOutputParser
**功能描述**: 继承自 `BaseLLMOutputParser` 和 `RunnableSerializable`，是处理模型生成结果的通用基类。它实现了 `invoke` 和 `ainvoke`，使得解析器可以直接处理字符串或消息输入。

#### 核心方法
- **`invoke` / `ainvoke`**: 接收 `str` 或 `BaseMessage` 输入，将其包装为 `Generation` 后调用 `parse_result`。

---

### 3. BaseOutputParser
**功能描述**: 这是开发者最常继承的基类。它在 `BaseLLMOutputParser` 之上进行了简化，主要关注如何解析单个字符串输出。

#### 核心方法
- **`parse` (抽象方法)**:
    - **功能**: 将 LLM 返回的单个字符串解析为目标结构。
    - **参数**: `text: str` (模型生成的文本内容)。
    - **返回值**: `T` (结构化结果)。
- **`parse_result`**: 默认实现是提取 `result` 中的第一个（最高概率）`Generation` 的文本，并传递给 `parse` 方法。
- **`get_format_instructions`**:
    - **功能**: 返回一个说明字符串，告知 LLM 应该以何种格式输出。通常通过 Prompt 注入。
- **`parse_with_prompt`**: 允许在解析时参考原始 Prompt 内容（常用于纠错或上下文敏感的解析）。

---

## 核心逻辑
1. **输入处理**: `BaseOutputParser` 可以接收 `str`（传统 LLM 输出）或 `BaseMessage`（聊天模型输出）。如果是消息，它会自动提取 `.content`。
2. **LCEL 集成**: 通过继承 `RunnableSerializable`，解析器可以无缝配合 `|` 操作符使用：`prompt | model | parser`。
3. **类型推断**: 利用 Pydantic 的泛型元数据，解析器能够推断其 `OutputType`，从而在复杂的链中提供类型校验支持。

---

## 使用示例

### 自定义简单的布尔解析器
```python
from langchain_core.output_parsers import BaseOutputParser

class BooleanOutputParser(BaseOutputParser[bool]):
    """将文本解析为布尔值的解析器。"""

    def parse(self, text: str) -> bool:
        cleaned_text = text.strip().lower()
        if "yes" in cleaned_text:
            return True
        elif "no" in cleaned_text:
            return False
        else:
            raise ValueError(f"无法解析输出: {text}")

    @property
    def _type(self) -> str:
        return "boolean_output_parser"

# 单独使用
parser = BooleanOutputParser()
print(parser.invoke("Yes, I agree.")) # 输出: True

# 在 LCEL 链中使用
# chain = prompt | model | parser
```

---

## 注意事项
- **单输出假设**: `BaseOutputParser.parse_result` 默认只处理 `Generation` 列表中的第一个元素。如果你的模型配置为生成多个 N-best 结果且你需要全部解析，请重写 `parse_result`。
- **序列化**: 为了支持 `load_keys` 或 `save` 等序列化操作，子类必须实现 `_type` 属性。
- **异常处理**: 解析器在处理不可控的模型输出时，应当抛出 `OutputParserException` 以便上层捕获并进行重试（Retry）或修复（OutputFixingParser）。

---

## 内部调用关系
- `BaseOutputParser` 依赖于 `langchain_core.outputs` 中的 `Generation` 数据结构。
- 它作为 `Runnable` 体系的一部分，被 `langchain_core.runnables` 调度执行。
- `JsonOutputParser`, `PydanticOutputParser` 等高级解析器均继承自此基类。

---

## 元信息
- **最后更新时间**: 2026-01-29
- **对应源码版本**: LangChain Core v1.2.7
