# libs\core\langchain_core\utils\strings.py

## 文件概述

`strings.py` 提供了一系列通用的字符串处理工具函数，包括对象字符串化、字典格式化、列表合并以及针对特定数据库（如 PostgreSQL）的安全过滤。

## 导入依赖

- `collections.abc.Iterable`: 用于处理可迭代对象。
- `typing.Any`: 类型提示支持。

## 类与函数详解

### 1. stringify_value
- **功能描述**: 将任意值转换为字符串。它会针对字典和列表进行递归处理，以获得更具可读性的输出。
- **参数说明**:
| 参数名 | 类型 | 默认值 | 是否必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `val` | `Any` | - | 是 | 要转换为字符串的值。 |
- **返回值**: `str`，转换后的字符串。

### 2. stringify_dict
- **功能描述**: 将字典转换为易读的键值对字符串，每行一个。
- **参数说明**:
| 参数名 | 类型 | 默认值 | 是否必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `data` | `dict` | - | 是 | 要转换的字典。 |
- **返回值**: `str`，格式化后的字典字符串。

### 3. comma_list
- **功能描述**: 将可迭代对象转换为以逗号分隔的字符串。
- **参数说明**:
| 参数名 | 类型 | 默认值 | 是否必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `items` | `Iterable[Any]` | - | 是 | 要合并的项。 |
- **返回值**: `str`，如 `"item1, item2, item3"`。

### 4. sanitize_for_postgres
- **功能描述**: 过滤文本中的 NUL (`\x00`) 字节。PostgreSQL 的文本字段不支持此类字节，否则会导致插入错误（`psycopg.DataError`）。
- **参数说明**:
| 参数名 | 类型 | 默认值 | 是否必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `text` | `str` | - | 是 | 要清理的原始文本。 |
| `replacement` | `str` | `""` | 否 | 用于替换 NUL 字节的字符串。默认直接移除。 |
- **返回值**: `str`，清理后的安全字符串。

## 使用示例

```python
from langchain_core.utils.strings import stringify_value, sanitize_for_postgres

# 递归字符串化
data = {"key": ["val1", "val2"]}
print(stringify_value(data))

# PostgreSQL 安全过滤
unsafe_text = "Hello\x00World"
safe_text = sanitize_for_postgres(unsafe_text)
assert safe_text == "HelloWorld"
```

## 注意事项

- **性能**: `stringify_value` 对大型嵌套结构的递归处理可能会有性能开销，主要用于日志记录或提示词构建。
- **数据库兼容性**: 在将用户输入或爬虫数据存入 PostgreSQL 之前，建议始终调用 `sanitize_for_postgres`。

---
最后更新时间: 2026-01-29
对应源码版本: LangChain Core v1.2.7
