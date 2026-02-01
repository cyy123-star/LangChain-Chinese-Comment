# libs\langchain\langchain_classic\agents\agent_toolkits\json\__init__.py

`json` 模块提供了用于与 JSON 数据进行交互的工具包。该模块目前已作为弃用模块，其核心实现已迁移至 `langchain_community`。

## 主要内容

- **JsonToolkit**: 包含了一系列用于操作和查询 JSON 数据的工具。
- **create_json_agent**: 用于创建专门处理 JSON 数据的代理的工厂函数。

## 迁移建议

该模块中的所有功能已迁移到 `langchain_community` 包中。建议开发者更新导入语句：

```python
# 弃用的导入方式
from langchain_classic.agents.agent_toolkits.json import JsonToolkit, create_json_agent

# 推荐的导入方式
from langchain_community.agent_toolkits.json import JsonToolkit, create_json_agent
```

## 注意事项

- **分层导航**: JSON 代理采用“分层导航”策略。它不是将整个 JSON 塞进 Prompt，而是像人类查阅文件一样，先看目录（List Keys），再读细节（Get Value）。
- **Token 优化**: 这种按需读取的方式极大地节省了 Token，使得处理超大 JSON 成为可能。
- **JsonSpec**: 使用时必须先定义 `JsonSpec(dict_=data, max_value_length=4000)`，其中 `max_value_length` 可以防止单个值过大撑爆上下文。
