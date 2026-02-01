# libs\langchain\langchain_classic\agents\output_parsers\self_ask.py

此文档提供了 `libs\langchain\langchain_classic\agents\output_parsers\self_ask.py` 文件的详细中文注释。该解析器专门用于 Self-Ask（自我提问）策略，通过将复杂问题拆解为多个子问题来逐步求解。

## 1. 核心类：`SelfAskOutputParser`

该解析器通过识别特定的关键词来区分模型是在提问（Follow up）还是在总结答案（Final Answer）。

### 解析逻辑

1. **关键词定义**:
   - `followups`: 支持 `"Follow up:"` 或 `"Followup:"` 作为子问题的引导词。
   - `finish_string`: 默认为 `"So the final answer is: "`。
2. **状态判定**:
   - 解析器主要观察输出的 **最后一行**。
   - **子问题判定**: 如果最后一行包含任何一个 `followups` 关键词 -> 返回 `AgentAction`。工具名统一设为 `"Intermediate Answer"`，输入为冒号后的内容。
   - **最终答案判定**: 如果最后一行不含 `followups` 但包含 `finish_string` -> 返回 `AgentFinish`，提取 `finish_string` 之后的内容作为输出。
3. **错误处理**: 如果最后一行既不符合子问题格式，也不符合最终答案格式，抛出 `OutputParserException`。

---

## 2. 期望的输出格式

### 场景 A：拆解子问题

```text
Who is the president of the country where the Eiffel Tower is located?
Follow up: In which country is the Eiffel Tower located?
```

### 场景 B：得出最终结论

```text
The Eiffel Tower is in France. The president of France is Emmanuel Macron.
So the final answer is: Emmanuel Macron
```

## 技术细节

- **工具约定**: 在 Self-Ask 架构中，通常只有一个搜索工具，解析器将所有动作硬编码为 `"Intermediate Answer"`，这意味着代理逻辑必须知道如何处理这个特定的“动作”。
- **单行局限**: 由于解析器依赖最后一行，模型生成的 Thoughts（思考过程）必须在关键词之前完成换行。
- **类型标识**: `_type` 为 `"self_ask"`。

## 关联组件

- [self_ask_with_search/base.py](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/self_ask_with_search/base.md): 该解析器是 Self-Ask 代理的核心驱动。
