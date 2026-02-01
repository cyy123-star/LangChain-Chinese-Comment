# aiter.py - 异步迭代器工具

`aiter.py` 模块提供了一系列用于处理异步迭代器（AsyncIterator）的实用工具函数，旨在增强对异步流的操作能力。

## 文件概述

该文件主要包含异步迭代器的模拟实现（如 `anext` 的 Python 版本）以及异步版本的 `tee` 操作，用于将一个异步迭代器拆分为多个独立的异步迭代器。

## 导入依赖

| 依赖模块 | 作用 |
| :--- | :--- |
| `collections` | 使用 `deque` 作为异步缓冲。 |
| `typing` | 提供类型注解支持（`AsyncIterator`, `Awaitable`, `TypeVar` 等）。 |
| `langchain_core._api` | 使用 `deprecated` 装饰器标记过时接口。 |

## 函数详解

### `py_anext`

#### 功能描述
异步迭代器 `anext()` 的纯 Python 实现，主要用于测试或在不支持原生 `anext` 的环境中使用。

#### 参数说明
| 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `iterator` | `AsyncIterator[T]` | - | 是 | 要获取下一个元素的异步迭代器。 |
| `default` | `T \| Any` | `_no_default` | 否 | 当迭代器耗尽时返回的默认值。 |

#### 返回值解释
返回迭代器的下一个值。如果迭代器耗尽且提供了 `default`，则返回 `default`；否则抛出 `StopAsyncIteration`。

---

### `atee`

#### 功能描述
将一个异步迭代器拆分为多个独立的异步迭代器。类似于 `itertools.tee` 的异步版本。

#### 参数说明
| 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `iterable` | `AsyncIterator[T]` | - | 是 | 源异步迭代器。 |
| `n` | `int` | `2` | 否 | 要生成的副本数量。 |

#### 返回值解释
返回一个包含 `n` 个异步迭代器的元组。

#### 核心逻辑
1. 为每个副本创建一个 `deque` 缓冲区。
2. 使用一个锁（Lock）确保在从源迭代器拉取新数据时是线程/协程安全的。
3. 当某个副本需要数据时：
   - 如果自己的缓冲区有数据，直接弹出。
   - 如果没有，则通过锁竞争从源迭代器获取新数据，并分发给所有副本的缓冲区。

---

## 使用示例

```python
import asyncio
from langchain_core.utils.aiter import atee

async def async_gen():
    for i in range(3):
        await asyncio.sleep(0.1)
        yield i

async def main():
    it1, it2 = atee(async_gen())
    
    # 同时消费两个迭代器
    async for val in it1:
        print(f"It1: {val}")
    
    async for val in it2:
        print(f"It2: {val}")

asyncio.run(main())
```

## 注意事项
- `py_anext` 已被标记为过时（`deprecated`），建议在生产环境中使用原生 `anext`（Python 3.10+）。
- `atee` 会在内存中维护缓冲区，如果不同副本的消费速度差异极大，可能会导致内存占用增加。

## 相关链接
- [Python AsyncIterator 文档](https://docs.python.org/3/library/stdtypes.html#async-iterators)
- [itertools.tee](https://docs.python.org/3/library/itertools.html#itertools.tee)

---
**最后更新时间**: 2026-01-29
**对应源码版本**: LangChain Core v1.2.7
