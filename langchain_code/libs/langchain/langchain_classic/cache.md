# Caching (缓存系统)

`cache` 模块提供了 LLM 响应的缓存机制。通过缓存，你可以避免对相同的输入重复调用昂贵的 LLM API，从而显著降低成本并提高响应速度。

## 核心价值

1. **节省成本**: 相同的提示词（Prompt）只需支付一次 Token 费用。
2. **加速开发**: 在测试和调试阶段，缓存可以提供瞬时的响应。
3. **确定性**: 对于给定的输入，缓存可以保证返回完全一致的输出。

## 缓存类型

### 1. 内存缓存 (`InMemoryCache`)
最简单的缓存方式，数据存储在 Python 进程的内存中。
- **优点**: 速度极快，无需额外配置。
- **缺点**: 进程重启后数据丢失。

### 2. 数据库缓存
适用于需要跨进程或长期持久化缓存的场景。
- `SQLiteCache`: 使用本地 SQLite 数据库。
- `RedisCache`: 使用 Redis 内存数据库，支持分布式。
- `SQLAlchemyCache`: 支持任何 SQLAlchemy 兼容的数据库（如 Postgres, MySQL）。

### 3. 语义缓存 (`Semantic Cache`)
这是一种更高级的缓存方式，它不要求输入文本完全一致，而是通过**嵌入（Embedding）**和**向量搜索**来查找语义相似的请求。
- `RedisSemanticCache`: 基于 Redis 的语义缓存。
- `AstraDBSemanticCache`: 基于 Astra DB 的语义缓存。

## 使用方法

缓存可以在全局范围内设置：

```python
import langchain
from langchain_community.cache import InMemoryCache
from langchain_openai import ChatOpenAI

# 设置全局缓存
langchain.llm_cache = InMemoryCache()

llm = ChatOpenAI()

# 第一次调用：会发送到 OpenAI
llm.invoke("Tell me a joke")

# 第二次调用：直接从内存中读取
llm.invoke("Tell me a joke")
```

## 注意事项

- **安全性**: 缓存可能包含敏感信息，请确保缓存存储（如 Redis）的安全。
- **一致性**: 如果你修改了模型的参数（如 `temperature`），缓存可能不再适用，需要手动清理或使用不同的缓存键。
- **语义缓存阈值**: 语义缓存通常需要配置一个相似度分数阈值（`score_threshold`），以决定什么样的相似度算作“命中”。

## 迁移指南

虽然 `langchain_classic` 提供了这些类的入口，但实际的实现已经移到了 `langchain_community` 中。建议在新项目中直接从 `langchain_community.cache` 导入。
