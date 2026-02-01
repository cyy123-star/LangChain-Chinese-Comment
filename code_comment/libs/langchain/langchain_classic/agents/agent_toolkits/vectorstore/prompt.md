# libs\langchain\langchain_classic\agents\agent_toolkits\vectorstore\prompt.py

此文档提供了 `libs\langchain\langchain_classic\agents\agent_toolkits\vectorstore\prompt.py` 文件的详细中文注释。该模块定义了向量存储代理所使用的默认提示词模板。

## 核心常量

### 1. `PREFIX` (基础代理前缀)
这是单向量库代理的默认角色定义。
- **内容摘要**:
  - 明确代理是一个专门用于回答文档集相关问题的助手。
  - 告知代理可以使用工具与文档交互，输入是问题。
  - 规定了当需要来源时，应使用带来源的工具。
  - **关键约束**: 如果问题与提供的工具无关，代理必须返回 "I don't know"（我不知道），以防止幻觉。

### 2. `ROUTER_PREFIX` (路由代理前缀)
这是多向量库路由代理的默认角色定义。
- **内容摘要**:
  - 明确代理的主要任务是决定哪一个工具（哪一个库）与当前问题最相关。
  - **高级能力**: 允许代理将复杂问题拆分为子问题，并分别使用不同工具回答。

## 使用方法

这些前缀通常作为 `create_vectorstore_agent` 函数的 `prefix` 参数传入，最终被注入到代理的系统提示词（System Prompt）中。

## 提示词工程要点

- **明确限制**: 通过显式告诉代理 "I don't know"，降低了代理在知识库之外胡乱猜测的可能性。
- **任务导向**: 提示词聚焦于“工具选择”和“文档交互”，确保代理不会偏离作为文档助手的职责。
