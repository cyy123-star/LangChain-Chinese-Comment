# libs\langchain\langchain_classic\agents\react\textworld_prompt.py

此文档提供了 `libs\langchain\langchain_classic\agents\react\textworld_prompt.py` 文件的详细中文注释。该文件定义了用于文本冒险游戏（TextWorld）的 ReAct 提示模板。

## 核心组件：`TEXTWORLD_PROMPT`

`TEXTWORLD_PROMPT` 是一个预定义的 `PromptTemplate`，它采用了 Few-Shot（少样本）学习方式，引导 LLM 如何在文本游戏中通过“思考-行动”循环来解决任务。

### 提示词结构

1. **Setup**: 描述游戏的初始状态和任务目标。
2. **Thought**: 模型的思考过程（例如：“我需要向东走”）。
3. **Action**: 模型的行动指令，格式为 `Play[动作指令]`。
4. **Observation**: 游戏环境的反馈结果。
5. **Finish**: 任务完成时的特殊行动。

### 示例内容 (Few-shot)

文档中包含了一个典型的游戏流程示例：
- 任务：移动、获取物品、放置物品。
- 展示了如何处理环境反馈（Observation）并据此更新下一步的思考（Thought）。

### 模板变量

- **`input`**: 游戏的初始设置或当前状态。
- **`agent_scratchpad`**: 代理之前的思考和行动记录。

## 使用场景

此提示词专门配合 [ReActTextWorldAgent](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/react/base.md) 使用。它展示了 ReAct 框架如何应用于具有复杂状态和交互的交互式小说/游戏环境。

## 关联文件

- [base.py](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/react/base.md): 定义了使用此提示词的代理类。
