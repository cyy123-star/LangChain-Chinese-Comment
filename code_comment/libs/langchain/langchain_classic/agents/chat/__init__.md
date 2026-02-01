# libs\langchain\langchain_classic\agents\chat\__init__.py

此文档提供了 `libs\langchain\langchain_classic\agents\chat\__init__.py` 文件的详细中文注释。该模块是专门为对话模型（Chat Models）设计的代理（Agent）入口。

## 功能描述

该模块定义了 `ChatAgent` 及其相关的输出解析器。与传统的文本代理不同，`ChatAgent` 引导对话模型输出结构化的 JSON 代码块来执行工具。这种方式在现代聊天 LLM（如 GPT-3.5/4）中表现更加稳定。

### 核心特性

- **结构化输出**: 要求模型在 Markdown 代码块中输出 JSON。
- **对话优化**: 提示词结构适配 Chat Models 的 System/Human/AI 消息模式。
- **动态导入**: 使用 `create_importer` 实现了平滑的弃用和迁移机制。

## 主要组件

- **`ChatAgent`**: 核心代理类，负责构建提示词和管理执行流程。
- **`ChatOutputParser`**: 专门用于解析模型生成的 JSON 代码块并将其转换为 `AgentAction` 或 `AgentFinish`。

## 弃用说明

⚠️ **注意**: 该模块已被标记为弃用。

- **弃用原因**: 随着 OpenAI 函数调用（Function Calling）和通用工具调用（Tool Calling）功能的普及，LangChain 引入了更强大、更通用的代理类型。
- **现代替代方案**:
    - **`create_tool_calling_agent`**: 推荐的首选方案，支持多工具并行调用。
    - **`create_structured_chat_agent`**: 如果模型不支持原生的工具调用，但擅长处理结构化输出，建议使用此替代方案。

## 核心逻辑

该文件利用 `create_importer` 处理弃用重定向：

```python
DEPRECATED_LOOKUP = {
    "ChatAgent": "langchain.agents.chat.base",
    "ChatOutputParser": "langchain.agents.chat.output_parser",
}

# 动态属性查找
_import_attribute = create_importer(__package__, deprecated_lookups=DEPRECATED_LOOKUP)

def __getattr__(name: str) -> Any:
    return _import_attribute(name)
```

## 迁移指南

```python
# 旧写法 (不推荐)
from langchain.agents.chat.base import ChatAgent

# 现代写法 (推荐 - 使用 Tool Calling)
from langchain.agents import create_tool_calling_agent
```
