# libs\core\langchain_core\outputs\run_info.py

## 文件概述

`run_info.py` 定义了一个简单的元数据容器 `RunInfo`，用于存储链（Chain）或模型（Model）单次执行的运行时信息。

## 导入依赖

- `uuid.UUID`: 用于唯一标识运行。
- `pydantic.BaseModel`: 数据建模基础类。

## 类与函数详解

### 1. RunInfo
- **功能描述**: 包含单次运行的元数据，主要是一个唯一的 `run_id`。
- **参数说明**:
| 参数名 | 类型 | 默认值 | 是否必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `run_id` | `UUID` | - | 是 | 模型或链运行的唯一标识符。 |

## 注意事项

- **弃用警告**: 该模型在未来可能会被弃用。
- **推荐做法**: 用户现在应该优先通过回调系统（Callbacks）或 `astream_event` API 来获取 `run_id` 信息，而不是依赖 `RunInfo` 对象。
- **向后兼容性**: 目前保留该类主要是为了保持与旧版本 `langchain_core` 的兼容性。

---
最后更新时间: 2026-01-29
对应源码版本: LangChain Core v1.2.7
