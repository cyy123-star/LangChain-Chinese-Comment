# libs\langchain\langchain_classic\agents\agent_toolkits\clickup\__init__.py

`clickup` 模块提供了用于与 ClickUp 生产力平台交互的工具包。该模块目前已作为弃用模块，其核心实现已迁移至 `langchain_community`。

## 主要内容

- **ClickupToolkit**: 整合了 ClickUp 任务管理、列表操作、团队信息检索等功能的工具包。

## 迁移建议

该模块中的所有功能已迁移到 `langchain_community` 包中。建议开发者更新导入语句：

```python
# 弃用的导入方式
from langchain_classic.agents.agent_toolkits.clickup import ClickupToolkit

# 推荐的导入方式
from langchain_community.agent_toolkits.clickup import ClickupToolkit
```

## 注意事项

- **环境依赖**: 使用此工具包需要安装 `pyclickup` 库。
- **凭据配置**: 必须在环境变量中正确设置 `CLICKUP_ACCESS_TOKEN`。
- **操作权限**: 请确保您的 ClickUp 令牌拥有操作对应工作区（Workspace）和列表（List）的权限。
