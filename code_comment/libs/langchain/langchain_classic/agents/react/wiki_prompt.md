# libs\langchain\langchain_classic\agents\react\wiki_prompt.py

此文档提供了 `libs\langchain\langchain_classic\agents\react\wiki_prompt.py` 文件的详细中文注释。这是 ReAct 论文中最经典的提示模板实现，用于解决多步搜索和推理问题。

## 核心组件：`WIKI_PROMPT`

`WIKI_PROMPT` 是一个 Few-shot `PromptTemplate`，它训练模型如何利用维基百科搜索工具（Search 和 Lookup）来回答复杂问题。

### 核心设计思想

该提示词体现了 ReAct 的精髓：
- **Reasoning (Thought)**: 模型在每一步都会解释它为什么要执行接下来的搜索或查找。
- **Acting (Action)**: 
    - `Search[词条]`: 在文档库中查找新主题。
    - `Lookup[关键词]`: 在当前文档中查找特定信息。
    - `Finish[答案]`: 给出最终结论。

### 内置示例

文件中包含了 6 个精心设计的 Few-shot 示例，涵盖了多种推理模式：
1. **多级跳转**: 搜索 A 得到 B，再根据 B 搜索 C（如：科罗拉多造山运动）。
2. **消歧与修正**: 当第一次搜索结果不匹配时，调整搜索词（如：High Plains）。
3. **比较与判断**: 搜索两个不同的事物并对比（如：电影导演的共同职业）。
4. **属性查找**: 在文档内部查找特定细节（如：人名由来）。

### 模板变量

- **`input`**: 用户提出的问题。
- **`agent_scratchpad`**: 包含之前所有 Thought、Action 和 Observation 的执行日志。

## 使用场景

此提示词是 [ReActDocstoreAgent](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/react/base.md) 的默认配置。它是研究和演示代理如何进行“自我纠错”和“逻辑链条推理”的绝佳案例。

## 关联文件

- [base.py](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/react/base.md): 定义了核心的 ReAct 代理。
- [output_parser.py](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/react/output_parser.md): 解析此提示词生成的 `Action[...]` 格式。
