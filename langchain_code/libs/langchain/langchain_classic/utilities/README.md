# Utilities (实用工具/第三方集成)

`utilities` 模块是 LangChain 与外部世界连接的底层实现层。它包含了各种封装好的客户端，供 `tools` 或 `chains` 调用。

## 核心职责

`utilities` 并不直接作为 Agent 的“动作”，而是为动作提供“能力”：
- **API 封装**: 对 Google Search, Wolfram Alpha, Wikipedia 等 API 的底层请求封装。
- **环境隔离**: 如 `PythonREPL` 的执行环境管理。
- **协议处理**: 处理 SQL, GraphQL, Bash 等特定协议的通信。

## 常用组件

| 组件 | 说明 |
| :--- | :--- |
| `SerpAPIWrapper` | 封装了主流搜索引擎的 API 访问。 |
| `SQLDatabase` | 提供对关系型数据库的连接、架构检查和查询执行。 |
| `WikipediaAPIWrapper` | 简化了对维基百科内容的搜索和摘要获取。 |
| `WolframAlphaAPIWrapper` | 接入 Wolfram Alpha 的计算知识引擎。 |
| `RequestsWrapper` | 提供了带认证和错误处理的标准 HTTP 请求功能。 |

## 与 Tools 的区别

- **Utility**: 底层实现。例如 `SQLDatabase` 负责连接数据库并执行 SQL。
- **Tool**: 顶层包装。例如 `QuerySQLDataBaseTool` 调用 `SQLDatabase` 并在其 `description` 中告诉 LLM 如何使用它。

## 使用示例

```python
from langchain_community.utilities import WikipediaAPIWrapper

wikipedia = WikipediaAPIWrapper()
result = wikipedia.run("LangChain")
print(result)
```

## 迁移指南

- **集成分离**: 绝大多数 Utility 实现现在都位于 `langchain-community` 中。
- **配置**: 大部分 Utility 依赖于环境变量（如 `OPENAI_API_KEY`, `SERPAPI_API_KEY`）进行身份验证。
