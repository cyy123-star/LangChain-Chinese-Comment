# Graphs (图数据库集成)

`graphs` 模块提供了与各种图数据库（Graph Databases）交互的统一接口。它允许 LangChain 应用（特别是 Graph QA 链）查询和操作图形结构的数据。

## 核心接口

### `BaseGraph`
所有图数据库集成的基类。它定义了执行查询、获取架构（Schema）和结构化数据的标准方法。

## 常用图数据库实现

| 数据库 | 说明 |
| :--- | :--- |
| `Neo4jGraph` | 最流行的图数据库实现，支持 Cypher 查询语言。 |
| `NetworkxGraph` | 在内存中运行的小型图结构，适合本地测试和算法演示。 |
| `ArangoDBGraph` | 多模态数据库的图功能实现。 |
| `MemgraphGraph` | 高性能的内存图数据库。 |
| `NebulaGraph` | 分布式图数据库。 |
| `RdfGraph` | 处理 RDF (Resource Description Framework) 三元组数据。 |

## 核心功能

1. **Schema 提取**: 自动从数据库中提取节点标签（Labels）、关系类型（Relationship Types）和属性，辅助 LLM 生成正确的查询语句。
2. **查询执行**: 安全地执行由 LLM 生成的 Cypher 或 Gremlin 查询。
3. **GraphDocument**: 定义了将非结构化文档转换为图结构的中间格式。

## 使用示例

```python
from langchain_community.graphs import Neo4jGraph

graph = Neo4jGraph(url="bolt://localhost:7687", username="neo4j", password="password")

# 查看数据库架构
print(graph.get_schema)

# 执行查询
result = graph.query("MATCH (p:Person) RETURN p.name LIMIT 5")
```

## 迁移与集成

- **集成分离**: 具体的图数据库驱动现在主要位于 `langchain-community` 中。
- **LangGraph**: 虽然本模块名为 `graphs`，但它主要处理图**数据库**。对于定义应用逻辑的**状态图**，请参考 `LangGraph` 库。
