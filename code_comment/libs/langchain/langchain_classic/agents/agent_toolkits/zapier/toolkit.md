# libs\langchain\langchain_classic\agents\agent_toolkits\zapier\toolkit.py

此文档提供了 `libs\langchain\langchain_classic\agents\agent_toolkits\zapier\toolkit.py` 文件的详细中文注释。该模块已被弃用，并重定向到 `langchain_community`。

## 功能描述

该模块定义了 `ZapierToolkit`，它是一个用于与 Zapier Natural Language Actions (NLA) API 交互的工具包。Zapier NLA 允许代理通过自然语言调用 Zapier 上的 5000 多个应用程序和 20000 多个操作。通过动态导入机制，它现在指向 `langchain_community.agent_toolkits.zapier.toolkit`。

## 弃用说明

该模块已被移动到 `langchain_community`。
- **原始导入路径**: `langchain_classic.agents.agent_toolkits.zapier.toolkit.ZapierToolkit`
- **建议导入路径**: `langchain_community.agent_toolkits.zapier.toolkit.ZapierToolkit`

## 主要类

### ZapierToolkit

用于与 Zapier NLA 交互的工具包。它通过 ZapierNLAWrapper 封装了与 Zapier API 的通信。

## 动态导入机制

模块使用 `create_importer` 实现动态加载，以确保向后兼容性并提供弃用警告。

```python
DEPRECATED_LOOKUP = {
    "ZapierToolkit": "langchain_community.agent_toolkits.zapier.toolkit",
}
```

## 注意事项

1. 建议开发者尽快迁移到 `langchain_community` 中的对应版本。
2. 使用此模块时会触发 `LangChainDeprecationWarning`。
3. 使用 Zapier NLA 需要有效的 Zapier API 密钥或 OAuth 令牌。

