# Chain Loading (serialization)

`loading` 模块提供了从序列化文件（JSON 或 YAML）加载 Chain 的功能。它支持从本地路径或 LangChain Hub 加载配置，并递归地实例化 Chain 及其子组件（如 LLM、Prompt 等）。

## 核心功能

- **load_chain**: 从文件路径加载 Chain。
- **load_chain_from_config**: 从配置字典加载 Chain。
- **递归加载**: 如果 Chain 的组件（如 `llm_chain`）也是一个配置，它会自动递归调用加载逻辑。

## 支持的 Chain 类型

该模块内置了对多种 Classic Chain 的加载支持，包括但不限于：
- `llm_chain`: 基础 LLM 链。
- `stuff_documents_chain`: 填充式文档合并链。
- `map_reduce_documents_chain`: 映射-归约文档合并链。
- `refine_documents_chain`: 迭代修正文档合并链。
- `retrieval_qa`: 检索问答链。
- `hyde_chain`: 假设文档嵌入链。

## 执行逻辑 (Verbatim Snippet)

### 基础加载逻辑
```python
def load_chain_from_config(config: dict, **kwargs: Any) -> Chain:
    """从配置字典加载 Chain。"""
    if "_type" not in config:
        raise ValueError("必须提供 `_type` 字段以识别 Chain 类型。")
    
    chain_type = config.pop("_type")
    
    # 根据 _type 映射到对应的加载函数
    if chain_type == "llm_chain":
        return _load_llm_chain(config, **kwargs)
    elif chain_type == "stuff_documents_chain":
        return _load_stuff_documents_chain(config, **kwargs)
    # ... 其他类型映射
```

### 递归加载示例 (StuffDocumentsChain)
```python
def _load_stuff_documents_chain(config: dict, **kwargs: Any) -> StuffDocumentsChain:
    # 加载内部的 llm_chain
    if "llm_chain" in config:
        llm_chain_config = config.pop("llm_chain")
        llm_chain = load_chain_from_config(llm_chain_config, **kwargs)
    elif "llm_chain_path" in config:
        llm_chain = load_chain(config.pop("llm_chain_path"), **kwargs)
    
    # 加载文档提示词
    if "document_prompt" in config:
        document_prompt = load_prompt_from_config(config.pop("document_prompt"))
    # ...
    
    return StuffDocumentsChain(llm_chain=llm_chain, document_prompt=document_prompt, **config)
```

## 迁移指南 (LCEL)

在 LCEL 中，序列化不再通过专门的 `loading` 模块完成，而是通过 `langchain-core` 中的 `dumpd` 和 `load` 函数实现统一的序列化支持：

```python
from langchain_core.load import dumpd, load

# 序列化
config = dumpd(my_runnable)

# 反序列化
my_runnable_reloaded = load(config)
```

这种新方式支持所有继承自 `Runnable` 的组件，且格式更加标准化。
