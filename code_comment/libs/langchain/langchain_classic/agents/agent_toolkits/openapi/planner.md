# libs\langchain\langchain_classic\agents\agent_toolkits\openapi\planner.py

此文档提供了 `libs\langchain\langchain_classic\agents\agent_toolkits\openapi\planner.py` 文件的详细中文注释。该模块定义了用于规划和执行 API 请求的高级工具类。

## 核心说明：动态重定向

该模块已弃用，其内部定义的工具类和工厂函数已通过动态导入机制重定向至 `langchain_community`。

### 导出内容

以下类和函数在 `DEPRECATED_LOOKUP` 中注册，并在访问时触发弃用警告：

- **请求工具类 (Requests Tools with Parsing)**:
    *   **`RequestsGetToolWithParsing`**: 具备自动响应解析能力的 GET 请求工具。
    *   **`RequestsPostToolWithParsing`**: 具备自动响应解析能力的 POST 请求工具。
    *   **`RequestsPatchToolWithParsing`**: 具备自动响应解析能力的 PATCH 请求工具。
    *   **`RequestsPutToolWithParsing`**: 具备自动响应解析能力的 PUT 请求工具。
    *   **`RequestsDeleteToolWithParsing`**: 具备自动响应解析能力的 DELETE 请求工具。
    *   *特点*: 这些工具不仅执行 HTTP 请求，还能根据 API 规范对返回的复杂数据进行结构化处理或简化。
    *   *解析逻辑*: 内部通常使用 `llm_chain` 来根据提示词（如 `PARSING_GET_PROMPT`）对 API 返回的原始 JSON 文本进行“提取”或“总结”。

- **规划与执行组件**:
    *   **`create_openapi_agent`**: 创建 OpenAPI 代理的入口函数。
    *   **工作流**:
        1. **Planner**: 接收用户问题，查阅 API 规范，生成一个 API 调用计划。
        2. **Controller**: 接收计划，按顺序调用对应的 `RequestsTool`，并将结果反馈给 LLM。

## 源码实现机制

该模块利用 `create_importer` 实现动态属性查找：

```python
DEPRECATED_LOOKUP = {
    "RequestsGetToolWithParsing": "langchain_community.agent_toolkits.openapi.planner",
    "RequestsPostToolWithParsing": "langchain_community.agent_toolkits.openapi.planner",
    "RequestsPatchToolWithParsing": "langchain_community.agent_toolkits.openapi.planner",
    "RequestsPutToolWithParsing": "langchain_community.agent_toolkits.openapi.planner",
    "RequestsDeleteToolWithParsing": "langchain_community.agent_toolkits.openapi.planner",
    "create_openapi_agent": "langchain_community.agent_toolkits.openapi.planner",
}

_import_attribute = create_importer(__package__, deprecated_lookups=DEPRECATED_LOOKUP)

def __getattr__(name: str) -> Any:
    return _import_attribute(name)
```

## 迁移建议

为了保持代码的现代性并避免弃用警告，请直接从社区包导入：

```python
from langchain_community.agent_toolkits.openapi.planner import (
    RequestsGetToolWithParsing,
    RequestsPostToolWithParsing,
    create_openapi_agent
)
```
