# libs\langchain\langchain_classic\agents\agent_toolkits\slack\__init__.py

`slack` 模块提供了用于与 Slack API 交互的工具包。该模块目前已作为弃用模块，其核心实现已迁移至 `langchain_community`。

## 主要内容

- **SlackToolkit**: 整合了 Slack 消息发送、频道加入、搜索等功能的工具包。

## 迁移建议

该模块中的所有功能已迁移到 `langchain_community` 包中。建议开发者更新导入语句：

```python
# 弃用的导入方式
from langchain_classic.agents.agent_toolkits.slack import SlackToolkit

# 推荐的导入方式
from langchain_community.agent_toolkits.slack import SlackToolkit
```

## 注意事项

- **环境依赖**: 使用此工具包需要安装 `slack_sdk` 库。
- **凭据配置**: 必须在环境变量中正确设置 `SLACK_BOT_TOKEN`。
- **范围与权限**: 请确保您的 Slack App 拥有执行所需操作（如 `chat:write`, `channels:read`）的必要 OAuth Scopes。

