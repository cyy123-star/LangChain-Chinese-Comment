# iter.py - 迭代器工具

`iter.py` 模块提供了用于操作同步迭代器（Iterator）的实用工具。

## 文件概述

该文件目前主要包含同步版本的 `tee` 操作。它允许将一个迭代器安全地拆分为多个独立的迭代器副本，且每个副本都可以独立消费数据。

## 导入依赖

| 依赖模块 | 作用 |
| :--- | :--- |
| `collections` | 使用 `deque` 作为缓冲区。 |
| `threading` | 使用 `Lock` 确保线程安全。 |
| `typing` | 提供类型注解支持（`Iterator`, `Generator`, `List`, `Any` 等）。 |

## 函数详解

### `tee`

#### 功能描述
将一个迭代器拆分为 `n` 个独立的迭代器副本。

#### 参数说明
| 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `iterable` | `Iterator[T]` | - | 是 | 源迭代器。 |
| `n` | `int` | `2` | 否 | 要生成的副本数量。 |

#### 返回值解释
`tuple[Iterator[T], ...]`: 返回包含 `n` 个迭代器的元组。

#### 核心逻辑
1. 内部维护一个 `lock` 和多个 `deque` 队列（每个副本对应一个）。
2. `tee_peer` 生成器函数定义了副本的行为：
   - 检查自己的队列是否有数据。
   - 如果没有，竞争锁，从源迭代器获取下一个元素。
   - 获取到元素后，将其添加到**所有**副本的队列中。
   - 从自己的队列弹出并返回。

---

## 使用示例

```python
from langchain_core.utils.iter import tee

# 源迭代器
nums = iter([1, 2, 3])

# 拆分为两个副本
it1, it2 = tee(nums)

print(next(it1))  # 输出: 1
print(next(it2))  # 输出: 1
print(next(it2))  # 输出: 2
print(next(it1))  # 输出: 2
```

## 注意事项
- **内存消耗**：如果其中一个副本被消费得很快，而另一个副本完全不消费，那么不消费的副本对应的 `deque` 会不断增长，直到存储了源迭代器的所有剩余数据。
- **线程安全**：该实现使用了 `threading.Lock`，因此在多线程环境下是安全的。

## 相关链接
- [Python itertools.tee 文档](https://docs.python.org/3/library/itertools.html#itertools.tee)

---
**最后更新时间**: 2026-01-29
**对应源码版本**: LangChain Core v1.2.7
