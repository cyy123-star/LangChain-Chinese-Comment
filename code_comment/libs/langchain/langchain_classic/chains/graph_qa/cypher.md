# libs\langchain\langchain_classic\chains\graph_qa\cypher.py

`GraphCypherQAChain` 是一个专门用于 Neo4j 图数据库的问答链。它能够将自然语言转换为 Cypher 查询语言，执行查询并返回解释性答案。

## 功能描述

该模块定义了与 Cypher 查询生成和执行相关的工具和链。主要功能包括：
1.  **Cypher 生成**：利用 LLM 将用户问题转化为 Cypher 语句。
2.  **Schema 提取**：自动获取 Neo4j 数据库的结构信息，用于辅助 Prompt 生成。
3.  **结果解析**：执行查询后，将原始数据转换回自然语言答案。

## 弃用说明

该文件已弃用，建议直接使用 `langchain_community` 中的对应实现。

| 类/属性 | 迁移目标 |
| :--- | :--- |
| `GraphCypherQAChain` | `langchain_community.chains.graph_qa.cypher.GraphCypherQAChain` |
| `CYPHER_GENERATION_PROMPT` | `langchain_community.chains.graph_qa.cypher.CYPHER_GENERATION_PROMPT` |
| `construct_schema` | `langchain_community.chains.graph_qa.cypher.construct_schema` |

## 核心组件逻辑

### 1. Schema 构造 (`construct_schema`)
通过查询 Neo4j 数据库，提取节点标签、关系类型以及它们的属性。这些信息会被注入到 Prompt 中，确保 LLM 知道可以查询哪些实体和关系。

### 2. Cypher 提取 (`extract_cypher`)
使用正则表达式从 LLM 生成的带有 Markdown 代码块的文本中提取纯净的 Cypher 语句。

## 迁移建议 (LCEL)

建议使用 `create_cypher_query_chain`（位于社区包中）来构建更灵活的流程。

### 现代用法示例

```python
from langchain.chains import create_cypher_query_chain
from langchain_community.graphs import Neo4jGraph
from langchain_openai import ChatOpenAI

graph = Neo4jGraph()
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# 创建 Cypher 生成链
chain = create_cypher_query_chain(llm, graph)

# 生成 Cypher 语句
response = chain.invoke({"question": "Who directed the movie Inception?"})
# 输出结果通常包含: {"query": "MATCH (p:Person)-[:DIRECTED]->(m:Movie {title: 'Inception'}) RETURN p.name"}
```

## 注意事项

1.  **方言限制**：该模块仅针对 Cypher 语言（Neo4j），不适用于 Gremlin 或 SPARQL。
2.  **Prompt 敏感性**：Cypher 的生成质量非常依赖于提供的 Schema 描述。
3.  **大图挑战**：对于拥有数百个节点类型和关系类型的超大型图，将完整 Schema 放入 Prompt 可能会导致上下文超出限制，建议进行 Schema 过滤。

