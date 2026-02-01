# run_collector.py - 运行数据收集器

`run_collector.py` 模块提供了一个简单的 Tracer，用于将所有的运行（Run）数据收集到一个本地列表中。

## 文件概述

该文件定义了 `RunCollectorCallbackHandler`。它主要用于调试、测试或交互式环境（如 Jupyter Notebook），让开发者能够方便地在代码执行后检查整个调用链条中产生的详细运行轨迹。

## 导入依赖

| 依赖模块 | 作用 |
| :--- | :--- |
| `langchain_core.tracers.base` | 继承 `BaseTracer` 基础类。 |
| `langchain_core.tracers._compat` | 使用 `run_copy` 安全地复制运行对象。 |

## 类详解

### `RunCollectorCallbackHandler`

#### 功能描述
该处理器会在每个运行完成并持久化时，将其深拷贝并存储到内部的 `traced_runs` 列表中。

#### 构造参数
| 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `example_id` | `UUID \| str` | `None` | 否 | 关联的数据集示例 ID。 |
| `**kwargs` | `Any` | - | 否 | 传递给 `BaseTracer` 的其他参数。 |

#### 核心属性
- `traced_runs`: 存储 `Run` 对象的列表。

#### 关键方法
- **`_persist_run(run)`**: 
    - 当一个运行树（或子运行）完成时调用。
    - 使用 `run_copy` 复制当前运行，避免后续修改影响已记录的数据。
    - 设置 `reference_example_id`。
    - 将复制后的对象添加到 `traced_runs`。

---

## 使用示例

```python
from langchain_core.tracers.run_collector import RunCollectorCallbackHandler

# 创建收集器
collector = RunCollectorCallbackHandler()

# 在运行中使用
# chain.invoke({"input": "test"}, config={"callbacks": [collector]})

# 检查收集到的运行数据
for run in collector.traced_runs:
    print(f"Run Name: {run.name}, Type: {run.run_type}")
    print(f"Inputs: {run.inputs}")
    print(f"Outputs: {run.outputs}")
```

## 注意事项
- **内存占用**：由于它会在内存中保存所有运行的深拷贝，如果运行非常频繁或运行数据（如输入输出）极大，可能会导致内存快速增长。
- **线程安全**：继承自 `BaseTracer`，在处理并发运行方面遵循基类的锁定机制。

## 相关链接
- [Run 结构定义](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/core/langchain_core/tracers/schemas.md)
- [BaseTracer 源码](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/core/langchain_core/tracers/base.md)

---
**最后更新时间**: 2026-01-29
**对应源码版本**: LangChain Core v1.2.7
