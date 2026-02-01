# OpenAICallbackHandler

`OpenAICallbackHandler` 是一个专门用于监控 OpenAI 模型调用成本的工具。它能够自动捕获并汇总单次运行（或上下文管理器内的多次运行）中消耗的 Token 数量以及预估的费用。

## 核心功能

- **Token 追踪**: 分别统计 `prompt_tokens`, `completion_tokens` 和 `total_tokens`。
- **成本计算**: 根据模型类型自动计算预估费用（基于官方定价）。
- **聚合统计**: 可以在一个 `with` 块中追踪多个并发或顺序的调用。

## 使用方法

通常通过 `get_openai_callback` 上下文管理器来使用：

```python
from langchain_community.callbacks.manager import get_openai_callback
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o")

with get_openai_callback() as cb:
    response1 = llm.invoke("What is the capital of France?")
    response2 = llm.invoke("What is the capital of Germany?")
    
    print(f"Total Tokens: {cb.total_tokens}")
    print(f"Prompt Tokens: {cb.prompt_tokens}")
    print(f"Completion Tokens: {cb.completion_tokens}")
    print(f"Total Cost (USD): ${cb.total_cost}")
```

## 注意事项

1. **兼容性**: 该处理器仅支持 OpenAI 系列模型（包括通过 Azure 部署的模型）。
2. **流式传输**: 在流式输出（Streaming）模式下，早期的 OpenAI API 不返回 Token 统计信息，但现代 API (如 `gpt-4o`) 已经支持在最后一个数据块中返回统计数据。
3. **数据来源**: 所有的属性（如 `total_tokens`）都是从模型返回的 `usage` 字段中提取的。
