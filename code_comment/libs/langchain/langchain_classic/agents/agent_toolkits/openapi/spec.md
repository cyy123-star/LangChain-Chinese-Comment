# libs\langchain\langchain_classic\agents\agent_toolkits\openapi\spec.py

此文档提供了 `libs\langchain\langchain_classic\agents\agent_toolkits\openapi\spec.py` 文件的详细中文注释。该模块定义了用于表示和精简解析 OpenAPI 规范的数据结构与函数。

## 核心说明：动态重定向

该模块已弃用，其内部定义的规范处理类和函数已通过动态导入机制重定向至 `langchain_community`。

### 导出内容

以下内容在 `DEPRECATED_LOOKUP` 中注册，并在访问时触发弃用警告：

- **`ReducedOpenAPISpec`**: 
    *   **类型**: 数据类/类。
    *   **关键属性**:
        *   `servers`: API 服务器列表。
        *   `description`: API 整体描述。
        *   `endpoints`: 精简后的端点信息列表，每个端点包含 `path`, `name`, `description`, `params` 等。
    *   **功能**: 一个精简版的 OpenAPI 规范表示。它提取了代理运行所必需的关键信息，从而显著减少了传递给大语言模型（LLM）的上下文长度（Token 数量）。
- **`reduce_openapi_spec`**: 
    *   **类型**: 函数。
    *   **签名**: `def reduce_openapi_spec(spec: dict, dereference: bool = True) -> ReducedOpenAPISpec`
    *   **功能**: 将原始的、通常非常庞大的 OpenAPI JSON/YAML 规范文件解析并转换为 `ReducedOpenAPISpec` 对象的工具函数。

## 源码实现机制

该模块利用 `create_importer` 实现动态重定向：

```python
DEPRECATED_LOOKUP = {
    "ReducedOpenAPISpec": "langchain_community.agent_toolkits.openapi.spec",
    "reduce_openapi_spec": "langchain_community.agent_toolkits.openapi.spec",
}

_import_attribute = create_importer(__package__, deprecated_lookups=DEPRECATED_LOOKUP)

def __getattr__(name: str) -> Any:
    return _import_attribute(name)
```

## 迁移建议

为了保持代码的现代性并避免弃用警告，请直接从社区包导入：

```python
from langchain_community.agent_toolkits.openapi.spec import (
    ReducedOpenAPISpec,
    reduce_openapi_spec
)
```
