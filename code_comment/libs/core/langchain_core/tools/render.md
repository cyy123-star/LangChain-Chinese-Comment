# langchain_core.tools.render

## 文件概述
**langchain_core.tools.render** 模块提供了一组工具函数，用于将 `BaseTool` 对象转换为文本描述。这些描述通常被用于 Prompt 中，向语言模型展示可用工具的名称、功能及参数。

---

## 导入依赖
| 依赖项 | 来源 | 作用 |
| :--- | :--- | :--- |
| `Callable` | `collections.abc` | 用于类型提示，定义渲染器函数的签名。 |
| `signature` | `inspect` | 用于检查工具函数的签名（参数信息）。 |
| `BaseTool` | `langchain_core.tools.base` | 工具的基类。 |

---

## 类与函数详解

### 1. ToolsRenderer (类型别名)
**功能描述**: 定义了一个渲染器函数的标准类型。它接受一个 `BaseTool` 列表并返回一个字符串。

### 2. render_text_description
**功能描述**: 将工具列表渲染为纯文本形式的“名称: 描述”。
#### 参数说明
| 参数名 | 类型 | 默认值 | 是否必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `tools` | `list[BaseTool]` | - | 是 | 需要渲染的工具列表。 |
#### 返回值解释
- **类型**: `str`
- **含义**: 渲染后的纯文本字符串，每行一个工具，格式为 `name - description` 或 `name(signature) - description`。

### 3. render_text_description_and_args
**功能描述**: 将工具列表渲染为包含名称、描述和参数架构（JSON 格式）的纯文本。
#### 参数说明
| 参数名 | 类型 | 默认值 | 是否必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `tools` | `list[BaseTool]` | - | 是 | 需要渲染的工具列表。 |
#### 返回值解释
- **类型**: `str`
- **含义**: 包含详细参数信息的文本字符串，格式为 `name - description, args: {schema}`。

---

## 核心逻辑
1. **函数签名提取**: 如果工具对象具有 `func` 属性（即它是从函数创建的），渲染器会使用 `inspect.signature` 提取函数的参数签名，并将其附加到工具名称后。
2. **文本拼接**: 遍历所有工具，按照预定义格式拼接名称、签名、描述和参数架构。

---

## 使用示例
```python
from langchain_core.tools import tool
from langchain_core.tools.render import render_text_description, render_text_description_and_args

@tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

tools = [add]

# 仅渲染描述
print(render_text_description(tools))
# 输出示例: add(a: int, b: int) -> int - Add two numbers.

# 渲染描述和参数
print(render_text_description_and_args(tools))
# 输出示例: add(a: int, b: int) -> int - Add two numbers., args: {'a': {'type': 'integer'}, 'b': {'type': 'integer'}}
```

---

## 注意事项
- **渲染限制**: 默认的渲染器仅支持简单的文本输出。对于更复杂的输出格式（如 JSON 或 XML），可能需要自定义渲染逻辑。
- **签名解析**: `signature` 的解析依赖于 Python 函数的类型注解。如果函数没有类型注解，生成的签名可能不够详细。

---

## 内部调用关系
- 该模块主要被 Prompt Template 或 Agent 调用，用于动态生成 Prompt 中关于工具的部分。

---

## 相关链接
- [LangChain 官方文档 - Tools](https://python.langchain.com/docs/modules/agents/tools/)
- [langchain_core.tools.base](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/core/langchain_core/tools/base.md)

---

## 元信息
- **最后更新时间**: 2026-01-29
- **对应源码版本**: LangChain Core v1.2.7
