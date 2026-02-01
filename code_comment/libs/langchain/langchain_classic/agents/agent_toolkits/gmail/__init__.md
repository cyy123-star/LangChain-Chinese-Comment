# libs\langchain\langchain_classic\agents\agent_toolkits\gmail\__init__.py

此文档提供了 `libs\langchain\langchain_classic\agents\agent_toolkits\gmail\__init__.py` 文件的详细中文注释。该模块是 Gmail 工具包的入口点。

## 功能描述

该模块负责 Gmail 工具包的相关功能实现。它提供了一组用于与 Gmail 邮件服务交互的工具，允许代理执行诸如发送邮件、阅读邮件、搜索邮件以及管理草稿等常见操作。

## 主要组件

- **`GmailToolkit`**: 提供 Gmail 交互的一站式工具包，集成了多个专门的 Gmail 操作工具。

## 弃用说明

该模块已被标记为弃用，并已迁移到 `langchain_community` 包中。

- **弃用警告**: 使用此模块时会触发 `LangChainDeprecationWarning`。
- **推荐做法**: 建议使用 `langchain_community.agent_toolkits.gmail` 代替。

## 核心逻辑

该文件使用 `create_importer` 实现了动态导入机制，用于处理弃用警告。所有 Gmail 相关的类均已映射到 `langchain_community`。

### 导出映射 (DEPRECATED_LOOKUP)

```python
DEPRECATED_LOOKUP = {
    "GmailToolkit": "langchain_community.agent_toolkits.gmail.toolkit",
}
```

当访问 `GmailToolkit` 时，系统会自动从 `langchain_community` 中导入并发出弃用警告。

## 迁移示例

### 弃用的方式
```python
from langchain_classic.agents.agent_toolkits.gmail import GmailToolkit
```

### 推荐的方式
```python
from langchain_community.agent_toolkits.gmail import GmailToolkit
```

