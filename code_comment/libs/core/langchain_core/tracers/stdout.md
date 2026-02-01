# stdout.py

- **最后更新时间**: 2026-01-29
- **对应源码版本**: LangChain Core v1.2.7

## 文件概述
`stdout.py` 提供了将追踪信息输出到控制台（标准输出）的追踪器实现。主要包括 `ConsoleCallbackHandler`，它通过彩色文本和缩进结构化地展示链、模型和工具的调用过程，是本地调试 LangChain 应用的最直接工具。

## 导入依赖
| 模块 | 作用 |
| :--- | :--- |
| `json` | 用于格式化输入输出数据。 |
| `langchain_core.utils.input` | 获取加粗和彩色文本的工具函数。 |
| `langchain_core.tracers.base.BaseTracer` | 继承追踪器基础接口。 |

## 类与函数详解
### 1. FunctionCallbackHandler
- **功能描述**: 一个通用的追踪器，它接收一个自定义函数，并将格式化后的追踪字符串传递给该函数。
- **参数说明**:
  | 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
  | :--- | :--- | :--- | :--- | :--- |
  | `function` | `Callable[[str], None]` | - | 是 | 处理格式化字符串的回调函数（如 `print` 或日志记录函数）。 |

### 2. ConsoleCallbackHandler (继承自 FunctionCallbackHandler)
- **功能描述**: 专门用于向控制台打印追踪信息的处理器。它是 `FunctionCallbackHandler` 使用 `print` 函数的特化版本。
- **使用场景**: 在代码中通过 `callbacks=[ConsoleCallbackHandler()]` 启用，即可在控制台看到详细的执行流程。

### 3. 辅助函数
- **elapsed(run)**: 计算并格式化运行的持续时间（秒或毫秒）。
- **try_json_stringify(obj, fallback)**: 尝试将对象转换为 JSON 字符串，失败则返回备选方案，确保输出不因序列化错误中断。

## 核心逻辑解读
1. **面包屑导航 (Breadcrumbs)**:
   - 通过 `get_breadcrumbs` 方法，追踪器会生成类似于 `Chain:MyChain > LLM:ChatOpenAI` 的路径，清晰地展示当前的调用深度和上下文。
2. **可视化标记**:
   - 使用不同的颜色标记不同的阶段：
     - `[chain/start]`, `[llm/start]`, `[tool/start]`: **绿色**
     - `[chain/end]`, `[llm/end]`, `[tool/end]`: **蓝色**
     - `[chain/error]`, `[llm/error]`, `[tool/error]`: **红色**

## 使用示例
```python
from langchain_core.tracers.stdout import ConsoleCallbackHandler
from langchain_core.runnables import RunnableLambda

chain = RunnableLambda(lambda x: x + 1)
# 启用控制台追踪
chain.invoke(1, config={"callbacks": [ConsoleCallbackHandler()]})
```

## 注意事项
- 由于向控制台打印大量数据会产生 I/O 开销，不建议在高性能生产环境的并发请求中大规模开启。
- 输出内容包含敏感数据（如 Prompt 内容和模型响应），请注意保护隐私。

## 相关链接
- [langchain_core.tracers.base](base.md)
- [langchain_core.utils.input](../utils/input.md)
