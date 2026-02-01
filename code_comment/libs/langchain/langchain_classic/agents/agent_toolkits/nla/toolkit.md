# libs\langchain\langchain_classic\agents\agent_toolkits\nla\toolkit.py

`nla/toolkit.py` 模块定义了 `NLAToolkit` 类，该类整合了多个自然语言 API 工具，提供了一种简便的方式来创建能够理解自然语言的 API 代理。

## 核心类

### `NLAToolkit`

`NLAToolkit` 继承自 `BaseToolkit`，它充当 `NLATool` 实例的容器和管理器。

#### 核心方法

##### `get_tools`

返回工具包中包含的所有 `NLATool` 实例。

```python
def get_tools(self) -> List[BaseTool]:
    """获取工具列表。"""
    return self.nla_tools
```

##### `from_toolkit_and_tools` (工厂方法)

允许从现有的工具包和工具列表中构建 `NLAToolkit`。

## 动态导入机制

该文件使用了 `create_importer` 实现了动态属性查找。当开发者尝试从 `langchain_classic` 导入 `NLAToolkit` 时，系统会发出弃用警告，并自动重定向到 `langchain_community.agent_toolkits.nla.toolkit`。

```python
DEPRECATED_LOOKUP = {"NLAToolkit": "langchain_community.agent_toolkits.nla.toolkit"}

# 动态属性查找逻辑
_import_attribute = create_importer(__package__, deprecated_lookups=DEPRECATED_LOOKUP)

def __getattr__(name: str) -> Any:
    """动态获取属性。"""
    return _import_attribute(name)
```

## 迁移指南

由于该模块已被弃用，建议直接从 `langchain_community` 导入：

```python
from langchain_community.agent_toolkits.nla.toolkit import NLAToolkit
```

## 注意事项

- **动态构建**: `NLAToolkit` 的强大之处在于它可以从 OpenAPI 规范或其他 API 描述文档中动态构建，从而快速生成支持自然语言的代理。
- **组合能力**: 可以将多个不同服务的 NLA 工具组合在一个 `NLAToolkit` 中，实现跨服务的自然语言交互。
- **Token 消耗**: 由于 NLA 工具在请求和响应阶段都可能涉及 LLM 调用，因此在使用时需要注意 Token 消耗和延迟。

