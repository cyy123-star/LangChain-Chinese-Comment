# libs\core\langchain_core\outputs\chat_result.py

## 文件概述

`chat_result.py` 定义了聊天模型单次调用（对应一个 Prompt）的结果容器。它包含模型生成的多个候选结果（`ChatGeneration`）以及模型供应商返回的原始元数据。

## 导入依赖

- `pydantic.BaseModel`: 提供基础的数据建模和验证功能。
- `langchain_core.outputs.chat_generation.ChatGeneration`: 聊天生成结果类。

## 类与函数详解

### 1. ChatResult
- **功能描述**: 表示聊天模型单次 Prompt 调用的完整结果。
- **参数说明**:
| 参数名 | 类型 | 默认值 | 是否必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `generations` | `list[ChatGeneration]` | - | 是 | 生成结果列表。支持返回多个候选生成（n > 1 的场景）。 |
| `llm_output` | `dict \| None` | `None` | 否 | 供应商特定的原始输出字典。通常包含 Token 使用情况、模型名称等非标准化信息。 |

## 使用示例

```python
from langchain_core.messages import AIMessage
from langchain_core.outputs import ChatGeneration, ChatResult

# 创建聊天结果容器
generation = ChatGeneration(message=AIMessage(content="Hello!"))
result = ChatResult(
    generations=[generation],
    llm_output={"model_name": "gpt-3.5-turbo", "usage": {"total_tokens": 10}}
)

print(result.generations[0].text)  # 输出: "Hello!"
```

## 注意事项

- **内部使用**: `ChatResult` 主要在聊天模型实现内部使用。
- **最终转换**: 它最终会被映射为更通用的 `LLMResult` 对象，或者在 Runnable 接口中直接被投影为 `AIMessage` 对象。
- **不稳定性**: `llm_output` 字段是自由格式且非标准化的，用户应尽量依赖 `AIMessage` 中的标准字段，而非直接读取此字典，以保证代码的跨供应商兼容性。

---
最后更新时间: 2026-01-29
对应源码版本: LangChain Core v1.2.7
