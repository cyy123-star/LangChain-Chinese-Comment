# libs\langchain\langchain_classic\embeddings\base.py

此文档提供了 `libs\langchain\langchain_classic\embeddings\base.py` 文件的详细中文注释。该模块主要定义了嵌入模型（Embeddings）的统一初始化接口。

## 文件概述

在 LangChain 0.3.9+ 版本中，推荐使用统一的 `init_embeddings` 函数来初始化不同供应商的嵌入模型。该模块实现了这个工厂函数，支持通过模型字符串或显式参数来创建嵌入模型实例。

## 核心函数：`init_embeddings`

该函数允许通过统一的接口初始化任何支持的供应商嵌入模型。

### 1. 主要功能

- **统一入口**：通过单一函数即可初始化 OpenAI, Bedrock, Cohere 等多种后端的嵌入模型。
- **智能推断**：支持解析 `provider:model` 格式的字符串自动推断供应商。
- **动态加载**：按需导入相应的集成包，减少不必要的依赖加载。

### 2. 参数说明

| 参数 | 类型 | 描述 |
| :--- | :--- | :--- |
| `model` | `str` | 模型名称。支持 `'provider:model'` 格式（如 `'openai:text-embedding-3-small'`）或仅模型名。 |
| `provider` | `str \| None` | 显式指定供应商名称。如果 `model` 参数中包含前缀，此参数可选。 |
| `**kwargs` | `Any` | 传递给底层嵌入模型构造函数的其他参数（如 `api_key`, `base_url` 等）。 |

### 3. 支持的供应商

- `openai` -> `langchain-openai`
- `azure_openai` -> `langchain-openai`
- `bedrock` -> `langchain-aws`
- `cohere` -> `langchain-cohere`
- `google_genai` / `google_vertexai` -> `langchain-google-genai` / `langchain-google-vertexai`
- `huggingface` -> `langchain-huggingface`
- `mistralai` -> `langchain-mistralai`
- `ollama` -> `langchain-ollama`

---

## 使用示例

### 1. 使用模型字符串
```python
from langchain.embeddings import init_embeddings

# 格式: provider:model
model = init_embeddings("openai:text-embedding-3-small")
vector = model.embed_query("你好，世界！")
```

### 2. 显式指定供应商
```python
# 显式分离模型名和供应商
model = init_embeddings(model="text-embedding-3-small", provider="openai")
```

### 3. 传递额外参数
```python
# 传递 api_key 等参数
model = init_embeddings(
    "openai:text-embedding-3-small",
    api_key="sk-..."
)
```

## 注意事项

1. **依赖安装**：必须预先安装对应供应商的集成包（例如 `pip install langchain-openai`）。
2. **格式要求**：如果仅提供模型名且未指定供应商，或者格式不正确，将抛出 `ValueError`。
3. **版本要求**：该功能是在 `langchain` 0.3.9 版本中新增的。

