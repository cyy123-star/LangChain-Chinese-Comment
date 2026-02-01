# Graph QA Chains

Graph QA 链用于将自然语言查询转换为图数据库特定的查询语言（如 Cypher, Gremlin, SPARQL 等），执行查询并返回结果。

> **注意**: `langchain_classic` 中的 Graph QA 相关类目前主要作为 `langchain_community.chains.graph_qa` 的导入代理。

## 核心功能

这类链的核心逻辑通常包含两个主要步骤：
1. **查询生成**: 利用 LLM 将用户的问题和图数据库的 Schema（节点、边、属性信息）转换为特定语言的查询语句。
2. **查询执行与总结**: 在图数据库上运行生成的查询，并将结果（通常是原始数据或路径）交回给 LLM 总结成自然语言回答。

## 支持的数据库与语言

| 链名称 | 数据库/语言 | 说明 |
| :--- | :--- | :--- |
| `GraphCypherQAChain` | Neo4j / Cypher | 最常用的图 QA 链，支持模式验证和校正。 |
| `ArangoGraphQAChain` | ArangoDB / AQL | 针对 ArangoDB 的多模型数据库设计。 |
| `GremlinQAChain` | Gremlin | 支持所有兼容 Gremlin 的图数据库（如 Amazon Neptune, JanusGraph）。 |
| `NeptuneSparqlQAChain` | Neptune / SPARQL | 针对 RDF 图数据的查询。 |
| `KuzuQAChain` | Kuzu | 嵌入式图数据库。 |

## 核心组件 (以 Cypher 为例)

| 参数 | 类型 | 说明 |
| :--- | :--- | :--- |
| `graph` | `GraphStore` | 图数据库的连接句柄。 |
| `cypher_generation_chain` | `LLMChain` | 用于生成 Cypher 语句的链。 |
| `qa_chain` | `LLMChain` | 用于根据查询结果生成最终回答的链。 |
| `validate_cypher` | `bool` | 是否在执行前验证生成的 Cypher 语句的语法。 |

## 迁移指南

对于所有 Graph QA 链，建议直接从 `langchain_community` 导入：

```python
# 推荐写法
from langchain_community.chains.graph_qa.cypher import GraphCypherQAChain
from langchain_community.graphs import Neo4jGraph
```

对于更复杂的图交互逻辑，建议参考 [LangGraph 图数据库示例](https://langchain-ai.github.io/langgraph/how-tos/graph-qa/)。
