# libs\core\langchain_core\outputs\generation.py

## 文件概述

`generation.py` 定义了 LangChain 中最基础的文本生成输出结构。它主要用于传统的 LLM（输入字符串，输出字符串）模型，代表单次生成的文本结果及其相关元数据。

## 导入依赖

- `langchain_core.load.Serializable`: 提供序列化能力。
- `langchain_core.utils._merge.merge_dicts`: 用于合并元数据字典，特别是在处理生成分片（Chunks）时。

## 类与函数详解

### 1. Generation
- **功能描述**: 表示单次文本生成的输出。它是传统 LLM 返回结果的基础单位。
- **参数说明**:
| 参数名 | 类型 | 默认值 | 是否必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `text` | `str` | - | 是 | 生成的文本内容。 |
| `generation_info` | `dict[str, Any] \| None` | `None` | 否 | 包含模型供应商提供的原始响应信息（如停止原因、Token 概率等）。 |
| `type` | `Literal["Generation"]` | `"Generation"` | 否 | 用于序列化的类型标识。 |

### 2. GenerationChunk
- **功能描述**: `Generation` 的子类，代表流式输出中的一个文本分片。支持通过 `+` 运算符与其他 `GenerationChunk` 进行拼接。
- **核心逻辑**:
  - `__add__` 方法：将两个分片的 `text` 字段进行字符串拼接，并使用 `merge_dicts` 合并两者的 `generation_info` 元数据。

## 使用示例

```python
from langchain_core.outputs import Generation, GenerationChunk

# 创建普通生成结果
gen = Generation(text="Hello world!", generation_info={"finish_reason": "stop"})

# 创建生成分片并拼接
chunk1 = GenerationChunk(text="Hello", generation_info={"index": 0})
chunk2 = GenerationChunk(text=" world", generation_info={"index": 1})
merged_chunk = chunk1 + chunk2

print(merged_chunk.text)  # 输出: "Hello world"
print(merged_chunk.generation_info)  # 输出: {'index': 1} (依赖合并策略)
```

## 注意事项

- `Generation` 主要用于非聊天模型（LLM）。对于聊天模型（Chat Model），应使用 `ChatGeneration`。
- 在流式输出场景中，建议始终使用 `GenerationChunk` 以支持自动拼接。

---
最后更新时间: 2026-01-29
对应源码版本: LangChain Core v1.2.7
