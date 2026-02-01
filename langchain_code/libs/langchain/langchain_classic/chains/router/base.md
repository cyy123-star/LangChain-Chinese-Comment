# Router Chains

路由链（Router Chains）用于根据输入内容动态决定将其发送到多个目标链中的哪一个。这对于构建多功能助手非常有用，例如一个可以处理数学、编程和普通对话的机器人。

## 核心架构

路由逻辑主要由两个组件协同完成：

| 组件 | 类型 | 说明 |
| :--- | :--- | :--- |
| `RouterChain` | `Chain` | **决策者**。分析输入并输出目标链的名称（`destination`）和修改后的输入（`next_inputs`）。 |
| `MultiRouteChain` | `Chain` | **协调者**。包含一个 `RouterChain`、一组目标链（`destination_chains`）和一个默认链（`default_chain`）。 |

## 常见的 RouterChain 实现

1. **`LLMRouterChain`**: 使用 LLM 分析输入并决定路由。通常结合 `RouterOutputParser` 将 LLM 输出解析为 JSON。
2. **`EmbeddingRouterChain`**: 使用向量相似度进行路由。通过计算输入与各目标链描述的向量距离来选择最匹配的链。

## 执行逻辑

1. **路由决策**: `MultiRouteChain` 调用 `router_chain.route()`。
2. **参数准备**: `RouterChain` 返回一个 `Route` 对象（包含目标链名称和传递给它的参数）。
3. **分发执行**: 
   - 如果 `destination` 存在且在 `destination_chains` 中，则执行该目标链。
   - 如果不存在或匹配失败，则执行 `default_chain`。

```python
# 核心逻辑 (简化)
def _call(self, inputs: dict[str, Any]) -> dict[str, Any]:
    # 1. 决定去哪
    route = self.router_chain.route(inputs)
    
    # 2. 执行目标链
    if route.destination in self.destination_chains:
        return self.destination_chains[route.destination](route.next_inputs)
    
    # 3. 兜底处理
    return self.default_chain(route.next_inputs)
```

## 典型子类

- **`MultiPromptChain`**: 专门用于在多个 Prompt 模板之间切换。
- **`MultiRetrievalQAChain`**: 专门用于在多个不同的检索器（Retriever）之间切换（例如，针对不同主题的文档库）。

## 迁移建议 (LCEL)

在 LCEL 中，路由可以通过 `RunnableBranch` 或简单的函数逻辑更优雅地实现。

```python
from langchain_core.runnables import RunnableBranch

# 使用 RunnableBranch 实现路由
branch = RunnableBranch(
    (lambda x: "math" in x["topic"], math_chain),
    (lambda x: "code" in x["topic"], code_chain),
    general_chain,
)

full_chain = {"topic": classifier_chain, "question": lambda x: x["question"]} | branch
```

这种方式比 `RouterChain` 更透明，且更容易调试和组合。
