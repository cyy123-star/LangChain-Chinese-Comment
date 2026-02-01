# VectorStore 实用工具模块文档

## 文件概述
`utils.py` 是 `langchain_core.vectorstores` 模块的内部实用工具库。它提供了一些底层的数学计算和算法实现，主要用于支持内存向量存储（`InMemoryVectorStore`）以及其他向量存储组件。

> **警告**: 该模块属于内部私有 API，其接口可能会在不经通知的情况下发生变化，建议普通用户不要直接使用。

## 导入依赖
- `numpy`: 核心数学库，用于矩阵运算和向量规范化。
- `simsimd` (可选): 高性能向量相似度计算库。如果安装了该库，会自动提速。
- `logging`, `warnings`: 用于输出调试信息和运行时警告。

## 类与函数详解

### 1. _cosine_similarity
**功能描述**: 计算两个等宽矩阵之间的行间余弦相似度。该函数支持 NumPy 原生实现，并优先使用 `simsimd` 进行加速（如果可用）。

#### 参数说明
| 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `x` | `Matrix` | - | 是 | 形状为 `(n, m)` 的矩阵（通常是查询向量）。 |
| `y` | `Matrix` | - | 是 | 形状为 `(k, m)` 的矩阵（通常是文档向量库）。 |

#### 返回值解释
- **类型**: `np.ndarray`
- **含义**: 形状为 `(n, k)` 的矩阵，其中 `(i, j)` 位置的值代表 `x` 的第 `i` 行与 `y` 的第 `j` 行之间的相似度分数。

#### 核心逻辑
1. **有效性检查**: 检查输入是否包含 NaN 或 Inf 值，并发出警告。
2. **加速方案**: 
    - 如果安装了 `simsimd`，调用其 `cdist` 方法以获取最高性能。
    - 否则，使用 NumPy 的 `np.dot` 和 `np.linalg.norm` 进行标准余弦相似度计算。
3. **异常处理**: 处理除以零的情况，将非法值设为 0.0。

---

### 2. maximal_marginal_relevance (MMR)
**功能描述**: 计算最大边际相关性。这是一种常用的重排序算法，旨在从搜索结果中挑选出既与查询高度相关，又相互之间具有多样性的文档。

#### 参数说明
| 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `query_embedding` | `np.ndarray` | - | 是 | 查询文本的嵌入向量。 |
| `embedding_list` | `list` | - | 是 | 待筛选的候选文档向量列表。 |
| `lambda_mult` | `float` | `0.5` | 否 | 平衡相关性和多样性的系数。1.0 完全侧重相关性，0.0 完全侧重多样性。 |
| `k` | `int` | `4` | 否 | 最终选出的文档数量。 |

#### 返回值解释
- **类型**: `list[int]`
- **含义**: 被选中的文档在 `embedding_list` 中的索引列表。

#### 核心逻辑
1. **初始化**: 选出与查询向量相似度最高的第一个文档。
2. **迭代选择**: 
    - 计算剩余文档与查询的相关性分数。
    - 计算剩余文档与已选中集合的最大相似度（冗余度）。
    - 根据公式 `score = lambda * similarity_to_query - (1 - lambda) * redundancy` 计算综合得分。
    - 选出得分最高的文档加入集合，重复直到达到数量 `k`。

## 使用示例
> 注意：以下为内部调用示例，通常由 `VectorStore` 类调用。
```python
import numpy as np
from langchain_core.vectorstores.utils import _cosine_similarity, maximal_marginal_relevance

# 模拟向量
query = np.array([0.1, 0.2, 0.3])
candidates = [
    np.array([0.1, 0.2, 0.3]),  # 完全一致
    np.array([0.1, 0.2, 0.31]), # 非常接近
    np.array([0.9, 0.1, 0.1])   # 差异较大
]

# 计算 MMR
selected_indices = maximal_marginal_relevance(
    query, 
    candidates, 
    k=2, 
    lambda_mult=0.5
)
# 结果会优先选第一个，然后为了多样性，可能会跳过第二个选第三个
print(selected_indices) 
```

## 注意事项
- **依赖性**: 必须安装 `numpy`。如果在大规模数据集上运行，强烈建议安装 `simsimd`。
- **维度匹配**: `x` 和 `y` 的列数（即向量维度）必须完全一致，否则会抛出 `ValueError`。

## 相关链接
- [Maximal Marginal Relevance 论文/算法介绍](https://www.cs.cmu.edu/~jgc/publication/The_Use_MMR_Diversity_Based_LTM_1998.pdf)

---
**最后更新时间**: 2026-01-29
**对应源码版本**: LangChain Core v1.2.7
