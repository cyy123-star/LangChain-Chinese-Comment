# libs\langchain\langchain_classic\agents\tools.py

此文档提供了 `libs\langchain\langchain_classic\agents\tools.py` 文件的详细中文注释。该模块定义了代理在遇到错误时使用的特殊工具。

## 功能描述

在代理的执行过程中，模型有时会产生幻觉，调用一个并不存在的工具。为了防止程序直接崩溃，LangChain 提供了一个专门的辅助工具来引导模型修正错误。

## 核心类：`InvalidTool`

`InvalidTool` 是一个容错工具，当 `AgentExecutor` 无法找到模型请求的工具时，会调用此类。

### 1. 核心属性
- **`name`**: `invalid_tool`
- **`description`**: 当工具名无效时调用，用于向模型建议正确的工具名。

### 2. 运行逻辑

无论同步还是异步执行，该工具都会执行以下逻辑：
1. 接收无效的工具名 `requested_tool_name` 和可用工具列表 `available_tool_names`。
2. 返回一段描述性文字，指出请求无效，并列出所有可用的选项。

**示例返回**:
> `google_search` is not a valid tool, try one of [`search`, `calculator`].

## 意义与作用

- **增强鲁棒性**: 防止因模型幻觉导致的执行中断。
- **反馈机制**: 将错误作为一种“观察结果”（Observation）反馈给模型，让模型有机会在下一次“思考”（Thought）中修正自己的行为。

## 导出组件

- `InvalidTool`: 异常处理工具类。
- `tool`: 装饰器，用于将普通的 Python 函数快速转换为 LangChain 工具。

