# Tools (工具集)

`tools` 模块是 LangChain 赋予 Agent 外部能力的桥梁。通过工具，LLM 可以执行 Python 代码、搜索网页、查询数据库或调用任何第三方 API。

## 核心接口

### `BaseTool`
所有工具的基类。一个标准的工具包含：
- `name`: 工具名称。
- `description`: 工具的功能描述（非常重要，LLM 根据描述决定是否调用该工具）。
- `args_schema`: 工具输入参数的 Pydantic 模型（用于增强类型安全）。

## 工具类型

| 类别 | 示例 |
| :--- | :--- |
| **搜索** | `DuckDuckGoSearchRun`, `TavilySearchResults`, `GoogleSearchRun` |
| **代码执行** | `PythonREPLTool` |
| **文件操作** | `ReadFileTool`, `WriteFileTool`, `ListDirectoryTool` |
| **数据库** | `QuerySQLDataBaseTool`, `InfoSQLDatabaseTool` |
| **协作/办公** | `GmailSendMessage`, `SlackSendMessage`, `JiraAction` |

## 定义工具的多种方式

1. **`@tool` 装饰器**: 最简单的方式，直接将 Python 函数转换为工具。
2. **继承 `BaseTool`**: 适合需要复杂逻辑或状态管理的工具。
3. **结构化工具**: 使用 `StructuredTool.from_function` 支持多参数输入。

## 使用示例

```python
from langchain.tools import tool

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers together."""
    return a * b

# 查看工具信息
print(multiply.name)
print(multiply.description)
```

## 注意事项

- **描述即性能**: 工具的 `description` 直接影响 Agent 的决策质量。
- **安全性**: 像 `ShellTool` 或 `PythonREPLTool` 这样的工具在生产环境中必须在沙箱或受控环境中运行。
- **现代集成**: 许多工具现在通过 `langchain-community` 提供，或直接作为外部包安装。
