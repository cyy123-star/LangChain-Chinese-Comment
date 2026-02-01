# rate_limiters.py - 频率限制器接口与实现

- **最后更新时间**: 2026-01-29
- **对应源码版本**: LangChain Core v1.2.7

## 文件概述

`rate_limiters.py` 定义了 LangChain 的频率限制系统。它提供了一个抽象基类 `BaseRateLimiter` 和一个基于令牌桶算法（Token Bucket）的内存实现 `InMemoryRateLimiter`。该模块的主要目的是控制对外部 API（如 LLM 提供商）的请求频率，防止因请求过快而触发服务端的配额限制。

## 导入依赖

| 依赖模块 | 作用 |
| :--- | :--- |
| `abc` | 提供抽象基类支持。 |
| `asyncio` | 提供异步支持。 |
| `threading` | 提供多线程支持和锁机制。 |
| `time` | 提供时间戳和休眠功能。 |

## 类详解

### 1. BaseRateLimiter (ABC)

频率限制器的抽象基类。

#### 功能描述
定义了获取“令牌”（许可）的标准接口，支持同步和异步调用。所有的频率限制逻辑都应通过 `acquire` 或 `aacquire` 方法触发。

#### 方法说明

| 方法名 | 类型 | 参数 | 返回值 | 功能描述 |
| :--- | :--- | :--- | :--- | :--- |
| `acquire` | 抽象方法 | `blocking: bool = True` | `bool` | 同步尝试获取令牌。如果 `blocking` 为 True，则阻塞直到成功。 |
| `aacquire` | 异步抽象方法 | `blocking: bool = True` | `bool` | 异步尝试获取令牌。如果 `blocking` 为 True，则等待直到成功。 |

---

### 2. InMemoryRateLimiter (BaseRateLimiter)

基于令牌桶算法的内存频率限制器实现。

#### 功能描述
该实现通过在内存中维护一个“令牌桶”来控制请求速率。桶以恒定速率填充令牌，每个请求消耗一个令牌。它具有以下特点：
- **线程安全**: 可以在多线程环境中使用。
- **混合支持**: 同时支持同步和异步代码。
- **突发控制**: 通过 `max_bucket_size` 允许一定程度的突发请求，但会限制长期平均速率。

#### 参数说明

| 参数名 | 类型 | 默认值 | 是否必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `requests_per_second` | `float` | `1` | 否 | 每秒生成的令牌数（即每秒允许的请求数）。 |
| `check_every_n_seconds` | `float` | `0.1` | 否 | 检查令牌是否可用的频率（秒）。 |
| `max_bucket_size` | `float` | `1` | 否 | 桶的最大容量，用于控制最大突发请求数。 |

#### 核心逻辑
1. **令牌填充**: 每次调用 `_consume` 时，根据自上次调用以来流逝的时间计算应新增的令牌。
2. **令牌消耗**: 如果桶中令牌数 $\ge 1$，则减去 1 并返回 `True`；否则返回 `False`。
3. **阻塞逻辑**: 如果 `blocking=True`，则在一个循环中不断调用 `_consume`，若不成功则休眠 `check_every_n_seconds` 秒。

#### 使用示例

```python
import time
from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain_openai import ChatOpenAI

# 创建一个限制器：每 10 秒允许 1 个请求
rate_limiter = InMemoryRateLimiter(
    requests_per_second=0.1, 
    max_bucket_size=1
)

# 将限制器传递给模型
model = ChatOpenAI(rate_limiter=rate_limiter)

# 连续调用
for i in range(3):
    start = time.time()
    response = model.invoke("你好")
    print(f"请求 {i+1} 耗时: {time.time() - start:.2f}s")
```

#### 注意事项
- **非跨进程**: 由于是内存实现，无法跨不同的 Python 进程进行频率限制。
- **与 LLM 令牌无关**: 这里的“令牌”是指“请求许可”，而不是 LLM 生成的文字令牌（Tokens）。
- **可观测性**: 目前频率限制的等待时间不会体现在回调或追踪中，而是计入总调用时长。

## 内部调用关系

- **集成**: 通常作为参数传递给 `BaseChatModel` 或 `BaseLLM` 的构造函数。
- **并发控制**: 内部使用 `threading.Lock` 保证令牌计数在多线程下的准确性。

## 相关链接
- [BaseChatModel 源码文档](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/core/langchain_core/language_models/chat_models.md)
- [令牌桶算法百科](https://baike.baidu.com/item/%E4%BB%A4%E7%89%8C%E6%A1%B6%E7%AE%97%E6%B3%95)
