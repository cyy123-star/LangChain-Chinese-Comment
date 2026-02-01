# libs\langchain\langchain_classic\callbacks\file.py

`file.py` 提供了一个将回调日志写入文件的处理器。

## 核心类

### `FileCallbackHandler`
该处理器会将 Chain、LLM 和 Tool 的运行日志格式化后写入指定的本地文件。

## 主要功能

- **日志持久化**: 允许开发者将复杂的 Chain 运行轨迹保存到磁盘，以便后续离线分析或审计。
- **自定义格式**: 支持通过 `color` 参数控制输出的颜色标记（在支持 ANSI 的查看器中有效）。

## 使用示例

```python
from langchain_classic.callbacks import FileCallbackHandler

# 指定输出文件路径
handler = FileCallbackHandler(filename="run_log.txt")

# 在运行链时传入
chain.invoke({"input": "test"}, callbacks=[handler])
```

## 注意事项

- **并发写入**: 当多个 Chain 实例同时使用同一个 `FileCallbackHandler` 且指向同一个文件时，可能会出现竞态条件或日志交织。建议为不同的运行实例创建不同的处理器。
- **文件管理**: 它不会自动滚动或清理日志文件，需要外部机制（如 `logrotate`）进行管理。
