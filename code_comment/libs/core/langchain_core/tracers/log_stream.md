# log_stream.py - 日志流 Tracer

`log_stream.py` 模块实现了 LangChain 的 `astream_log` API，通过 JSONPatch 增量更新的方式提供运行状态的实时视图。

## 文件概述

该模块定义了 `LogStreamCallbackHandler`，它能够将一个复杂的链式运行过程（包括所有子运行、Token 输出等）转换为一系列的 `JSONPatch` 操作。这种方式允许客户端高效地重建并维护一个代表当前运行状态的完整字典。

## 导入依赖

| 依赖模块 | 作用 |
| :--- | :--- |
| `jsonpatch` | 用于生成和应用 JSON Patch 操作。 |
| `asyncio` | 提供异步流支持。 |
| `langchain_core.tracers.memory_stream` | 内部跨线程/协程通信通道。 |
| `langchain_core.load` | 序列化和反序列化运行数据。 |

## 类详解

### `LogStreamCallbackHandler`

#### 功能描述
该 Tracer 维护了一个 `RunState` 对象，记录了根运行及其所有子运行的详细信息（输入、输出、耗时、流式 Token 等）。每当状态发生变化时，它会发送一个 `RunLogPatch`。

#### 核心数据结构

1.  **`LogEntry` (TypedDict)**: 代表子运行的条目。
    - `streamed_output`: 流式输出块列表。
    - `final_output`: 最终输出。
    - `start_time` / `end_time`: ISO 格式的时间戳。

2.  **`RunState` (TypedDict)**: 代表整个运行树的完整状态。
    - `logs`: 键为子运行名称，值为 `LogEntry` 的映射。

3.  **`RunLogPatch`**: 包含一个 `ops` 列表（JSONPatch 操作，如 `add`, `replace`）。

#### 关键方法

- **`send(*ops)`**: 向输出流推送新的 Patch 操作。
- **`include_run(run)`**: 根据用户提供的 `include_names`, `include_types` 等过滤器决定是否记录该子运行。
- **`_on_run_create(run)`**: 
    - 如果是根运行，初始化整个 `RunState`。
    - 如果是子运行且满足过滤条件，在 `/logs/` 路径下创建一个新的 `LogEntry`。
- **`_on_run_update(run)`**: 更新运行的 `final_output` 和 `end_time`。
- **`_on_llm_new_token(run, token, chunk)`**: 向对应运行的 `streamed_output` 列表追加新 Token。

---

## 内部逻辑：JSONPatch 路径规范

该模块使用标准的 JSON 指针路径来定位状态中的数据：
- `/logs/MyChainName`: 指向名为 "MyChainName" 的子运行。
- `/logs/MyChainName/streamed_output/-`: 向流式输出列表末尾追加。
- `/final_output`: 指向根运行的最终结果。

---

## 使用示例

```python
from langchain_core.tracers.log_stream import LogStreamCallbackHandler

handler = LogStreamCallbackHandler()

# 模拟异步迭代获取 Patch
async def consume_logs():
    async for patch in handler:
        print(f"收到 Patch: {patch.ops}")
        # 可以使用 jsonpatch.apply_patch(current_state, patch.ops) 更新本地状态
```

## 注意事项
- **名称冲突**：如果多个子运行具有相同的名称，模块会自动添加后缀（如 `MyChain:2`）。
- **性能开销**：由于需要维护完整的运行状态并计算 Patch，对于极其庞大的运行树，内存和 CPU 占用会高于普通 Tracer。
- **自动关闭**：默认情况下，当根运行结束时，输出流会自动关闭。

## 相关链接
- [astream_log 官方文档](https://python.langchain.com/docs/expression_language/streaming#astream_log)
- [JSONPatch 规范 (RFC 6902)](https://jsonpatch.com/)

---
**最后更新时间**: 2026-01-29
**对应源码版本**: LangChain Core v1.2.7
