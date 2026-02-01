# libs\langchain\langchain_classic\agents\agent_toolkits\powerbi\base.py

此文档提供了 `libs\langchain\langchain_classic\agents\agent_toolkits\powerbi\base.py` 文件的详细中文注释。该模块提供了创建 PowerBI 代理的工厂方法。

## 核心说明：动态重定向

该模块已弃用，其核心功能已通过动态导入机制重定向至 `langchain_community`。

### 导出功能

以下函数在 `DEPRECATED_LOOKUP` 中注册，并在访问时触发弃用警告：

- **`create_pbi_agent`**: 
    *   **功能**: 创建一个能够理解和操作 Microsoft PowerBI 报表、数据集及工作空间的智能代理。
    *   **函数原型**:
        ```python
        def create_pbi_agent(
            llm: BaseLanguageModel,
            toolkit: PowerBIToolkit,
            callback_manager: Optional[BaseCallbackManager] = None,
            prefix: str = POWERBI_PREFIX,
            suffix: str = POWERBI_SUFFIX,
            format_instructions: str = POWERBI_FORMAT_INSTRUCTIONS,
            input_variables: Optional[List[str]] = None,
            top_k: int = 10,
            verbose: bool = False,
            agent_executor_kwargs: Optional[Dict[str, Any]] = None,
            **kwargs: Any,
        ) -> AgentExecutor:
        ```
    *   **工作原理**: 代理利用 PowerBI 的 REST API 获取数据集结构和元数据，并根据用户的问题生成相应的查询逻辑（如 DAX 表达式），从而实现对企业数据的自然语言问答。

## 源码实现机制

该模块利用 `create_importer` 实现动态属性查找：

```python
DEPRECATED_LOOKUP = {
    "create_pbi_agent": "langchain_community.agent_toolkits.powerbi.base",
}

_import_attribute = create_importer(__package__, deprecated_lookups=DEPRECATED_LOOKUP)

def __getattr__(name: str) -> Any:
    return _import_attribute(name)
```

## 迁移建议

为了保持代码的现代性并避免弃用警告，请直接从社区包导入：

```python
from langchain_community.agent_toolkits.powerbi.base import create_pbi_agent
```
