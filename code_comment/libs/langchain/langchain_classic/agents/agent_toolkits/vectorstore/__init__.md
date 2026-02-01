# libs\langchain\langchain_classic\agents\agent_toolkits\vectorstore\__init__.py

此文档提供了 `libs\langchain\langchain_classic\agents\agent_toolkits\vectorstore\__init__.py` 文件的详细中文注释。

## 功能描述

该模块是用于与向量存储（Vector Stores）进行交互的代理工具包的入口点。它允许代理查询向量存储中的信息。

## 主要组件

- `create_vectorstore_agent`: 用于创建向量存储代理的工厂函数（位于 `base.py`）。
- `VectorStoreToolkit`: 用于与单个向量存储交互的工具包（位于 `toolkit.py`）。
- `VectorStoreRouterToolkit`: 用于在多个向量存储之间进行路由的工具包（位于 `toolkit.py`）。

## 注意事项

此模块中的功能已被标记为弃用，建议新项目使用 **LangGraph** 和 `create_react_agent` 来实现更灵活的向量存储查询代理。

