# langchain_core.callbacks

## 模块概述
`langchain_core.callbacks` 模块是 LangChain 框架的事件监听和监控中心。它定义了一套完整的生命周期回调机制，允许开发者挂钩（Hook）到 LLM、Chain、Tool 和 Retriever 等组件的执行过程中。

通过该模块，可以实现诸如：
- **日志记录**: 实时打印执行进度（StdOut, File）。
- **流式显示**: 在终端实现打字机效果（StreamingStdOut）。
- **监控与追踪**: 将运行轨迹发送到外部平台（如 LangSmith）。
- **成本统计**: 自动计算 Token 消耗（UsageMetadata）。
- **自定义逻辑**: 在特定步骤执行自定义代码。

## 核心组件导出
该模块采用了动态导入（Dynamic Imports）机制，以提高启动速度并支持类型检查。

### 1. 基础接口 (from `base.py`)
- **`BaseCallbackHandler`**: 所有同步回调处理器的基类。
- **`AsyncCallbackHandler`**: 所有异步回调处理器的基类。
- **`Callbacks`**: 表示一组回调的类型定义（可以是列表或 Manager）。

### 2. 管理器 (from `manager.py`)
- **`CallbackManager`**: 核心管理器，负责分发同步事件。
- **`AsyncCallbackManager`**: 负责分发异步事件。
- **`RunManager`**: 针对单次运行的上下文管理器，用于在运行过程中上报事件。

### 3. 内置处理器
- **`StdOutCallbackHandler`**: 将日志打印到标准输出。
- **`StreamingStdOutCallbackHandler`**: 处理流式 Token 输出。
- **`FileCallbackHandler`**: 将日志写入文件。
- **`UsageMetadataCallbackHandler`**: 统计 Token 使用量。

### 4. 辅助函数
- **`dispatch_custom_event` / `adispatch_custom_event`**: 用于在执行过程中发送自定义事件。
- **`get_usage_metadata_callback`**: 便捷获取 Token 统计处理器的上下文管理器。

## 导入与使用建议
开发者通常不需要直接操作 `manager.py` 中的类，而是通过以下方式使用：

1. **配置回调**:
   ```python
   # 在调用 invoke 时传入
   chain.invoke(input, config={"callbacks": [handler1, handler2]})
   ```

2. **全局配置**:
   可以通过设置环境变量或全局配置来启用某些回调（如启用 LangSmith 追踪）。

## 相关链接
- [LangChain 官方文档 - Callbacks 概览](https://python.langchain.com/docs/modules/callbacks/)
- [源码目录](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/core/langchain_core/callbacks/)

---
最后更新时间: 2026-01-29
对应源码版本: LangChain Core v1.2.7
