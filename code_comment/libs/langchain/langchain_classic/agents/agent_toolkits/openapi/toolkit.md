# libs\langchain\langchain_classic\agents\agent_toolkits\openapi\toolkit.py

此文档提供了 `libs\langchain\langchain_classic\agents\agent_toolkits\openapi\toolkit.py` 文件的详细中文注释。该模块定义了用于与 RESTful API 进行 OpenAPI 交互的工具包。

## 核心说明：动态重定向

该模块已弃用，其核心工具包类已通过动态导入机制重定向至 `langchain_community`。

### 导出类

以下类在 `DEPRECATED_LOOKUP` 中注册，并在访问时触发弃用警告：

- **`OpenAPIToolkit`**: 
    *   **功能**: 封装了一组基于 OpenAPI 规范生成的工具。
    *   **初始化**:
        ```python
        def from_llm(
            cls,
            llm: BaseLanguageModel,
            spec: ReducedOpenAPISpec,
            requests_wrapper: TextRequestsWrapper,
            allow_dangerous_requests: bool = False,
            **kwargs: Any,
        ) -> "OpenAPIToolkit":
        ```
    *   **内容**: 它通常持有 API 规范的引用，并能够动态生成用于执行特定 API 操作的工具（如 `RequestsGetToolWithParsing` 等）。
- **`RequestsToolkit`**: 
    *   **功能**: 一个更通用的工具包，提供基础的 HTTP 请求能力（GET, POST 等），通常被 `OpenAPIToolkit` 内部使用或作为其基础。
    *   **包含工具**: `RequestsGetTool`, `RequestsPostTool`, `RequestsPatchTool`, `RequestsPutTool`, `RequestsDeleteTool`。

## 源码实现机制

该模块利用 `create_importer` 实现动态属性查找：

```python
DEPRECATED_LOOKUP = {
    "RequestsToolkit": "langchain_community.agent_toolkits.openapi.toolkit",
    "OpenAPIToolkit": "langchain_community.agent_toolkits.openapi.toolkit",
}

_import_attribute = create_importer(__package__, deprecated_lookups=DEPRECATED_LOOKUP)

def __getattr__(name: str) -> Any:
    return _import_attribute(name)
```

## 迁移建议

为了保持代码的现代性并避免弃用警告，请直接从社区包导入：

```python
from langchain_community.agent_toolkits.openapi.toolkit import (
    OpenAPIToolkit,
    RequestsToolkit
)
```
