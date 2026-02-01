# libs\core\langchain_core\outputs\llm_result.py

## 文件概述

`llm_result.py` 定义了 LangChain 中 LLM 和聊天模型调用的统一结果容器 `LLMResult`。它是模型输出、元数据和运行信息的顶层封装，常用于回调系统和结果处理流水线。

## 导入依赖

- `pydantic.BaseModel`: 基础模型。
- `langchain_core.outputs.chat_generation`: 聊天生成相关类。
- `langchain_core.outputs.generation`: 文本生成相关类。
- `langchain_core.outputs.run_info.RunInfo`: 运行信息类。

## 类与函数详解

### 1. LLMResult
- **功能描述**: 封装 LLM 调用的完整结果，支持多 Prompt 和多候选生成。
- **参数说明**:
| 参数名 | 类型 | 默认值 | 是否必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `generations` | `list[list[Generation \| ChatGeneration]]` | - | 是 | 二维列表。第一维对应不同的输入 Prompt，第二维对应同一个 Prompt 的多个候选生成结果。 |
| `llm_output` | `dict \| None` | `None` | 否 | 供应商特定的原始输出（如 Token 统计）。 |
| `run` | `list[RunInfo] \| None` | `None` | 否 | 每个输入的运行元数据列表。 |
| `type` | `Literal["LLMResult"]` | `"LLMResult"` | 否 | 序列化类型标识。 |

- **核心逻辑**:
  - `flatten()`: 将嵌套的生成结果展开。将 `list[list[Generation]]` 转换为 `list[LLMResult]`，每个返回的 `LLMResult` 只包含一个生成结果。
  - **Token 计数防重**: 在 `flatten` 过程中，为了避免下游（如 OpenAICallback）重复计算 Token，只有第一个展开的 `LLMResult` 会保留 `token_usage` 信息，后续结果的 `token_usage` 会被清空。
  - `__eq__`: 比较两个 `LLMResult` 是否相等，比较时会忽略 `run` 字段。

## 使用示例

```python
from langchain_core.outputs import Generation, LLMResult

# 创建多 Prompt 结果
res = LLMResult(
    generations=[
        [Generation(text="Result 1")],
        [Generation(text="Result 2")]
    ],
    llm_output={"token_usage": {"total": 100}}
)

# 展开结果
flattened = res.flatten()
print(len(flattened))  # 输出: 2
print(flattened[0].llm_output)  # 输出: {'token_usage': {'total': 100}}
print(flattened[1].llm_output)  # 输出: {'token_usage': {}} (防止重复计数)
```

## 注意事项

- **多维列表**: 注意 `generations` 的结构。即使只有一个 Prompt 和一个生成结果，它也是 `[[Generation(...)]]`。
- **元数据依赖**: `llm_output` 包含非标准化信息。如果需要通用的 Token 统计，建议查看模型返回的消息对象中的标准化字段。

---
最后更新时间: 2026-01-29
对应源码版本: LangChain Core v1.2.7
