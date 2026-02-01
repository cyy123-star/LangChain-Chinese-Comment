# libs\langchain\langchain_classic\agents\agent_toolkits\powerbi\__init__.py

`powerbi` 模块提供了用于与 Microsoft PowerBI 交互的工具包。该模块目前已作为弃用模块，其核心实现已迁移至 `langchain_community`。

## 主要内容

- **PowerBIToolkit**: 整合了操作 PowerBI 数据集、表和查询的工具。
- **create_pbi_agent**: 创建通用 PowerBI 代理。
- **create_pbi_chat_agent**: 创建专为聊天优化的 PowerBI 代理。

## 迁移建议

该模块中的所有功能已迁移到 `langchain_community` 包中。建议开发者更新导入语句：

```python
# 弃用的导入方式
from langchain_classic.agents.agent_toolkits.powerbi import PowerBIToolkit, create_pbi_agent

# 推荐的导入方式
from langchain_community.agent_toolkits.powerbi import PowerBIToolkit, create_pbi_agent
```

## 注意事项

- **身份验证**: 使用 PowerBI 工具包通常需要配置 Azure AD 身份验证，并提供访问令牌或服务主体凭据。
- **权限控制**: 代理的操作受限于所使用的 PowerBI 账号权限（如工作区访问权、数据集查询权）。
- **查询生成**: 代理会根据用户自然语言生成 DAX 或其他查询语言，建议在受控环境中测试。
