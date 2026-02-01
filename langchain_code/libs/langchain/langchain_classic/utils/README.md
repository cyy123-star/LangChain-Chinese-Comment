# Utils (底层辅助工具)

`utils` 模块包含了一系列跨组件通用的底层辅助函数。它们处理一些琐碎但重要的任务，如字符串格式化、数学计算、环境检测等。

## 核心组件

| 工具 | 说明 |
| :--- | :--- |
| `openai_functions.py` | 提供了在 LangChain 对象和 OpenAI 函数调用（Function Calling）参数格式之间转换的工具。 |
| `math.py` | 包含余弦相似度（Cosine Similarity）等常用的向量计算函数。 |
| `env.py` | 统一管理环境变量的读取和验证。 |
| `formatting.py` | 字符串模板的高级格式化工具。 |
| `pydantic.py` | 增强对 Pydantic 模型的动态创建和验证支持。 |
| `aiter.py` / `iter.py` | 异步和同步迭代器的增强工具，用于流式处理。 |

## 关键功能：OpenAI 函数转换

该模块中的 `convert_to_openai_function` 等函数是实现 Agent 工具调用的关键：
- 将 Pydantic 类或 Python 函数转换为 OpenAI 要求的 JSON Schema。

## 使用示例

```python
from langchain.utils.math import cosine_similarity

# 计算两个向量的相似度
similarity = cosine_similarity([[1.0, 0.0]], [[0.8, 0.6]])
print(similarity)
```

## 注意事项

- **内部使用**: 本模块中的许多函数主要供 LangChain 内部组件使用，但开发者在实现自定义组件时也可以利用它们。
- **标准化**: 随着核心库的演进，许多通用工具已迁移到 `langchain-core` 的 `utils` 子包中。
