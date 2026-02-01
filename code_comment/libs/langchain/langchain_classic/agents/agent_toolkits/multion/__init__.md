# libs\langchain\langchain_classic\agents\agent_toolkits\multion\__init__.py

此文档提供了 `libs\langchain\langchain_classic\agents\agent_toolkits\multion\__init__.py` 文件的详细中文注释。该模块是 MultiOn 工具包的入口点。

## 功能描述

该模块负责 MultiOn 工具包的相关功能实现。MultiOn 是一个 AI 代理，可以浏览网页并代表用户执行操作。此工具包允许代理与 MultiOn API 交互，以自动化复杂的 Web 任务。

## 主要组件

- `MultionToolkit`: 提供与 MultiOn 服务交互的一组工具。

## 弃用说明

该模块已被标记为弃用，并已迁移到 `langchain_community` 包中。建议使用 `langchain_community.agent_toolkits.multion` 代替。

## 核心逻辑

该文件使用 `create_importer` 实现了动态导入机制，用于处理弃用警告。

```python
DEPRECATED_LOOKUP = {
    "MultionToolkit": "langchain_community.agent_toolkits.multion.toolkit",
}
```

当访问 `MultionToolkit` 时，系统会自动从 `langchain_community` 中导入并发出弃用警告。

