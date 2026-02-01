# evaluation.py - 评估回调处理工具

`evaluation.py` 模块提供了一个专门用于在运行完成后执行评估逻辑的 Tracer。

## 文件概述

该文件定义了 `EvaluatorCallbackHandler`，它可以在 LangChain 的运行（Run）持久化时，自动触发预定义的评估器（Evaluator）。这对于集成 LangSmith 评估流程或自定义自动化评估任务非常有用。

## 导入依赖

| 依赖模块 | 作用 |
| :--- | :--- |
| `langsmith` | 提供 LangSmith 客户端和评估接口。 |
| `concurrent.futures` | 使用线程池并发执行评估任务。 |
| `weakref` | 使用弱引用管理 Future 对象和 Tracer 实例，防止内存泄漏。 |
| `langchain_core.tracers.base` | 继承 `BaseTracer` 基础类。 |

## 类详解

### `EvaluatorCallbackHandler`

#### 功能描述
该 Tracer 在每次运行结束并持久化时，将运行数据提交给一组评估器进行分析。支持并发执行，并能将结果记录回 LangSmith 或本地字典。

#### 构造参数
| 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `evaluators` | `Sequence[RunEvaluator]` | - | 是 | 要执行的评估器列表。 |
| `client` | `langsmith.Client` | `None` | 否 | LangSmith 客户端实例。 |
| `example_id` | `UUID \| str` | `None` | 否 | 与运行关联的数据集示例 ID。 |
| `skip_unfinished` | `bool` | `True` | 否 | 是否跳过未完成或出错的运行。 |
| `project_name` | `str` | `"evaluators"` | 否 | 评估运行所属的 LangSmith 项目名。 |
| `max_concurrency` | `int` | `None` | 否 | 最大并发评估任务数。 |

#### 核心方法

1.  **`_persist_run(run)`**:
    - 核心入口。当一个运行树完成时被调用。
    - 复制运行数据并关联 `example_id`。
    - 将评估任务提交至线程池执行。

2.  **`_evaluate_in_project(run, evaluator)`**:
    - 在特定的 LangSmith 项目上下文中执行单个评估器。
    - 处理评估结果并将其记录到反馈系统中。

3.  **`wait_for_futures()`**:
    - 等待所有正在进行的异步评估任务完成。

---

## 全局函数

### `wait_for_all_evaluators()`

#### 功能描述
静态函数，用于等待所有活跃的 `EvaluatorCallbackHandler` 实例完成其后台评估任务。在程序退出前调用此函数可确保评估数据不丢失。

---

## 使用示例

```python
from langsmith import Client
from langchain_core.tracers.evaluation import EvaluatorCallbackHandler

# 假设已定义一些评估器
evaluators = [my_evaluator1, my_evaluator2]

# 创建处理程序
handler = EvaluatorCallbackHandler(
    evaluators=evaluators,
    project_name="my_eval_project"
)

# 在 Chain 运行中使用
# chain.invoke({"input": "test"}, config={"callbacks": [handler]})

# 等待评估结束
handler.wait_for_futures()
```

## 注意事项
- **后台执行**：评估任务默认在后台线程池执行，不会阻塞主流程的响应时间。
- **内存管理**：内部使用 `weakref.WeakSet` 跟踪任务，确保不会因为未完成的任务阻塞垃圾回收。
- **环境依赖**：通常需要配置 `LANGSMITH_API_KEY` 以便将反馈记录到云端。

## 相关链接
- [LangSmith 评估文档](https://docs.smith.langchain.com/evaluation)
- [BaseTracer 源码](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/core/langchain_core/tracers/base.md)

---
**最后更新时间**: 2026-01-29
**对应源码版本**: LangChain Core v1.2.7
