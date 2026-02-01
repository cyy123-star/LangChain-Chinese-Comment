# Storage (持久化存储)

`storage` 模块提供了一套用于存储大块数据（如文档、向量或原始文本）的键值对（Key-Value）存储接口。

## 核心接口

### `BaseStore`
所有存储实现的抽象基类。它定义了四个核心操作：
- `mget(keys)`: 批量获取。
- `mset(key_value_pairs)`: 批量设置。
- `mdelete(keys)`: 批量删除。
- `yield_keys(prefix)`: 迭代所有键。

## 常见实现

| 实现类 | 存储介质 | 适用场景 |
| :--- | :--- | :--- |
| `InMemoryStore` | 内存 (Dict) | 测试、短期缓存、单机小规模应用。 |
| `LocalFileStore` | 本地文件系统 | 需要简单持久化且不具备数据库环境时。 |
| `RedisStore` | Redis 数据库 | 分布式环境、高性能缓存、高并发访问。 |
| `UpstashRedisStore` | Serverless Redis | 云原生应用，按量计费。 |

## 高级用法：`EncoderBackedStore`

`EncoderBackedStore` 允许你在存取数据时自动进行序列化和反序列化（例如将对象转换为 JSON 字符串存入 Redis，读取时还原为 Pydantic 模型）。

## 应用场景

1. **缓存 (Caching)**: 缓存 LLM 的响应以节省费用和时间。
2. **多向量检索 (Multi-Vector Retrieval)**: 在向量库中存储摘要/切片，在 `Storage` 中存储对应的完整大文档。
3. **父文档检索 (Parent Document Retrieval)**: 存储父文档原始内容。

## 使用示例

```python
from langchain.storage import RedisStore

store = RedisStore(redis_url="redis://localhost:6379")

# 批量设置
store.mset([("key1", b"value1"), ("key2", b"value2")])

# 批量获取
values = store.mget(["key1", "key2"])
```

## 迁移说明

- **标准化**: 所有的存储接口现在由 `langchain-core` 统一。
- **扩展性**: 通过继承 `BaseStore`，开发者可以轻松实现自定义的存储后端（如 MinIO, SQL 数据库等）。
