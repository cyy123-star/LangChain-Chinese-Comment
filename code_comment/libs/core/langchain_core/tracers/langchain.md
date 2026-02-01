# langchain.py

- **最后更新时间**: 2026-01-29
- **对应源码版本**: LangChain Core v1.2.7

## 文件概述
`langchain.py` 实现了 `LangChainTracer`，这是 LangChain 与 LangSmith 平台连接的关键组件。它负责将追踪数据（Runs）通过 LangSmith 客户端异步发送到指定的项目端点，从而实现对链、代理和模型的监控、调试和评估。

## 导入依赖
| 模块 | 作用 |
| :--- | :--- |
| `langsmith.Client` | 用于与 LangSmith API 交互的客户端。 |
| `concurrent.futures.ThreadPoolExecutor` | 用于异步发送运行数据，避免阻塞主线程。 |
| `tenacity` | 提供重试机制，确保在网络波动时数据能可靠发送。 |
| `langchain_core.tracers.base.BaseTracer` | 继承追踪器基础接口。 |

## 类与函数详解
### 1. LangChainTracer
- **功能描述**: 将 LangChain 的执行记录持久化到 LangSmith。它是生产环境下最常用的追踪器。
- **参数说明**:
  | 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
  | :--- | :--- | :--- | :--- | :--- |
  | `example_id` | `UUID | str` | `None` | 否 | 关联的数据集示例 ID，用于评估。 |
  | `project_name` | `str` | `None` | 否 | LangSmith 中的项目名称。 |
  | `client` | `Client` | `None` | 否 | LangSmith 客户端实例。 |
  | `tags` | `list[str]` | `None` | 否 | 附加到所有运行的全局标签。 |

#### 核心方法:
- **_persist_run(run: Run)**: 内部维护一个 `latest_run` 引用，但不包含子运行以节省内存。
- **_persist_run_single(run: Run)**: 调用 `run.post()` 将新创建的运行发送到 LangSmith。
- **_update_run_single(run: Run)**: 调用 `run.patch()` 在运行结束时更新输出和元数据。
- **get_run_url()**: 获取当前根运行在 LangSmith 网页端的访问 URL，便于快速调试。

## 核心逻辑解读
1. **异步发送**: 追踪器利用线程池（`ThreadPoolExecutor`）进行网络请求，确保追踪过程对原始业务逻辑的延迟影响降到最低。
2. **环境变量集成**: 自动从环境变量（如 `LANGCHAIN_PROJECT`）中读取配置信息。
3. **元数据自动补充**: 在发送前会自动收集运行时环境信息（如 Python 版本、系统平台等）作为元数据。

## 注意事项
- 必须正确配置 `LANGCHAIN_API_KEY` 才能成功发送数据。
- 追踪器支持 `run_inline=True`，这意味着某些核心逻辑会在主线程中执行，但网络请求始终是异步的。
- 所有的异常都会被内部捕获并记录到日志中，不会中断正常的链执行。

## 相关链接
- [LangSmith Documentation](https://docs.smith.langchain.com/)
- [langchain_core.tracers.base](base.md)
