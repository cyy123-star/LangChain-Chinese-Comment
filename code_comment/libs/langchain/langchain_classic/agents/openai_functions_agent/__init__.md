# libs\langchain\langchain_classic\agents\openai_functions_agent\__init__.py

此文档提供了 `libs\langchain\langchain_classic\agents\openai_functions_agent\__init__.py` 文件的详细中文注释。

## 功能描述

该模块实现了利用 OpenAI 早期的“函数调用”（Function Calling）能力的代理。虽然现在 OpenAI 推荐使用“工具调用”（Tools），但“函数调用”仍然被广泛使用，尤其是在一些旧的代码库中。

## 主要组件

- `OpenAIFunctionsAgent`: 基于 OpenAI 函数调用逻辑的代理类。
- `create_openai_functions_agent`: 用于创建该类型代理的工厂函数（推荐使用）。

## 核心逻辑

该代理将工具描述转换为 OpenAI 的 `functions` 参数格式。模型会决定是否调用某个函数，并返回函数名称和参数。代理执行工具后，将结果作为 `FunctionMessage` 传回给模型。

## 注意事项

- **已弃用**: `OpenAIFunctionsAgent` 类已在 0.1.0 版本标记为弃用，建议迁移到 `create_openai_functions_agent` 函数。
- **现代替代方案**: 对于支持最新 API 的模型，建议优先使用 `create_openai_tools_agent`。

