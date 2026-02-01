# libs\langchain\langchain_classic\agents\self_ask_with_search\base.py

此文档提供了 `libs\langchain\langchain_classic\agents\self_ask_with_search\base.py` 文件的详细中文注释。该模块实现了 Self-Ask 策略，即代理通过自我提问并调用搜索工具来逐步解答复杂问题。

## 1. 核心类：`SelfAskWithSearchAgent` (已弃用)

这是基于 `Agent` 基类实现的 Self-Ask 代理类。

### 核心特性

- **工具限制**: 必须且只能提供一个工具，且该工具的名称必须为 `"Intermediate Answer"`。
- **输出解析**: 默认使用 `SelfAskOutputParser`。
- **前缀定义**:
  - `observation_prefix`: `"Intermediate answer: "`，用于将工具返回的观察结果拼接到提示词中。
  - `llm_prefix`: 为空。
- **提示词**: 使用预定义的 `PROMPT`，它不依赖于工具列表，因为逻辑是硬编码的。

---

## 2. 核心类：`SelfAskWithSearchChain` (已弃用)

这是一个便捷的 `AgentExecutor` 封装类，专门用于 Self-Ask。

- **初始化**: 接收一个 LLM 和一个搜索工具包装器（如 `GoogleSerperAPIWrapper`）。
- **自动化**: 自动将搜索包装器封装为名为 `"Intermediate Answer"` 的工具，并初始化代理。

---

## 3. 核心函数：`create_self_ask_with_search_agent`

这是推荐的现代创建方法，返回一个 `Runnable` 对象（LCEL）。

### 参数说明

| 参数 | 类型 | 说明 |
| :--- | :--- | :--- |
| `llm` | `BaseLanguageModel` | 使用的语言模型，会被绑定 `stop=["\nIntermediate answer:"]` 以防模型过度生成。 |
| `tools` | `Sequence[BaseTool]` | 必须包含且仅包含一个名为 `"Intermediate Answer"` 的工具。 |
| `prompt` | `BasePromptTemplate` | 必须包含 `agent_scratchpad` 变量。 |

### 工作流 (LCEL)

1. **变量分配**:
   - 将 `intermediate_steps` 格式化为字符串并赋值给 `agent_scratchpad`。
   - 默认初始化 `chat_history`。
2. **提示词填充**: 将变量填入 `prompt`。
3. **模型执行**: 调用 LLM。
4. **输出解析**: 使用 `SelfAskOutputParser` 将模型输出解析为动作或完成信号。

## 关联组件

- [output_parser.py](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/self_ask_with_search/output_parser.md): 指向通用的 Self-Ask 解析逻辑。
- [prompt.py](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/self_ask_with_search/prompt.md): 包含默认的少样本（Few-shot）提示词模板。

## 迁移指南

- **现代方案**: 建议使用 `create_self_ask_with_search_agent` 函数配合 LCEL。
- **提示词**: 推荐从 `langchain-hub` 拉取最新的 `hwchase17/self-ask-with-search`。
