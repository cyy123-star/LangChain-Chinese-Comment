# libs\langchain\langchain_classic\agents\agent_toolkits\powerbi\toolkit.py

此文档提供了 `libs\langchain\langchain_classic\agents\agent_toolkits\powerbi\toolkit.py` 文件的详细中文注释。该模块定义了 PowerBI 工具集。

## 核心说明：动态重定向

该模块中的核心类已重定向至 `langchain_community`。

### 导出类
- **`PowerBIToolkit`**: 
  - **功能**: 封装了一系列与 PowerBI 交互的工具。
  - **初始化**:
    ```python
    def __init__(
        self,
        powerbi: PowerBIDataset,
        llm: BaseLanguageModel,
        examples: Optional[str] = None,
        max_iterations: int = 5,
        callback_manager: Optional[BaseCallbackManager] = None,
    ):
    ```
  - **包含工具**:
    - `list_powerbi_datasets`: 列出所有可用的数据集。
    - `get_powerbi_dataset_schema`: 获取指定数据集的表结构和列信息。
    - `query_powerbi_dataset`: 执行 DAX 查询并获取结果。
    - `get_powerbi_dataset_description`: 获取数据集的描述信息。

## 迁移建议

建议直接从社区包导入：
```python
from langchain_community.agent_toolkits.powerbi.toolkit import PowerBIToolkit
```
