# core.py

- **最后更新时间**: 2026-01-29
- **对应源码版本**: LangChain Core v1.2.7

## 文件概述
`core.py` 提供了追踪器（Tracers）的核心逻辑实现。它定义了抽象基类 `_TracerCore`，负责管理运行（Run）的生命周期、维护父子调用关系、处理堆栈追踪以及创建不同类型的运行对象。

## 导入依赖
| 模块 | 作用 |
| :--- | :--- |
| `datetime` | 处理运行的开始和结束时间。 |
| `traceback` | 获取异常的堆栈追踪信息。 |
| `langchain_core.load.dumpd` | 将对象序列化为字典。 |
| `langchain_core.tracers.schemas.Run` | 运行数据的核心模式。 |

## 类与函数详解
### 1. _TracerCore (抽象基类)
- **功能描述**: 追踪器的核心逻辑基类，不直接参与回调处理，而是专注于运行对象的创建、维护和持久化逻辑。
- **核心属性**:
  - `run_map`: `dict[str, Run]` - 存储当前正在进行的运行，键为运行 ID 的字符串形式。
  - `order_map`: `dict[UUID, tuple[UUID, str]]` - 存储运行 ID 到其对应的追踪 ID 和点状顺序（dotted order）的映射。

#### 核心方法:
- **_start_trace(run: Run)**: 
  - **功能**: 初始化追踪。计算运行的 `trace_id` 和 `dotted_order`。
  - **逻辑**: 如果存在父运行，则将当前运行作为子项添加到父运行中，并继承父运行的 `trace_id`。
- **_create_llm_run(...)**:
  - **功能**: 创建一个 LLM 类型的运行对象。
- **_create_chat_model_run(...)**:
  - **功能**: 创建一个聊天模型类型的运行对象（仅支持特定架构格式）。
- **_complete_llm_run(response, run_id)**:
  - **功能**: 标记 LLM 运行完成，记录输出结果和结束时间。
- **_persist_run(run: Run)**:
  - **功能**: 抽象方法，由子类实现，用于将运行数据持久化（如保存到数据库或发送到 API）。

## 核心逻辑解读
1. **点状顺序 (Dotted Order)**:
   - LangChain 使用一种基于时间戳和 UUID 的点状字符串来表示运行的层级关系。例如 `20230101T000000Z<uuid1>.<timestamp><uuid2>`。这种设计允许在分布式系统中快速重建调用树。
2. **生命周期管理**:
   - 追踪器通过 `run_map` 维护活跃运行。当一个运行结束时，它会从 `run_map` 中移除，并触发持久化逻辑。

## 注意事项
- `_schema_format` 参数目前主要用于内部实验性功能（如 `streaming_events`），普通用户通常不需要修改。
- `run_map` 在运行结束时会被清理，但 `order_map` 会在追踪器对象的生命周期内一直存在，以支持深层嵌套的调用关系。

## 相关链接
- [langchain_core.tracers.base](base.md)
- [langchain_core.tracers.schemas](schemas.md)
