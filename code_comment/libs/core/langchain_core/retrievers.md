# retrievers.py

- **最后更新时间**: 2026-01-29
- **对应源码版本**: LangChain Core v1.2.7

## 文件概述
`retrievers.py` 定义了 LangChain 中检索器（Retriever）的抽象基类 `BaseRetriever`。检索器是一种能够根据文本查询返回相关文档（`Document`）的系统。它比向量数据库（Vector Store）更通用，因为检索器不一定需要存储文档，只需具备检索能力即可。

## 导入依赖
| 模块 | 作用 |
| :--- | :--- |
| `langchain_core.documents.Document` | 检索返回的核心数据对象。 |
| `langchain_core.runnables.RunnableSerializable` | 检索器继承自此，使其具备 LCEL 链式调用能力。 |
| `langchain_core.callbacks.manager` | 用于追踪和监控检索过程的回调管理。 |

## 类与函数详解

### 1. BaseRetriever (抽象基类)
- **功能描述**: 所有检索器的基类。它将复杂的检索逻辑封装在一个标准的 `Runnable` 接口中，支持 `invoke`, `ainvoke`, `batch` 等方法。
- **核心方法**:
  - **_get_relevant_documents(query, run_manager)**: **抽象方法**。子类必须实现此方法来定义同步检索逻辑。
  - **_aget_relevant_documents(query, run_manager)**: **可选方法**。子类可以重写此方法以提供原生异步支持，默认在线程池中运行同步方法。
  - **invoke(input, config, **kwargs)**: 同步调用入口，负责处理回调、元数据和检索逻辑。
  - **ainvoke(input, config, **kwargs)**: 异步调用入口。

#### 核心属性:
- **tags**: `list[str]` - 关联的标签，用于追踪和过滤。
- **metadata**: `dict[str, Any]` - 关联的元数据，用于记录额外信息。

## 使用示例
### 自定义检索器实现
```python
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever

class MySimpleRetriever(BaseRetriever):
    def _get_relevant_documents(self, query: str, *, run_manager):
        # 自定义检索逻辑
        return [Document(page_content=f"Result for {query}")]

retriever = MySimpleRetriever()
docs = retriever.invoke("hello")
```

## 注意事项
- **接口一致性**: 检索器应始终通过 `invoke` 或 `ainvoke` 调用，而不是直接调用私有的 `_get_relevant_documents`。
- **与向量库的区别**: 向量库通常作为检索器的后端实现，但检索器也可以是基于 API、SQL 或 Web 搜索的。

## 相关链接
- [langchain_core.runnables](file:///d%3A/TraeProjects/langchain_code_comment/code_comment/libs/core/langchain_core/runnables/base.md)
- [langchain_core.documents](file:///d%3A/TraeProjects/langchain_code_comment/code_comment/libs/core/langchain_core/documents/base.md)
