# libs\langchain\langchain_classic\agents\agent_toolkits\multion\toolkit.py

`multion/toolkit.py` 模块定义了 `MultionToolkit` 类，该类整合了多个用于 Web 自动化的工具。

## 核心类

### `MultionToolkit`

`MultionToolkit` 为代理提供了与 MultiOn 服务交互的能力，实现浏览器自动化任务。

#### 主要工具

通常包含以下工具：
- `create_session`: 启动一个新的 Web 浏览器会话。
- `update_session`: 更新现有的会话，执行点击、输入或导航等操作。
- `list_sessions`: 列出当前活跃的会话。

## 动态导入机制

该文件使用了 `create_importer` 实现了动态属性查找。当开发者尝试从 `langchain_classic` 导入 `MultionToolkit` 时，系统会发出弃用警告，并自动重定向到 `langchain_community.agent_toolkits.multion.toolkit`。

```python
DEPRECATED_LOOKUP = {
    "MultionToolkit": "langchain_community.agent_toolkits.multion.toolkit",
}
```

## 迁移指南

由于该模块已被弃用，建议直接从 `langchain_community` 导入：

```python
from langchain_community.agent_toolkits.multion.toolkit import MultionToolkit
```

## 注意事项

- **API 密钥**: 必须设置 `MULTION_API_KEY` 环境变量或在初始化时提供。
- **Web 自动化**: 代理将能够根据自然语言指令在真实网站上执行操作。

