# libs\langchain\langchain_classic\agents\agent_toolkits\openapi\planner_prompt.py

此文档提供了 `libs\langchain\langchain_classic\agents\agent_toolkits\openapi\planner_prompt.py` 文件的详细中文注释。该模块定义了 OpenAPI 规划器（Planner）和控制器（Controller）使用的各种提示词模板常量。

## 核心说明：动态重定向

与 OpenAPI 模块的其他部分一样，此文件已弃用，所有提示词常量已通过动态导入机制重定向至 `langchain_community`。

### 导出常量

以下常量在 `DEPRECATED_LOOKUP` 中注册，涵盖了从规划到执行的各个环节：

- **核心指令 (Core Instructions)**:
    *   **`API_PLANNER_PROMPT`**: 
        *   **逻辑**: “给定 API 规范和用户问题，请创建一个包含步骤的计划。”
        *   **输出**: 一个结构化的计划列表。
    *   **`API_CONTROLLER_PROMPT`**: 
        *   **逻辑**: “给定计划和当前背景，请决定下一步执行哪个 API 调用。”
        *   **核心**: 负责实际的参数填充和工具选择。

- **解析提示词 (Parsing Prompts)**:
    *   针对不同 HTTP 方法的解析引导：`PARSING_GET_PROMPT`, `PARSING_POST_PROMPT` 等。
    *   **逻辑**: “这是 API 返回的原始 JSON，请根据用户需求提取关键信息。”

- **工具元数据 (Tool Metadata)**:
    *   `API_PLANNER_TOOL_DESCRIPTION`: 告知 LLM 这是一个可以生成多步 API 调用计划的工具。
    *   `API_CONTROLLER_TOOL_DESCRIPTION`: 告知 LLM 这是一个可以执行具体 API 请求的工具。

## 源码实现机制

该模块利用 `create_importer` 实现动态重定向：

```python
DEPRECATED_LOOKUP = {
    "API_PLANNER_PROMPT": "langchain_community.agent_toolkits.openapi.planner_prompt",
    "API_ORCHESTRATOR_PROMPT": "langchain_community.agent_toolkits.openapi.planner_prompt",
    # ... 其他 20 多个常量 ...
}

_import_attribute = create_importer(__package__, deprecated_lookups=DEPRECATED_LOOKUP)

def __getattr__(name: str) -> Any:
    return _import_attribute(name)
```

## 迁移建议

请直接从社区包导入：

```python
from langchain_community.agent_toolkits.openapi.planner_prompt import (
    API_PLANNER_PROMPT,
    API_ORCHESTRATOR_PROMPT,
    API_CONTROLLER_PROMPT
)
```
