# libs\langchain\langchain_classic\agents\mrkl\prompt.py

此文档提供了 `libs\langchain\langchain_classic\agents\mrkl\prompt.py` 文件的详细中文注释。该文件定义了 MRKL (ZeroShot) 代理使用的经典 ReAct 提示词模板。

## 文件概述

这些常量共同构成了引导 LLM 执行“推理-行动”循环的完整指令集。它们被设计为易于拼接和自定义。

## 核心常量

### 1. `PREFIX`
- **内容**: `"Answer the following questions as best you can. You have access to the following tools:"`
- **作用**: 设定任务目标，并引入接下来的工具列表。

### 2. `FORMAT_INSTRUCTIONS`
- **内容**: 详细规定了输出格式。
- **关键结构**:
    - **Question**: 用户输入。
    - **Thought**: 思考过程。
    - **Action**: 从给定的工具列表中选择。
    - **Action Input**: 工具的输入参数。
    - **Observation**: 工具执行结果（代理会自动填入）。
    - **Final Answer**: 最终答案。
- **作用**: 这是 ReAct 框架的灵魂，通过强格式约束引导模型进行结构化输出。

### 3. `SUFFIX`
- **内容**: `"Begin!\n\nQuestion: {input}\nThought:{agent_scratchpad}"`
- **作用**: 标志着指令结束，并启动任务。它注入了用户的实际问题 `{input}`，以及最重要的 `{agent_scratchpad}`（用于存放历史思考和工具观察结果）。

## 设计意图

- **少样本思维链的替代**: 虽然这里叫 ZeroShot（零样本），但 `FORMAT_INSTRUCTIONS` 本身就像是一个“格式模板”，它教会了模型一种推理协议，而不需要针对特定任务的大量示例。
- **递归推理**: 通过 `{agent_scratchpad}`，模型能够看到自己之前的思考和工具返回的结果，从而实现多步推理。
- **严格性**: 该提示词配合 `MRKLOutputParser` 使用，确保了 LLM 输出的可预测性。

## 注意事项

1. **多语言支持**: 默认常量为英文。如果需要构建中文代理，通常需要自定义这些常量为中文，以获得更好的效果。
2. **Scratchpad**: 确保自定义后缀时保留 `{agent_scratchpad}` 占位符，否则代理将失去记忆，陷入死循环。
3. **冒号格式**: `MRKLOutputParser` 依赖这些标签后面的冒号。如果修改这些标签，请确保解析器也能识别新的格式。

## 关联文件

- [base.py](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/mrkl/base.md): `ZeroShotAgent.create_prompt` 方法负责将这些片段组装成最终的 `PromptTemplate`。
- [output_parser.py](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/mrkl/output_parser.md): 负责解析符合此处 `FORMAT_INSTRUCTIONS` 的文本。

