# libs\langchain\langchain_classic\agents\agent_toolkits\zapier\__init__.py

此文档提供了 `libs\langchain\langchain_classic\agents\agent_toolkits\zapier\__init__.py` 文件的详细中文注释。

## 功能描述

该初始化文件通过动态导入机制暴露了 `ZapierToolkit`。它是 Zapier 工具包的入口点。

## 导出内容

- `ZapierToolkit`: 用于与 Zapier NLA 交互的工具包。

## 动态导入

所有导出内容现在都指向 `langchain_community`。

```python
__all__ = [
    "ZapierToolkit",
]
```

## 注意事项

此模块仅用于向后兼容。新项目应直接从 `langchain_community.agent_toolkits.zapier` 导入。

