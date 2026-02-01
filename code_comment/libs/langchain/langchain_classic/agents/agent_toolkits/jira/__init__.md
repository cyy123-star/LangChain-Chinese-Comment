# libs\langchain\langchain_classic\agents\agent_toolkits\jira\__init__.py

此文档提供了 `libs\langchain\langchain_classic\agents\agent_toolkits\jira\__init__.py` 文件的详细中文注释。该模块是 Jira 工具包的入口点。

## 功能描述

该模块负责 Jira 工具包的相关功能实现。它提供了一组用于与 Atlassian Jira 任务管理系统交互的工具，允许代理执行诸如创建、更新、搜索 Issue 以及添加评论等操作。

## 主要组件

- **`JiraToolkit`**: 提供 Jira 交互的一站式工具包，集成了多个专门的 Jira 操作工具。

## 弃用说明

该模块已被标记为弃用，并已迁移到 `langchain_community` 包中。

- **弃用警告**: 使用此模块时会触发 `LangChainDeprecationWarning`。
- **推荐做法**: 建议使用 `langchain_community.agent_toolkits.jira` 代替。

## 核心逻辑

该文件使用 `create_importer` 实现了动态导入机制，用于处理弃用警告。所有 Jira 相关的类均已映射到 `langchain_community`。

### 导出映射 (DEPRECATED_LOOKUP)

```python
DEPRECATED_LOOKUP = {
    "JiraToolkit": "langchain_community.agent_toolkits.jira.toolkit",
}
```

当访问 `JiraToolkit` 时，系统会自动从 `langchain_community` 中导入并发出弃用警告。

## 迁移示例

### 弃用的方式
```python
from langchain_classic.agents.agent_toolkits.jira import JiraToolkit
```

### 推荐的方式
```python
from langchain_community.agent_toolkits.jira import JiraToolkit
```

