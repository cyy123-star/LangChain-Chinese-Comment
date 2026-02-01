# __init__.py

- **最后更新时间**: 2026-01-29
- **对应源码版本**: LangChain Core v1.2.7

## 文件概述
`langchain_core.tracers` 模块的初始化文件。它通过动态导入（Lazy Import）机制暴露了模块内最常用的追踪器类和数据结构。

## 核心接口说明
通过此模块，用户可以方便地导入以下核心组件：

### 1. 追踪器 (Tracers)
- **BaseTracer**: 所有追踪器的抽象基类。
- **LangChainTracer**: 用于将数据发送到 LangSmith 的官方追踪器。
- **ConsoleCallbackHandler**: 用于在控制台打印执行流程的追踪器。
- **LogStreamCallbackHandler**: 用于流式输出运行日志的追踪器（常用于 `astream_log`）。
- **EvaluatorCallbackHandler**: 用于在追踪过程中进行自动化评估的处理器。

### 2. 数据模型 (Data Models)
- **Run**: 代表一个执行单元的完整信息模型。
- **RunLog**: 包含运行状态和操作历史的日志对象。
- **RunLogPatch**: 代表运行日志的增量更新补丁。

## 动态导入机制
该模块采用了 `__getattr__` 钩子实现的动态导入：
1. **优势**: 减少初始加载时间，只有在实际用到某个追踪器时才会加载其对应的子模块。
2. **实现**: `_dynamic_imports` 字典维护了类名到子模块名的映射关系。

## 使用建议
推荐通过此入口统一导入追踪器相关组件：
```python
from langchain_core.tracers import LangChainTracer, ConsoleCallbackHandler
```

## 相关链接
- [base.md](base.md)
- [langchain.md](langchain.md)
- [stdout.md](stdout.md)
- [log_stream.md](log_stream.md)
- [schemas.md](schemas.md)
