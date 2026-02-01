# libs\langchain\langchain_classic\chains\graph_qa\base.py

`GraphQAChain` 是一个用于在图数据库上进行自然语言问答的通用链。它能够将自然语言问题转化为图查询，并基于图数据库的返回结果生成答案。

## 功能描述

该模块目前作为 `langchain_community` 中对应功能的动态导入层。其核心逻辑通常包括：
1.  **查询生成**：根据用户问题和图 Schema 生成图查询语句。
2.  **查询执行**：在关联的图数据库上执行生成的查询。
3.  **答案合成**：结合原始问题和查询结果，由 LLM 生成最终的自然语言回答。

## 弃用说明

该文件已被标记为弃用。核心功能已迁移至 `langchain_community`。

| 类/属性 | 迁移目标 |
| :--- | :--- |
| `GraphQAChain` | `langchain_community.chains.graph_qa.base.GraphQAChain` |

## 迁移建议 (LCEL)

虽然 `GraphQAChain` 仍然可用，但建议使用更现代的 LCEL (LangChain Expression Language) 模式来构建图问答链。

### 示例：构建图问答流程

```python
from langchain_community.graphs import Neo4jGraph
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# 1. 准备图数据库和 LLM
graph = Neo4jGraph()
# 2. 定义查询生成链
query_prompt = ChatPromptTemplate.from_template("Generate a query for: {question}")
query_chain = query_prompt | llm | StrOutputParser()

# 3. 定义答案生成链
qa_prompt = ChatPromptTemplate.from_template("Answer based on: {context}")
qa_chain = qa_prompt | llm

# 4. 组合完整流程 (伪代码)
full_chain = (
    {"question": RunnablePassthrough()} 
    | query_chain 
    | graph.query 
    | (lambda x: {"context": x, "question": ...})
    | qa_chain
)
```

## 注意事项

1.  **环境依赖**：使用此类通常需要安装特定的图数据库驱动（如 `neo4j`）。
2.  **Schema 注入**：图问答的准确性高度依赖于提供给 LLM 的图 Schema（节点标签、属性、关系类型等）的完整性。
3.  **安全性**：生成的查询直接在数据库上运行，应确保数据库账号权限受限（只读）。

