# structured_query.py - 结构化查询语言中间表示 (IR)

- **最后更新时间**: 2026-01-29
- **对应源码版本**: LangChain Core v1.2.7

## 文件概述

`structured_query.py` 定义了 LangChain 内部用于结构化查询的中间表示（Intermediate Representation, IR）。这套系统允许用户以一种平台无关的方式表达复杂的查询逻辑（如过滤、比较和逻辑运算），然后通过访问者模式（Visitor Pattern）将其转换为特定向量数据库（如 Pinecone, Chroma, Elasticsearch 等）的原生查询语言。

## 导入依赖

| 依赖模块 | 作用 |
| :--- | :--- |
| `abc` | 提供抽象基类支持。 |
| `enum` | 提供枚举类型支持，用于定义操作符和比较符。 |
| `typing` | 提供类型提示。 |
| `pydantic` | 提供 `BaseModel` 用于定义表达式的数据模型。 |

## 类与函数详解

### 1. Visitor (ABC)

定义了将中间表示转换为特定后端语言的接口。

#### 功能描述
采用访问者模式，为每种类型的表达式（Operation, Comparison, StructuredQuery）定义了对应的 `visit_*` 方法。

#### 方法说明

| 方法名 | 参数 | 返回值 | 功能描述 |
| :--- | :--- | :--- | :--- |
| `visit_operation` | `operation: Operation` | `Any` | 转换逻辑运算（如 AND, OR）。 |
| `visit_comparison` | `comparison: Comparison` | `Any` | 转换比较运算（如 EQ, GT）。 |
| `visit_structured_query`| `structured_query: StructuredQuery`| `Any` | 转换整个结构化查询对象。 |

---

### 2. Expr (BaseModel)

所有表达式的基类。

#### 方法说明

| 方法名 | 参数 | 返回值 | 功能描述 |
| :--- | :--- | :--- | :--- |
| `accept` | `visitor: Visitor` | `Any` | 接受访问者，并根据类名分发到对应的 `visit_*` 方法。 |

---

### 3. 核心枚举类型

#### Operator (Enum)
逻辑操作符：`AND`, `OR`, `NOT`。

#### Comparator (Enum)
比较操作符：`EQ` (等于), `NE` (不等于), `GT` (大于), `GTE` (大于等于), `LT` (小于), `LTE` (小于等于), `CONTAIN` (包含), `LIKE` (模糊匹配), `IN` (在列表中), `NIN` (不在列表中)。

---

### 4. 核心表达式类

#### Comparison
代表一个属性与一个值的比较。包含 `comparator`, `attribute`, `value` 三个字段。

#### Operation
代表多个过滤指令之间的逻辑运算。包含 `operator` 和 `arguments` (指令列表)。

#### StructuredQuery
完整的结构化查询。包含 `query` (查询字符串), `filter` (过滤指令), `limit` (结果数量限制)。

## 核心逻辑

- **访问者模式分发**: `Expr.accept` 方法通过将类名转换为蛇形命名（Snake Case），动态调用访问者上对应的方法。例如，`StructuredQuery` 类会调用 `visitor.visit_structured_query`。
- **验证机制**: `Visitor` 基类提供了 `_validate_func` 方法，用于检查传入的操作符或比较符是否在后端支持的允许列表中。

## 使用示例

```python
from langchain_core.structured_query import (
    Comparison, 
    Comparator, 
    Operation, 
    Operator, 
    StructuredQuery
)

# 构建一个查询：查找作者是 "Jane" 且评分大于 9 的文档，限制返回 5 条
query = StructuredQuery(
    query="关于 AI 的研究",
    filter=Operation(
        operator=Operator.AND,
        arguments=[
            Comparison(comparator=Comparator.EQ, attribute="author", value="Jane"),
            Comparison(comparator=Comparator.GT, attribute="rating", value=9)
        ]
    ),
    limit=5
)

# 打印表达式结构
print(query)
```

## 注意事项

- **平台无关性**: 该 IR 并不直接执行查询，它只是一个描述符。
- **扩展性**: 如果要支持新的向量数据库，只需实现一个新的 `Visitor` 子类。
- **Pydantic 序列化**: 所有表达式都是 Pydantic 模型，支持方便的 JSON 序列化和反序列化。

## 内部调用关系

- **被调用**: 主要被 `SelfQueryRetriever` 调用，用于将自然语言转换后的结构化指令映射到向量存储的过滤参数上。
- **转换流程**: 自然语言 -> LLM 解析 -> `StructuredQuery` 对象 -> `Visitor` 实现 -> 数据库原生 DSL。

## 相关链接
- [Retriever 源码文档](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/core/langchain_core/retrievers.md)
- [Pydantic 官方文档](https://docs.pydantic.dev/)
