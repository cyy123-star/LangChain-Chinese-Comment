# libs\langchain\langchain_classic\agents\self_ask_with_search\prompt.py

此文档提供了 `libs\langchain\langchain_classic\agents\self_ask_with_search\prompt.py` 文件的详细中文注释。该文件定义了 Self-Ask 代理默认使用的少样本（Few-shot）提示词模板。

## 1. 核心常量：`PROMPT`

这是一个 `PromptTemplate` 实例，包含了一系列引导模型进行自我提问的示例。

### 模板结构

1. **Few-shot 示例**: 提供了四个具有代表性的问题拆解示例，涵盖了：
   - 年龄对比（Muhammad Ali vs Alan Turing）
   - 创始人信息（Craigslist）
   - 家族关系（George Washington 的外祖父）
   - 跨领域对比（Jaws 与 Casino Royale 的导演国籍）
2. **格式规范**: 每个示例都遵循统一的格式：
   - `Question`: 原始复杂问题。
   - `Are follow up questions needed here`: 总是以 `Yes.` 开头以激活推理。
   - `Follow up`: 子问题。
   - `Intermediate answer`: 工具返回的搜索结果（占位符）。
   - `So the final answer is`: 最终结论。
3. **输入占位符**:
   - `{input}`: 用户输入的问题。
   - `{agent_scratchpad}`: 代理的执行日志（包括中间的 Follow up 和 Intermediate answer）。

---

## 2. 交互示例 (模板末尾)

```text
Question: {input}
Are followup questions needed here:{agent_scratchpad}
```

## 技术细节

- **变量依赖**: 必须提供 `input` 和 `agent_scratchpad` 两个变量。
- **强制引导**: 模板末尾的 `Are followup questions needed here:` 后面紧跟 `{agent_scratchpad}`，这种设计强制 LLM 模仿前文的示例进行后续推理。

## 关联组件

- [base.py](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/self_ask_with_search/base.md): 该模板通过 `SelfAskWithSearchAgent.create_prompt` 被加载。
