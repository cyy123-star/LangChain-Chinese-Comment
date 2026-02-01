# libs\langchain\langchain_classic\agents\agent_toolkits\file_management\__init__.py

`file_management` 模块提供了用于本地文件系统操作的工具包。该模块目前已作为弃用模块，其核心实现已迁移至 `langchain_community`。

## 主要内容

- **FileManagementToolkit**: 整合了文件读取、写入、移动、删除、目录列表等功能的工具包。

## 迁移建议

该模块中的所有功能已迁移到 `langchain_community` 包中。建议开发者更新导入语句：

```python
# 弃用的导入方式
from langchain_classic.agents.agent_toolkits.file_management import FileManagementToolkit

# 推荐的导入方式
from langchain_community.agent_toolkits.file_management import FileManagementToolkit
```

## 注意事项

- **根目录限制**: 强烈建议在初始化工具包时指定 `root_dir`，以限制代理仅能访问特定的文件目录。
- **安全警告**: 文件管理工具具有破坏性（如删除、覆盖）。请确保代理的运行环境受到限制，并避免在包含敏感数据的目录中运行。
