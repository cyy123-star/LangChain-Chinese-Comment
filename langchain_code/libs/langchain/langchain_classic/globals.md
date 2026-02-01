# Globals (全局配置)

`globals` 模块管理影响整个 LangChain 运行行为的全局状态。

## 核心配置项

### 1. 详细模式 (Verbose)
- **`set_verbose(bool)`**: 控制是否打印 Chain 运行过程中的详细内部日志。
- **`get_verbose()`**: 获取当前的详细模式状态。

### 2. 调试模式 (Debug)
- **`set_debug(bool)`**: 开启后，将打印最底层的运行信息，包括所有的 Prompt 详情和模型原始返回。
- **`get_debug()`**: 获取当前的调试模式状态。

### 3. 全局缓存 (LLM Cache)
- **`set_llm_cache(BaseCache)`**: 设置一个全局生效的 LLM 响应缓存。
- **`get_llm_cache()`**: 获取当前的全局缓存对象。

## 使用建议

- **开发阶段**: 建议开启 `verbose=True` 或 `debug=True` 以便快速定位问题。
- **生产阶段**: 除非有特殊审计需求，否则建议关闭这些全局日志输出以保持整洁并降低开销。
- **缓存策略**: 在生产环境中使用全局缓存（如 RedisCache）可以显著降低 API 调用费用。

## 迁移说明

这些功能已迁移至 `langchain_core.globals`。在 `langchain_classic` 中保留这些入口是为了兼容旧代码：

```python
import langchain

# 传统设置方式
langchain.verbose = True
langchain.debug = True

# 现代设置方式 (推荐)
from langchain_core.globals import set_debug
set_debug(True)
```
