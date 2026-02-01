# libs\core\langchain_core\utils\formatting.py

## 文件概述

`formatting.py` 模块提供了字符串格式化的工具，主要用于 LangChain 的提示词模板（Prompt Templates）。它通过扩展 Python 标准库的 `string.Formatter`，引入了更严格的校验机制，确保变量替换的准确性和显式性。

## 导入依赖

- `string.Formatter`: Python 标准库提供的基础格式化类。
- `collections.abc`: 提供 `Mapping` 和 `Sequence` 类型提示。

## 类与函数详解

### 1. StrictFormatter
- **功能描述**: 继承自 `Formatter`，强制要求所有变量替换必须使用关键字参数（keyword arguments），禁止使用位置参数（positional arguments）。这在复杂的提示词工程中可以有效防止因参数顺序错误导致的逻辑漏洞。
- **主要方法**:
    - `vformat(format_string, args, kwargs)`: 重写基类方法。如果 `args` 不为空（即存在位置参数），则抛出 `ValueError`。
    - `validate_input_variables(format_string, input_variables)`: 预验证函数。检查提供的变量列表是否足以填充格式化字符串中的所有占位符。

### 2. formatter (全局实例)
- **功能描述**: `StrictFormatter` 的默认实例，供 LangChain 内部（如 `PromptTemplate`）统一使用。

## 使用示例

```python
from langchain_core.utils.formatting import formatter

# 正确用法：使用关键字参数
text = formatter.format("Hello, {name}!", name="LangChain")
print(text) # "Hello, LangChain!"

# 错误用法：使用位置参数会报错
try:
    formatter.format("Hello, {}!", "LangChain")
except ValueError as e:
    print(e) # "No arguments should be provided..."

# 预验证变量
formatter.validate_input_variables("Welcome to {city}, {name}!", ["city", "name"]) # 通过
```

## 注意事项

- **严格性**: `StrictFormatter` 仅支持显式命名变量。如果你的模板中包含 `{}` 这种匿名占位符，必须改为 `{var_name}` 形式。
- **集成**: 该类是 LangChain 提示词系统的基石，确保了 LCEL 表达式中数据流向的清晰。

---
最后更新时间: 2026-01-29
对应源码版本: LangChain Core v1.2.7
