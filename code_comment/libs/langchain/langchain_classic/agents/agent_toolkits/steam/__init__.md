# libs\langchain\langchain_classic\agents\agent_toolkits\steam\__init__.py

`steam` 模块提供了用于与 Steam 游戏平台交互的工具包。该模块目前已作为弃用模块，其核心实现已迁移至 `langchain_community`。

## 主要内容

- **SteamToolkit**: 整合了 Steam 游戏搜索、用户资料检索、成就查看等功能的工具包。

## 迁移建议

该模块中的所有功能已迁移到 `langchain_community` 包中。建议开发者更新导入语句：

```python
# 弃用的导入方式
from langchain_classic.agents.agent_toolkits.steam import SteamToolkit

# 推荐的导入方式
from langchain_community.agent_toolkits.steam import SteamToolkit
```

## 注意事项

- **环境依赖**: 使用此工具包需要安装 `steamspypi` 库。
- **凭据配置**: 必须在环境变量中正确设置 `STEAM_KEY`。
- **数据来源**: 代理通过 Steam Web API 获取数据，受限于 API 的访问限制和隐私设置。

