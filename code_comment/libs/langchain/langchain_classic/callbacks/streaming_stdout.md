# libs\langchain\langchain_classic\callbacks\streaming_stdout.py

`streaming_stdout.py` 提供了一个专门用于**流式输出**的回调处理器。

## 核心类

### `StreamingStdOutCallbackHandler`
该处理器通过实现 `on_llm_new_token` 方法，在 LLM 生成每一个新 Token 时立即将其打印到控制台，而不是等待整个响应生成完毕。

## 主要功能

- **实时交互**: 为用户提供类似 ChatGPT 的打字机效果，极大地提升了用户体验。
- **无缓冲打印**: 默认情况下，它会立即刷新输出流，确保 Token 能够实时显示。

## 使用示例

```python
from langchain_openai import ChatOpenAI
from langchain_classic.callbacks import StreamingStdOutCallbackHandler

# 必须在模型中开启 streaming=True
llm = ChatOpenAI(streaming=True, callbacks=[StreamingStdOutCallbackHandler()])

llm.invoke("写一篇关于人工智能的长文")
```

## 注意事项

- **流式支持**: 只有当底层的语言模型（LLM/ChatModel）支持流式输出并显式开启了 `streaming=True` 时，该处理器才会生效。
- **单路输出**: 如果在一个 Chain 中同时运行多个 LLM，它们的流式 Token 可能会交织在一起打印。
