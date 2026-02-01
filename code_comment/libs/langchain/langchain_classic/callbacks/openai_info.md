# libs\langchain\langchain_classic\callbacks\openai_info.py

`openai_info.py` 提供了专门用于跟踪 OpenAI API 调用信息（如 Token 使用量和成本）的回调处理器。

## 核心类

### `OpenAICallbackHandler`
一个继承自 `BaseCallbackHandler` 的处理器，专门设计用来监听 OpenAI 模型的输出并提取其 `usage` 字段。

## 主要功能

- **Token 计数**: 自动累计 `prompt_tokens`、`completion_tokens` 和 `total_tokens`。
- **成本估算**: 根据内置的模型价格表，自动计算本次调用的预估成本（USD）。
- **请求跟踪**: 记录成功的请求次数。

## 使用说明

该处理器通常通过 `get_openai_callback` 上下文管理器来便捷使用，而不是手动实例化。

```python
from langchain_classic.callbacks import get_openai_callback

with get_openai_callback() as cb:
    # 执行 OpenAI 相关操作
    ...
    print(cb) # 打印详细的使用情况汇总
```

## 注意事项

- **模型支持**: 主要支持 OpenAI 官方模型。对于通过 Azure OpenAI 或其他代理调用的模型，可能需要确保返回的响应格式符合 OpenAI 标准。
- **实时性**: 只有在 LLM 调用完成后，相关的计数信息才会更新。
