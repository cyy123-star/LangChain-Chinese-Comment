# Runnable Schema：流式事件协议规范

`schema.py` 模块定义了 LangChain `astream_events` API 所使用的核心数据结构和类型声明。它是开发者理解和消费 LangChain 流式输出（Streaming Events）的蓝图。

## 文件概述

| 特性 | 描述 |
| :--- | :--- |
| **角色** | 类型定义模块、API 协议规范 |
| **主要职责** | 定义流式事件的标准格式，确保不同组件输出的事件结构统一 |
| **所属模块** | `langchain_core.runnables.schema` |

该模块不包含运行逻辑，仅包含基于 `TypedDict` 的类型定义，用于为 IDE 提供补全支持，并作为 `astream_events` 输出结果的正式文档。

## 核心数据结构详解

### 1. EventData (事件数据负载)

这是事件中 `data` 字段的具体内容，根据事件阶段（开始、流中、结束）包含不同的信息。

| 字段名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `input` | `Any` | 传递给 Runnable 的原始输入。 |
| `output` | `Any` | Runnable 完成后的最终输出结果（仅在 `end` 事件中可用）。 |
| `chunk` | `Any` | 增量输出块（仅在 `stream` 事件中可用）。多个 chunk 累加通常等于最终 output。 |
| `error` | `BaseException` | 执行过程中抛出的异常（仅在发生错误时存在）。 |
| `tool_call_id` | `str` | 与工具执行相关的唯一标识符（用于关联工具错误）。 |

### 2. BaseStreamEvent (流式事件基类)

定义了所有事件共有的基础元数据。

| 字段名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `event` | `str` | 事件名称，格式为 `on_[类型]_[阶段]`（详见下文）。 |
| `run_id` | `str` | 本次运行的唯一 UUID。 |
| `tags` | `list[str]` | 关联的标签，自动从父级继承。 |
| `metadata` | `dict` | 关联的元数据，用于存放业务相关的上下文。 |
| `parent_ids` | `list[str]` | 父级 Runnable 的 ID 列表，反映了调用栈深度。 |

### 3. 事件命名规范

`event` 字段遵循严格的命名约定：`on_<runnable_type>_<action>`

*   **Runnable 类型 (`runnable_type`)**:
    *   `llm`: 纯文本大模型。
    *   `chat_model`: 对话式大模型。
    *   `prompt`: 提示词模板。
    *   `tool`: 自定义工具。
    *   `chain`: 大多数 Runnable 组合（如 LCEL 链）。
*   **动作阶段 (`action`)**:
    *   `start`: 任务启动。
    *   `stream`: 产生增量数据。
    *   `end`: 任务结束。

## 使用示例

通过 `astream_events` 获取结构化事件流：

```python
from langchain_core.runnables import RunnableLambda

async def my_logic(input_str: str):
    # ... 业务逻辑 ...
    return f"Processed: {input_str}"

chain = RunnableLambda(my_logic).with_config(run_name="MyProcessor")

# 消费事件流
async for event in chain.astream_events("Hello", version="v2"):
    kind = event["event"]
    name = event["name"]
    
    if kind == "on_chain_start":
        print(f"开始执行 {name}, 输入: {event['data'].get('input')}")
    elif kind == "on_chain_stream":
        print(f"收到增量块: {event['data'].get('chunk')}")
    elif kind == "on_chain_end":
        print(f"执行结束 {name}, 输出: {event['data'].get('output')}")
```

## 注意事项

*   **API 版本**：建议始终使用 `astream_events(..., version="v2")`。v2 版本提供了更完整的 `parent_ids` 支持，方便构建复杂的追踪视图。
*   **数据可用性**：
    *   `input` 并非在所有事件中都可用。
    *   `output` 仅在 `end` 事件中可用。
    *   `chunk` 仅在 `stream` 事件中可用。
*   **自定义事件**：用户可以通过 `on_custom_event` 触发自定义事件，其 `data` 字段是完全自由格式的。

## 内部调用关系

*   **astream_events**: `Runnable` 基类中的此方法是该 schema 的主要生产者。
*   **Callback Handlers**: 事件系统在底层与 LangChain 的回调系统（Callbacks）紧密耦合，将回调信号转换为这些结构化的事件对象。

## 相关链接

*   [LangChain 官方文档 - astream_events 使用指南](https://python.langchain.com/docs/expression_language/how_to/streaming#using-stream-events)
*   [Runnable 核心类定义](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/core/langchain_core/runnables/base.md)

---
最后更新时间：2026-01-29
对应源码版本：LangChain Core v1.2.7
