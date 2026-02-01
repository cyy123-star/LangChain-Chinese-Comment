# libs\langchain\langchain_classic\agents\agent_toolkits\azure_cognitive_services.py

此文档提供了 `libs\langchain\langchain_classic\agents\agent_toolkits\azure_cognitive_services.py` 文件的详细中文注释。该模块已被弃用，并重定向到 `langchain_community`。

## 功能描述

该模块定义了 `AzureCognitiveServicesToolkit`，它是一个用于与 Azure 认知服务（Azure Cognitive Services）交互的工具包。它允许代理使用 Azure 提供的各种 AI 能力，如计算机视觉、文本分析、语音识别等。通过动态导入机制，它现在指向 `langchain_community.agent_toolkits.azure_cognitive_services`。

## 弃用说明

该模块已被移动到 `langchain_community`。
- **原始导入路径**: `langchain_classic.agents.agent_toolkits.azure_cognitive_services.AzureCognitiveServicesToolkit`
- **建议导入路径**: `langchain_community.agent_toolkits.azure_cognitive_services.AzureCognitiveServicesToolkit`

## 主要类

### AzureCognitiveServicesToolkit

用于与 Azure 认知服务交互的工具包。它封装了一系列工具，允许 LLM 调用 Azure 的图像处理、翻译、表单识别等功能。

## 动态导入机制

模块使用 `create_importer` 实现动态加载，以确保向后兼容性并提供弃用警告。

```python
DEPRECATED_LOOKUP = {
    "AzureCognitiveServicesToolkit": "langchain_community.agent_toolkits.azure_cognitive_services",
}
```

## 注意事项

1. 建议开发者尽快迁移到 `langchain_community` 中的对应版本。
2. 使用此模块时会触发 `LangChainDeprecationWarning`。
3. 需要有效的 Azure 认知服务订阅密钥和终结点（Endpoint）才能使用。

