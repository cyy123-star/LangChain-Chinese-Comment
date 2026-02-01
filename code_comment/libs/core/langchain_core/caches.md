# caches.py - LLM 缓存层

- **最后更新时间**: 2026-01-29
- **对应源码版本**: LangChain Core v1.2.7

## 文件概述

`caches.py` 定义了语言模型（LLM/Chat Model）的可选缓存层。缓存可以显著减少对模型提供商的 API 调用次数，从而节省成本并加快应用程序响应速度。

> **注意**: 该功能目前处于 Beta 阶段。

## 导入依赖

| 模块 | 作用 |
| :--- | :--- |
| `langchain_core.outputs.Generation` | 缓存存储的核心数据对象。 |
| `langchain_core.runnables.run_in_executor` | 用于在线程池中执行同步操作以提供默认异步实现。 |

## 类与函数详解

### 1. BaseCache (抽象基类)
- **功能描述**: 所有缓存实现的通用接口。定义了查找、更新和清理缓存的标准方法。
- **核心方法**:
  - **lookup(prompt, llm_string)**: **抽象方法**。根据 Prompt 和 LLM 配置字符串查找缓存。命中则返回 `Generation` 列表，未命中返回 `None`。
  - **update(prompt, llm_string, return_val)**: **抽象方法**。将模型生成的响应存入缓存。
  - **clear(**kwargs)**: **抽象方法**。清空缓存。
  - **alookup / aupdate / aclear**: 对应异步版本，默认在线程池中运行。

### 2. InMemoryCache
- **功能描述**: 将缓存数据存储在内存字典中的简单实现。

## 核心逻辑

1. **Key 生成**: 缓存通常将 `prompt`（序列化后的提示词）和 `llm_string`（包含模型名、温度等参数的序列化字符串）组合作为唯一的缓存键。
2. **异步支持**: 对于没有原生异步支持的缓存，默认会使用 `run_in_executor` 在独立线程中运行同步逻辑。

## 使用场景

- **开发测试**: 避免在调试时反复调用收费 API。
- **高频重复查询**: 针对固定输入的 FAQ 或常用指令。

## 使用示例

```python
from langchain_core.globals import set_llm_cache
from langchain_core.caches import InMemoryCache

# 设置全局缓存
set_llm_cache(InMemoryCache())

# 后续的所有 LLM 调用都将自动尝试从缓存中获取结果
```

## 相关链接
- [langchain_core.globals](globals.md) (用于设置全局缓存)
- [langchain_core.outputs](file:///d%3A/TraeProjects/langchain_code_comment/code_comment/libs/core/langchain_core/outputs/generation.md)
