# libs\langchain\langchain_classic\agents\agent_toolkits\sql\__init__.py

此文档提供了 `libs\langchain\langchain_classic\agents\agent_toolkits\sql\__init__.py` 文件的详细中文注释。

## 功能描述

该模块是 SQL 代理工具包的入口点，旨在允许代理与 SQL 数据库进行交互。它可以自动发现表结构、执行查询并根据结果回答问题。

## 主要组件

- `create_sql_agent`: 创建 SQL 代理的核心函数。
- `SQLToolkit`: 包含数据库交互工具（查询、表信息、语法检查等）的工具包。

## 迁移指南

虽然此模块仍受支持，但建议新项目参考 [LangChain 官方文档](https://python.langchain.com/docs/how_to/sql_query/) 使用现代的 `create_react_agent` 和 `QuerySQLDatabaseTool` 来构建更强大的 SQL 代理。

