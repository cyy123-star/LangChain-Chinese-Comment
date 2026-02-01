# usage.py - Token 使用量与统计工具

`usage.py` 模块提供了一系列用于处理 LLM 资源消耗（如 Token 计数）的实用工具。

## 文件概述

在处理 LLM 输出时，通常需要对多个步骤的 Token 使用量进行累加。该模块提供了能够递归处理嵌套字典并执行加法运算的函数，非常适合合并多个 `usage_metadata`。

## 导入依赖

| 依赖模块 | 作用 |
| :--- | :--- |
| `typing` | 提供类型注解支持（`Callable`, `Any` 等）。 |

## 函数详解

### `_dict_int_op`

#### 功能描述
对两个嵌套字典中对应位置的整数值执行指定的二元运算（默认为加法）。

#### 参数说明
| 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `left` | `dict` | - | 是 | 左操作数（字典）。 |
| `right` | `dict` | - | 是 | 右操作数（字典）。 |
| `op` | `Callable[[int, int], int]` | - | 是 | 要执行的操作函数（如 `operator.add`）。 |
| `default` | `int` | `0` | 否 | 当某个键在其中一个字典中不存在时的默认值。 |

#### 返回值解释
`dict`: 返回合并后的新字典。

#### 核心逻辑
1. 遍历两个字典的所有唯一键。
2. 如果值仍是字典，则递归调用自身。
3. 如果值是整数，则应用 `op`（如 `left_val + right_val`）。
4. 包含深度限制防止无限递归（默认最大深度 100）。

---

## 使用示例

```python
import operator
from langchain_core.utils.usage import _dict_int_op

usage1 = {"prompt_tokens": 10, "completion_tokens": 5}
usage2 = {"prompt_tokens": 20, "total_tokens": 25}

# 累加使用量
total_usage = _dict_int_op(usage1, usage2, operator.add)
print(total_usage)
# 输出: {'prompt_tokens': 30, 'completion_tokens': 5, 'total_tokens': 25}
```

## 注意事项
- 该函数主要针对数值统计设计，如果字典中包含非整数且非字典的类型，可能会导致 `op` 抛出错误。
- 用于合并 LLM 的 `usage_metadata` 时，它是 `AIMessageChunk` 等组件内部实现的核心逻辑。

## 相关链接
- [AIMessageChunk 使用说明](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/core/langchain_core/messages/ai.md)

---
**最后更新时间**: 2026-01-29
**对应源码版本**: LangChain Core v1.2.7
