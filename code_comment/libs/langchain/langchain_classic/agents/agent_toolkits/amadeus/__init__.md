# libs\langchain\langchain_classic\agents\agent_toolkits\amadeus\__init__.py

`amadeus` 模块提供了用于与 Amadeus 旅游服务 API 交互的工具包。该模块目前已作为弃用模块，其核心实现已迁移至 `langchain_community`。

## 主要内容

- **AmadeusToolkit**: 整合了航班搜索、酒店搜索、租车搜索等旅游相关功能的工具包。

## 迁移建议

该模块中的所有功能已迁移到 `langchain_community` 包中。建议开发者更新导入语句：

```python
# 弃用的导入方式
from langchain_classic.agents.agent_toolkits.amadeus import AmadeusToolkit

# 推荐的导入方式
from langchain_community.agent_toolkits.amadeus import AmadeusToolkit
```

## 注意事项

- **环境依赖**: 使用此工具包需要安装 `amadeus` 库。
- **凭据配置**: 必须在环境变量中设置 `AMADEUS_CLIENT_ID` 和 `AMADEUS_CLIENT_SECRET`。
- **服务限制**: API 调用受 Amadeus 平台的配额和费率限制。
