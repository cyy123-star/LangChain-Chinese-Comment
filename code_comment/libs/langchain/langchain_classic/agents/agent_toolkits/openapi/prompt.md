# libs\langchain\langchain_classic\agents\agent_toolkits\openapi\prompt.py

此文档提供了 `libs\langchain\langchain_classic\agents\agent_toolkits\openapi\prompt.py` 文件的详细中文注释。该模块定义了 OpenAPI 代理使用的基础提示词模板常量。

## 核心说明：动态重定向

该模块已弃用，所有提示词常量已通过动态导入机制重定向至 `langchain_community`。

### 导出常量

以下常量在 `DEPRECATED_LOOKUP` 中注册，并在访问时触发弃用警告：

- **`OPENAPI_PREFIX`**: 
    *   **用途**: OpenAPI 代理的基础系统提示词前缀。
    *   **核心逻辑**: 强调代理应优先使用工具获取 API 结构信息，严禁幻觉 API 端点。
- **`OPENAPI_SUFFIX`**: 
    *   **用途**: 提示词后缀。
    *   **内容**: 包含 `Thought`, `Action`, `Action Input`, `Observation` 等 ReAct 框架的格式引导。
- **`DESCRIPTION`**: 
    *   **用途**: 对该代理工具集的通用描述，帮助 `AgentExecutor` 识别该工具包的能力范围。

## 源码实现机制

该模块利用 `create_importer` 实现动态属性查找：

```python
DEPRECATED_LOOKUP = {
    "DESCRIPTION": "langchain_community.agent_toolkits.openapi.prompt",
    "OPENAPI_PREFIX": "langchain_community.agent_toolkits.openapi.prompt",
    "OPENAPI_SUFFIX": "langchain_community.agent_toolkits.openapi.prompt",
}

_import_attribute = create_importer(__package__, deprecated_lookups=DEPRECATED_LOOKUP)

def __getattr__(name: str) -> Any:
    return _import_attribute(name)
```

## 迁移建议

为了避免弃用警告并使用最新版本的提示词，请直接从社区包导入：

```python
from langchain_community.agent_toolkits.openapi.prompt import (
    OPENAPI_PREFIX, 
    OPENAPI_SUFFIX
)
```
