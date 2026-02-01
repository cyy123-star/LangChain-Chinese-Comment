# libs\langchain\langchain_classic\agents\agent_toolkits\ainetwork\__init__.py

`ainetwork` 模块提供了用于与 AINetwork 区块链交互的工具包。该模块目前已作为弃用模块，其核心实现已迁移至 `langchain_community`。

## 主要内容

- **AINetworkToolkit**: 整合了 AINetwork 区块链的数据读取、写入和管理功能的工具包。

## 迁移建议

该模块中的所有功能已迁移到 `langchain_community` 包中。建议开发者更新导入语句：

```python
# 弃用的导入方式
from langchain_classic.agents.agent_toolkits.ainetwork import AINetworkToolkit

# 推荐的导入方式
from langchain_community.agent_toolkits.ainetwork import AINetworkToolkit
```

## 注意事项

- **环境依赖**: 使用此工具包需要安装 `ainetwork-sdk` 库。
- **区块链交互**: 代理可以直接操作区块链数据。请确保私钥安全，并在受控环境下运行。
- **权限管理**: AINetwork 的操作受限于账户权限和应用配置。
