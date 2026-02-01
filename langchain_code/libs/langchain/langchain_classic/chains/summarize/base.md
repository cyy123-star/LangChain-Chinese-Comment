# Summarization Chains

`summarize` 模块提供了便捷的工厂函数，用于快速加载针对**摘要任务**优化的文档合并链（Combine Documents Chains）。

## 核心函数

通常通过 `load_summarize_chain` 函数来调用这些逻辑（该函数位于 `langchain.chains.summarize.__init__`）。

### 1. `stuff` 模式
- **函数**: `_load_stuff_chain`
- **逻辑**: 将所有文档内容拼接在一起，一次性交给 LLM 生成摘要。
- **适用场景**: 文档总量较小，不会超过 LLM 的上下文窗口。

### 2. `map_reduce` 模式
- **函数**: `_load_map_reduce_chain`
- **逻辑**: 
  1. **Map**: 分别对每个文档片段生成摘要。
  2. **Reduce**: 将所有片段摘要汇总，生成最终摘要。
- **适用场景**: 超长文档。

### 3. `refine` 模式
- **函数**: `_load_refine_chain`
- **逻辑**: 迭代式处理。先摘要第一个片段，然后将该摘要与第二个片段一起交给 LLM 生成更新后的摘要，以此类推。
- **适用场景**: 需要在摘要中保留更多细节，且不介意较慢的串行处理速度。

## 参数配置

| 参数 | 说明 |
| :--- | :--- |
| `llm` | 用于生成摘要的语言模型。 |
| `chain_type` | 字符串，可选 `"stuff"`, `"map_reduce"`, `"refine"`。 |
| `verbose` | 是否打印中间步骤。 |
| `map_prompt` | (仅限 map_reduce) 用于 map 阶段的自定义提示词。 |
| `combine_prompt` | (仅限 map_reduce) 用于 combine 阶段的自定义提示词。 |

## 示例代码

```python
from langchain_classic.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import ChatOpenAI

loader = WebBaseLoader("https://example.com")
docs = loader.load()

llm = ChatOpenAI(temperature=0)
chain = load_summarize_chain(llm, chain_type="map_reduce")
summary = chain.run(docs)
```

## 现代替代方案

建议参考 [LangGraph Map-Reduce 指南](https://langchain-ai.github.io/langgraph/how-tos/map-reduce/)。使用 LangGraph 可以更好地处理并行化、错误重试以及中间状态的持久化。
