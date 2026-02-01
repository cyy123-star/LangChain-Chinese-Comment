# libs\langchain\langchain_classic\agents\agent_toolkits\conversational_retrieval\tool.py

该模块提供了一个辅助函数，用于将检索器（Retriever）包装成代理可以使用的工具。

## 核心功能

### `create_retriever_tool`

该函数实际上是对 `langchain_classic.tools.retriever.create_retriever_tool` 的重新导出（Re-export）。

#### 参数说明

- `retriever`: `BaseRetriever` 类型，底层的检索器实例。
- `name`: `str` 类型，工具的名称。代理将使用这个名称来调用该工具。
- `description`: `str` 类型，工具的详细描述。代理通过描述来判断何时应该使用此工具。

#### 返回值

返回一个 `Tool` 对象，可以直接添加到代理的工具列表中。

## 使用示例

```python
from langchain_classic.agents.agent_toolkits.conversational_retrieval.tool import create_retriever_tool

# 初始化一个检索器 (例如来自向量数据库)
retriever = vectorstore.as_retriever()

# 创建工具
search_tool = create_retriever_tool(
    retriever,
    "search_state_of_the_union",
    "搜索并返回有关国情咨文的信息。"
)

# 将工具传递给代理
# tools = [search_tool]
```

## 注意事项

- 工具的 `name` 应该是唯一的，且不应包含空格（虽然 LangChain 内部会进行一些处理，但建议遵循规范）。
- 工具的 `description` 对代理的决策至关重要，描述越清晰准确，代理使用该工具的效果就越好。
