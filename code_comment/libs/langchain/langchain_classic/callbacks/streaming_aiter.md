# libs\langchain\langchain_classic\callbacks\streaming_aiter.py

`streaming_aiter.py` 提供了将 LLM 的流式输出转换为异步生成器（AsyncIterator）的实用工具。

## 核心类

### `AsyncIteratorCallbackHandler`
这是一个异步回调处理器，它内部维护一个 `asyncio.Queue`。每当 LLM 产生一个新 Token 时，该 Token 就会被放入队列中。

## 主要功能

- **异步迭代**: 允许开发者使用 `async for` 语法来遍历 LLM 生成的 Token。
- **解耦输出**: 它可以将回调驱动的流式输出（Push）转换为拉取式（Pull）的异步迭代，方便在异步 Web 框架（如 FastAPI, Sanic）中使用。

## 执行逻辑

1. **初始化**: 创建一个队列和完成事件（`done`）。
2. **入队**: 在 `on_llm_new_token` 中将 Token 存入队列。
3. **完成**: 在 `on_llm_end` 或 `on_llm_error` 中设置完成事件。
4. **迭代 (`aiter`)**: 
   - 循环等待队列中的新 Token 或完成事件。
   - 使用 `asyncio.wait` 同时监听队列获取和事件等待，响应最先发生的那个。
   - 产生（yield）获取到的 Token，直到完成事件被触发且队列为空。

## 使用示例

```python
from langchain_classic.callbacks import AsyncIteratorCallbackHandler

handler = AsyncIteratorCallbackHandler()

# 启动 LLM 调用（不要等待它结束）
task = asyncio.create_task(llm.agenerate(prompts=["..."], callbacks=[handler]))

# 异步迭代 Token
async for token in handler.aiter():
    print(token, end="", flush=True)

await task
```

## 注意事项

- **单任务限制**: 目前的实现不支持两个并发的 LLM 调用共享同一个处理器实例，因为 `done` 事件和 `queue` 会发生冲突。
- **错误处理**: 如果发生异常，`on_llm_error` 会设置完成事件，但 `aiter` 本身不会抛出原始异常，需要通过外层 `task` 来捕获。
