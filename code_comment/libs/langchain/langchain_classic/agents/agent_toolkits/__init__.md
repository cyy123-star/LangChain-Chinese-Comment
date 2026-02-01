# libs\langchain\langchain_classic\agents\agent_toolkits\__init__.py

此文档提供了 `libs\langchain\langchain_classic\agents\agent_toolkits\__init__.py` 文件的详细中文注释。该模块是代理工具包（Agent Toolkits）的入口点，包含了各种外部资源和服务的集成。

## 功能描述

代理工具包（Agent Toolkits）包含与各种资源和服务的集成。LangChain 拥有庞大的集成生态系统，包括本地和远程文件系统、API 和数据库。

这些集成允许开发者创建多功能应用程序，将大语言模型（LLMs）的能力与访问、交互和操作外部资源的能力相结合。

## 主要组件与工厂函数

该模块导出了核心的代理创建函数和工具包类：

### 1. 对话检索代理 (Conversational Retrieval)
- `create_conversational_retrieval_agent`: 创建一个能够进行对话并根据检索结果回答问题的代理。

### 2. 向量存储代理 (Vectorstore)
- `create_vectorstore_agent`: 针对单个向量存储的代理创建函数。
- `create_vectorstore_router_agent`: 针对多个向量存储进行路由的代理创建函数。
- `VectorStoreToolkit`, `VectorStoreRouterToolkit`, `VectorStoreInfo`: 向量存储相关的工具包和配置类。

### 3. 通用工具
- `create_retriever_tool`: 将检索器（Retriever）包装为代理可用的工具。

## 动态导入与弃用处理

为了优化加载速度并保持向后兼容性，该模块使用了动态导入机制处理已迁移到 `langchain_community` 或 `langchain_experimental` 的组件。

### 1. 迁移至 `langchain_community`
以下工具包和函数已迁移到 `langchain_community`，通过 `DEPRECATED_LOOKUP` 进行动态映射：

| 组件名称 | 目标路径 |
| :--- | :--- |
| `AINetworkToolkit` | `langchain_community.agent_toolkits.ainetwork.toolkit` |
| `AmadeusToolkit` | `langchain_community.agent_toolkits.amadeus.toolkit` |
| `AzureCognitiveServicesToolkit` | `langchain_community.agent_toolkits.azure_cognitive_services` |
| `FileManagementToolkit` | `langchain_community.agent_toolkits.file_management.toolkit` |
| `GmailToolkit` | `langchain_community.agent_toolkits.gmail.toolkit` |
| `JiraToolkit` | `langchain_community.agent_toolkits.jira.toolkit` |
| `JsonToolkit` | `langchain_community.agent_toolkits.json.toolkit` |
| `MultionToolkit` | `langchain_community.agent_toolkits.multion.toolkit` |
| `NasaToolkit` | `langchain_community.agent_toolkits.nasa.toolkit` |
| `NLAToolkit` | `langchain_community.agent_toolkits.nla.toolkit` |
| `O365Toolkit` | `langchain_community.agent_toolkits.office365.toolkit` |
| `OpenAPIToolkit` | `langchain_community.agent_toolkits.openapi.toolkit` |
| `PlayWrightBrowserToolkit` | `langchain_community.agent_toolkits.playwright.toolkit` |
| `PowerBIToolkit` | `langchain_community.agent_toolkits.powerbi.toolkit` |
| `SlackToolkit` | `langchain_community.agent_toolkits.slack.toolkit` |
| `SteamToolkit` | `langchain_community.agent_toolkits.steam.toolkit` |
| `SQLDatabaseToolkit` | `langchain_community.agent_toolkits.sql.toolkit` |
| `SparkSQLToolkit` | `langchain_community.agent_toolkits.spark_sql.toolkit` |
| `ZapierToolkit` | `langchain_community.agent_toolkits.zapier.toolkit` |
| `create_json_agent` | `langchain_community.agent_toolkits.json.base` |
| `create_openapi_agent` | `langchain_community.agent_toolkits.openapi.base` |
| `create_pbi_agent` | `langchain_community.agent_toolkits.powerbi.base` |
| `create_pbi_chat_agent` | `langchain_community.agent_toolkits.powerbi.chat_base` |
| `create_spark_sql_agent` | `langchain_community.agent_toolkits.spark_sql.base` |
| `create_sql_agent` | `langchain_community.agent_toolkits.sql.base` |

### 2. 迁移至 `langchain_experimental`
以下代理创建函数已迁移到 `langchain_experimental`，直接调用会抛出 `ImportError` 并提示迁移：
- `create_csv_agent`
- `create_pandas_dataframe_agent`
- `create_xorbits_agent`
- `create_python_agent`
- `create_spark_dataframe_agent`

## 安全警告

在开发应用程序时，开发者应检查给定代理工具包底层工具的功能和权限，并确定该工具包的权限是否适合该应用程序。

更多信息请参见 [LangChain 安全策略](https://docs.langchain.com/oss/python/security-policy)。
