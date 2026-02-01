# libs\langchain\langchain_classic\agents\agent_iterator.py

此文档提供了 `libs\langchain\langchain_classic\agents\agent_iterator.py` 文件的详细中文注释。该模块提供了 `AgentExecutorIterator` 类，允许以迭代器的方式运行代理执行器。

## 功能描述

`AgentExecutorIterator` 是对 `AgentExecutor` 运行逻辑的包装，它将原本黑盒式的 `run` 或 `invoke` 过程转变为可观察、可干预的迭代过程。

这对于需要实时展示代理思考过程（思考 -> 行动 -> 观察）或在步骤间插入自定义逻辑的场景非常有用。

## 核心类：`AgentExecutorIterator`

代理执行器的迭代器实现，支持同步和异步迭代。

### 1. 初始化参数表

| 参数 | 类型 | 描述 |
| :--- | :--- | :--- |
| `agent_executor` | `AgentExecutor` | 要迭代运行的代理执行器实例。 |
| `inputs` | `Any` | 传递给代理的原始输入。 |
| `callbacks` | `Callbacks` | 用于监控迭代过程的回调管理器。 |
| `include_run_info` | `bool` | 是否在产出结果中包含运行元数据。 |
| `yield_actions` | `bool` | 是否在生成动作（Action）时立即产出，而不等待工具执行结果。 |

### 2. 核心状态管理

- `intermediate_steps`: 记录当前的动作-观察链条。
- `iterations`: 累计迭代步数。
- `time_elapsed`: 累计执行时长。

### 3. 主要方法

- `__next__()` / `__anext__()`: 执行代理的下一个逻辑步。如果代理结束，则抛出 `StopIteration` 或返回最终结果。
- `reset()`: 重置迭代器状态，准备开始新的任务运行。

## 内部工作流程

1. **初始化**: 预处理输入，初始化回调环境和计时器。
2. **步进逻辑 (`_iter_next_step`)**:
   - 验证停止条件（最大次数/超时）。
   - 调用代理的 `plan` 方法。
   - 处理 `AgentAction`: 如果 `yield_actions` 为真，则直接返回动作；否则执行工具并记录观察结果。
   - 处理 `AgentFinish`: 触发结束回调并返回最终输出。
3. **清理**: 迭代结束后，触发 `on_chain_end`。

## 应用场景

- **实时日志展示**: 在终端或 Web 端逐条流式输出代理的思考轨迹。
- **断点调试**: 允许开发者在代理执行特定工具前进行人工干预。
- **自定义限制**: 在迭代过程中根据动态条件（如预算、资源消耗）随时中断代理运行。


