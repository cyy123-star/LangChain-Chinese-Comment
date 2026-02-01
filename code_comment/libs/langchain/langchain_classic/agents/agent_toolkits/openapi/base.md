# libs\langchain\langchain_classic\agents\agent_toolkits\openapi\base.py

此文档提供了 `libs\langchain\langchain_classic\agents\agent_toolkits\openapi\base.py` 文件的详细中文注释。该模块提供了创建 OpenAPI 代理的工厂方法。

## 核心说明：动态重定向

与 `agent_toolkits` 中的其他模块一致，此模块已弃用，其核心功能通过动态导入机制重定向至 `langchain_community`。

### 导出功能

以下函数在 `DEPRECATED_LOOKUP` 中注册，并在访问时触发弃用警告：

- **`create_openapi_agent`**: 
    *   **功能**: 创建一个能够理解 OpenAPI/Swagger 规范并能与 RESTful API 进行交互的智能代理。
    *   **函数原型**:
        ```python
        def create_openapi_agent(
            llm: BaseLanguageModel,
            toolkit: OpenAPIToolkit,
            callback_manager: Optional[BaseCallbackManager] = None,
            prefix: str = OPENAPI_PREFIX,
            suffix: str = OPENAPI_SUFFIX,
            format_instructions: str = OPENAPI_FORMAT_INSTRUCTIONS,
            input_variables: Optional[List[str]] = None,
            max_iterations: Optional[int] = 15,
            max_execution_time: Optional[float] = None,
            early_stopping_method: str = "force",
            verbose: bool = False,
            return_intermediate_steps: bool = False,
            agent_executor_kwargs: Optional[Dict[str, Any]] = None,
            **kwargs: Any,
        ) -> AgentExecutor:
        ```
    *   **工作机制**: 代理会解析提供的 API 规范（通常经过简化），自动识别可用的路径（Paths）和操作（Operations），并利用底层的 HTTP 请求工具执行具体的 API 调用来回答用户问题。

## 源码实现机制

该模块使用 `create_importer` 实现了对弃用属性的动态拦截：

```python
DEPRECATED_LOOKUP = {
    "create_openapi_agent": "langchain_community.agent_toolkits.openapi.base",
}

_import_attribute = create_importer(__package__, deprecated_lookups=DEPRECATED_LOOKUP)

def __getattr__(name: str) -> Any:
    return _import_attribute(name)
```

## 迁移建议

为了保持代码的现代性并避免弃用警告，请直接从 `langchain_community` 导入：

```python
from langchain_community.agent_toolkits.openapi.base import create_openapi_agent
```
