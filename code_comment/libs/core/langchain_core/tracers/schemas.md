# schemas.py

- **最后更新时间**: 2026-01-29
- **对应源码版本**: LangChain Core v1.2.7

## 文件概述
`schemas.py` 模块定义了追踪器（Tracers）使用的数据结构模式。目前该模块主要作为 LangSmith `RunTree` 的兼容性层，将 `RunTree` 重新导出为 `Run`。

## 导入依赖
| 模块 | 作用 |
| :--- | :--- |
| `langsmith.RunTree` | 来自 LangSmith 的核心数据结构，用于表示一个追踪运行（Run）。 |

## 类与函数详解
### 1. Run (别名)
- **功能描述**: `Run` 是 `langsmith.RunTree` 的别名。它代表了 LangChain 中的一个执行单元（如 LLM 调用、Chain 执行、Tool 运行等）。
- **核心字段**:
  - `id`: 运行的唯一标识符（UUID）。
  - `name`: 运行的名称。
  - `run_type`: 运行类型（如 `llm`, `chain`, `tool`, `retriever`）。
  - `start_time`: 开始时间。
  - `end_time`: 结束时间。
  - `inputs`: 输入字典。
  - `outputs`: 输出字典。
  - `parent_run_id`: 父运行的 ID。
  - `child_runs`: 子运行列表。
  - `tags`: 标签列表。
  - `metadata`: 元数据字典。

## 内部调用关系
- 该模块定义的 `Run` 别名被 `BaseTracer`、`_TracerCore` 以及其他具体的追踪器广泛使用，作为数据传递的基础模型。

## 相关链接
- [LangSmith Documentation](https://docs.smith.langchain.com/)
- [langchain_core.tracers.base](base.md)
