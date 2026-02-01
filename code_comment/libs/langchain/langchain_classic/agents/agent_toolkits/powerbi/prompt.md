# libs\langchain\langchain_classic\agents\agent_toolkits\powerbi\prompt.py

此文档提供了 `libs\langchain\langchain_classic\agents\agent_toolkits\powerbi\prompt.py` 文件的详细中文注释。该模块定义了 PowerBI 代理使用的各种提示词模板常量。

## 核心说明：动态重定向

该模块已弃用，所有提示词常量已通过动态导入机制重定向至 `langchain_community`。

### 导出常量

以下常量在 `DEPRECATED_LOOKUP` 中注册，并在访问时触发弃用警告：

- **标准代理提示词 (Standard Agent Prompts)**:
    *   **`POWERBI_PREFIX`**: 代理的系统提示词前缀。它规定了代理作为 PowerBI 专家的身份，并提供了如何利用 API 工具查询数据集、处理表结构和生成查询结果的行为准则。
    *   **`POWERBI_SUFFIX`**: 提示词后缀，包含对 ReAct 推理路径（Thought/Action/Observation）的引导和输出格式要求。

- **聊天代理提示词 (Chat Agent Prompts)**:
    *   **`POWERBI_CHAT_PREFIX`**: 专为基于聊天的代理（`create_pbi_chat_agent`）设计的系统提示词前缀，强调了对话上下文和多轮交互。
    *   **`POWERBI_CHAT_SUFFIX`**: 聊天代理的提示词后缀，优化了在聊天界面下的交互体验和结果展示。

## 源码实现机制

该模块利用 `create_importer` 实现动态属性查找：

```python
DEPRECATED_LOOKUP = {
    "POWERBI_CHAT_PREFIX": "langchain_community.agent_toolkits.powerbi.prompt",
    "POWERBI_CHAT_SUFFIX": "langchain_community.agent_toolkits.powerbi.prompt",
    "POWERBI_PREFIX": "langchain_community.agent_toolkits.powerbi.prompt",
    "POWERBI_SUFFIX": "langchain_community.agent_toolkits.powerbi.prompt",
}

_import_attribute = create_importer(__package__, deprecated_lookups=DEPRECATED_LOOKUP)

def __getattr__(name: str) -> Any:
    return _import_attribute(name)
```

## 迁移建议

为了避免弃用警告并使用最新版本的提示词，请直接从社区包导入：

```python
from langchain_community.agent_toolkits.powerbi.prompt import (
    POWERBI_PREFIX,
    POWERBI_CHAT_PREFIX
)
```
