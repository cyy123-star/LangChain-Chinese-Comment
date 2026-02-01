# FakeEmbeddings & DeterministicFakeEmbedding

## 文件概述
`fake.py` 包含了一系列用于测试目的的模拟嵌入模型（Fake Embedding Models）。这些类允许开发者在不需要调用真实 API（如 OpenAI 或 Hugging Face）的情况下，模拟嵌入向量的生成，从而进行单元测试或流程验证。

## 导入依赖
- `hashlib`: 用于在 `DeterministicFakeEmbedding` 中根据文本内容生成确定的随机种子。
- `numpy`: 用于生成服从正态分布的随机数。
- `pydantic.BaseModel`: 提供参数验证。
- `langchain_core.embeddings.Embeddings`: 继承自标准嵌入接口。

## 类与函数详解

### 1. FakeEmbeddings
**功能描述**: 这是一个完全随机的模拟嵌入模型。每次调用都会从正态分布中采样生成全新的向量。

#### 核心属性
| 参数名 | 类型 | 是否必填 | 详细用途 |
| :--- | :--- | :--- | :--- |
| `size` | `int` | 是 | 嵌入向量的维度（长度）。 |

#### 使用示例
```python
from langchain_core.embeddings import FakeEmbeddings

# 创建一个维度为 100 的随机模拟模型
embed = FakeEmbeddings(size=100)
vector = embed.embed_query("测试文本")
print(len(vector)) # 100
```

---

### 2. DeterministicFakeEmbedding
**功能描述**: 这是一个**确定性**的模拟嵌入模型。它根据文本内容的哈希值作为随机种子。这意味着相同的文本始终会产生相同的“随机”向量。

#### 核心属性
| 参数名 | 类型 | 是否必填 | 详细用途 |
| :--- | :--- | :--- | :--- |
| `size` | `int` | 是 | 嵌入向量的维度。 |

#### 核心逻辑
- **种子生成**: 使用 `SHA-256` 计算文本哈希，取模后作为 `numpy` 随机生成器的种子。
- **确定性**: 保证了在测试过程中，相同的输入能得到可预测的输出，非常适合断言测试。

#### 使用示例
```python
from langchain_core.embeddings import DeterministicFakeEmbedding

embed = DeterministicFakeEmbedding(size=100)
v1 = embed.embed_query("Hello")
v2 = embed.embed_query("Hello")

assert v1 == v2 # 相同的文本产生相同的向量
```

#### 注意事项
- **!!! 警告**: 这些仅为**玩具模型**（Toy Models）。严禁在生产环境中使用，因为生成的向量不具备任何真实的语义含义。

## 相关链接
- [源码文件](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/core/langchain_core/embeddings/fake.py)

---
最后更新时间: 2026-01-29
对应源码版本: LangChain Core v1.2.7
