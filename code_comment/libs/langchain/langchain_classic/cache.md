# libs\langchain\langchain_classic\cache.py

此文档提供了 `libs\langchain\langchain_classic\cache.py` 文件的详细中文注释。该文件是一个动态导入层，用于导出各种 LLM 缓存实现。

## 文件概述

该文件主要负责将 `langchain_community.cache` 中的各种缓存实现重新导出到 `langchain.cache`（通过 `langchain_classic` 包装）。它使用了动态导入机制（`create_importer`），以便在用户导入这些类时能够发出弃用警告，并引导用户向 `langchain_community` 迁移。

## 支持的缓存实现

该模块导出了多种后端存储的缓存类，包括但不限于：

- **内存缓存**: `InMemoryCache`
- **关系型数据库**: `SQLiteCache`, `SQLAlchemyCache`
- **NoSQL / 键值存储**: `RedisCache`, `CassandraCache`, `UpstashRedisCache`, `MomentoCache`
- **向量/语义缓存**: `RedisSemanticCache`, `AstraDBSemanticCache`, `AzureCosmosDBSemanticCache`
- **专门化缓存**: `GPTCache`, `FullLLMCache`

## 核心机制：动态导入

文件使用 `create_importer` 和 `__getattr__` 实现了属性的按需加载：

1. **`DEPRECATED_LOOKUP`**: 定义了类名到其真实位置（通常是 `langchain_community.cache`）的映射。
2. **`__getattr__(name)`**: 当尝试从该模块访问某个属性时，动态触发导入并发出弃用提醒。

## 注意事项

1. **弃用说明**: 尽管可以继续从 `langchain.cache` 导入，但官方强烈建议直接从 `langchain_community.cache` 导入，以避免弃用警告并确保未来的兼容性。
2. **依赖项**: 大多数缓存后端（如 Redis, Cassandra, SQLAlchemy 等）需要安装额外的驱动包。
3. **全局设置**: 在 LangChain 中使用缓存通常通过设置 `langchain.globals.set_llm_cache(YourCache())` 来实现。

