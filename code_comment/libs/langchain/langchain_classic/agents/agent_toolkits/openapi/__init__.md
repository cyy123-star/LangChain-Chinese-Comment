# libs\langchain\langchain_classic\agents\agent_toolkits\openapi\__init__.py

此文档提供了 `libs\langchain\langchain_classic\agents\agent_toolkits\openapi\__init__.py` 文件的详细中文注释。该文件是 OpenAPI 工具包的入口。

## 模块概述

OpenAPI 工具包允许 LLM 与任何遵循 OpenAPI (Swagger) 规范的 API 进行交互。代理可以自动理解 API 的端点描述、参数要求和数据结构，并根据自然语言指令发起相应的 HTTP 请求。

## 主要组件

- **`create_openapi_agent`**: 创建 OpenAPI 代理的核心入口。
- **`OpenAPIToolkit`**: 提供 API 交互所需的工具集合。
- **`ReducedOpenAPISpec`**: 规范解析与精简工具。

## 迁移状态

所有核心功能均已迁移至 `langchain_community.agent_toolkits.openapi`。
