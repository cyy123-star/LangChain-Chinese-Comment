# Rate Limiters (速率限制器)

`rate_limiters` 模块提供了对模型 API 调用频率进行控制的抽象和实现。这在多租户应用或需要严格遵守 API 提供商配额限制的场景中至关重要。

## 核心组件

### 1. BaseRateLimiter
所有速率限制器的抽象基类。定义了获取令牌（Token）的核心接口，支持同步和异步调用。

### 2. InMemoryRateLimiter
基于内存的令牌桶算法实现。
- **原理**: 令牌以固定速率生成并放入桶中。每次 API 请求前需要从桶中获取令牌，如果桶空了，请求将等待直到有新令牌产生。
- **适用场景**: 单进程、单节点的速率控制。

## 使用方法

通常将速率限制器实例作为 `rate_limiter` 参数传递给聊天模型初始化函数：

```python
from langchain.chat_models import init_chat_model
from langchain.rate_limiters import InMemoryRateLimiter

# 定义每秒最多 2 个请求的限制器
rate_limiter = InMemoryRateLimiter(
    requests_per_second=2.0, 
    check_every_n_seconds=0.1,
    max_bucket_size=10
)

# 绑定到模型
model = init_chat_model(
    "openai:gpt-4o", 
    rate_limiter=rate_limiter
)
```

## 注意事项
- **线程安全**: `InMemoryRateLimiter` 是线程安全的。
- **分布式限制**: 目前内置实现仅限于单机内存。如果需要分布式环境下的速率限制（如 Redis 支撑），通常需要自定义继承自 `BaseRateLimiter` 的类。
