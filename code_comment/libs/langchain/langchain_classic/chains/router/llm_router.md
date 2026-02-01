# libs\langchain\langchain_classic\chains\router\llm_router.py

## 文件概述

`llm_router.py` 定义了基于大语言模型（LLM）的路由器实现。它使用 LLM 来解析输入并决定应该将请求路由到哪个目标。

## 核心类：LLMRouterChain (已弃用)

### 功能描述

`LLMRouterChain` 持有一个 `LLMChain`。它期望 LLM 返回一个结构化的响应（通常是 JSON），包含目标链名称和下一步的输入。

### 核心属性

| 属性名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `llm_chain` | `LLMChain` | 用于执行路由决策的底层 LLM 链。其 Prompt 必须配置有输出解析器。 |

### 核心逻辑

```python
def _call(
    self,
    inputs: dict[str, Any],
    run_manager: CallbackManagerForChainRun | None = None,
) -> dict[str, Any]:
    callbacks = run_manager.get_child() if run_manager else None
    
    # 1. 调用 LLM 进行预测
    prediction = self.llm_chain.predict(callbacks=callbacks, **inputs)
    
    # 2. 使用 Prompt 自带的解析器将文本转换为字典
    # 该字典应包含 "destination" 和 "next_inputs"
    return self.llm_chain.prompt.output_parser.parse(prediction)
```

## 辅助类：RouterOutputParser

### 功能描述

专门用于解析路由预测结果的解析器。它通常期望 LLM 输出一段包含 JSON 的 Markdown 代码块。

### 解析逻辑

1. 使用 `parse_and_check_json_markdown` 提取 JSON。
2. 检查是否包含 `destination` 和 `next_inputs` 键。
3. 处理默认路由逻辑：如果 `destination` 匹配 `default_destination`（通常是 "DEFAULT"），则将其设为 `None`。

## 迁移建议

该类已被弃用，建议使用 LCEL 的 `RunnableLambda` 或 `RunnableBranch` 实现。

### 现代替代示例 (LCEL)

```python
from operator import itemgetter
from langchain_core.runnables import RunnableLambda

# 定义路由逻辑
def route(info):
    if "python" in info["topic"].lower():
        return python_chain
    elif "js" in info["topic"].lower():
        return js_chain
    else:
        return default_chain

# 构建链
full_chain = {
    "topic": classification_chain, # 负责分类的链
    "question": itemgetter("question")
} | RunnableLambda(route)
```

## 注意事项

1. **Prompt 依赖**：`LLMRouterChain` 极度依赖于 Prompt 的编写质量和输出解析器的准确性。
2. **JSON 稳定性**：如果 LLM 输出的 JSON 格式不规范，会导致 `OutputParserException`。
3. **性能开销**：每次路由都会产生一次额外的 LLM 调用，对于简单逻辑，建议使用 `EmbeddingRouterChain` 或简单的关键词匹配。
