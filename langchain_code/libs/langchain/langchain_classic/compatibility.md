# Backwards Compatibility (向后兼容层)

为了确保从旧版本（v0.0.x）平滑过渡到现代 LangChain 架构，`langchain_classic` 的根目录下保留了一系列“补丁文件”或“垫片文件”（Shim Files）。

## 核心原理

这些文件的主要作用是：
1. **重定向导入**: 当用户尝试执行 `from langchain.text_splitter import ...` 时，这些文件会将请求重定向到新的包（如 `langchain-text-splitters`）或模块中。
2. **发出警告**: 在执行重定向的同时，通过内部的 `_api` 模块发出弃用警告，告知用户该组件的新位置。
3. **防止代码中断**: 即使底层代码结构发生了巨大变化（例如拆分为多个独立的包），用户的存量代码依然可以正常运行。

## 关键兼容文件说明

| 文件 | 说明 | 新位置 / 替代方案 |
| :--- | :--- | :--- |
| `text_splitter.py` | 传统的文本切分器。 | 已拆分为独立的 `langchain-text-splitters` 包。 |
| `sql_database.py` | SQL 数据库连接工具。 | 已迁移至 `langchain_community.utilities.sql_database`。 |
| `python.py` | Python REPL 运行环境。 | 已迁移至 `langchain_community.utilities.python`。 |
| `serpapi.py` | SerpAPI 搜索封装。 | 已迁移至 `langchain_community.utilities.serpapi`。 |
| `requests.py` | HTTP 请求工具。 | 已迁移至 `langchain_community.utilities.requests`。 |
| `formatting.py` | 字符串格式化工具。 | 已迁移至 `langchain_core.utils.formatting`。 |
| `input.py` | 终端输入输出工具（着色等）。 | 已迁移至 `langchain_core.utils.input`。 |
| `hub.py` | LangChain Hub 客户端。 | 建议直接使用 `langsmith` SDK 或 `langchainhub` 包。 |

## 实现机制示例

大部分兼容文件采用动态属性查找（`__getattr__`）或静态重新导入（Re-export）的方式：

```python
# 示例：text_splitter.py 中的重新导入
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    TextSplitter,
    # ...
)

# 示例：sql_database.py 中的动态查找
def __getattr__(name: str) -> Any:
    # 调用 _api 模块进行动态导入并发出警告
    return _import_attribute(name)
```

## 开发者建议

- **新开发**: 避免直接引用 `langchain` 根目录下的这些兼容文件，应直接从 `langchain-core`、`langchain-community` 或具体的集成包（如 `langchain-openai`）中导入。
- **重构**: 如果你的 IDE 提示某些导入已弃用，请根据警告信息中的建议更新你的 `import` 语句。
