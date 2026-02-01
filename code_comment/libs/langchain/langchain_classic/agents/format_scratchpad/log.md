# libs\langchain\langchain_classic\agents\format_scratchpad\log.py

此文档提供了 `libs\langchain\langchain_classic\agents\format_scratchpad\log.py` 文件的详细中文注释。该模块用于将代理的中间步骤（Intermediate Steps）格式化为纯字符串。

## 核心函数：`format_log_to_str`

这是最基础的草稿纸（Scratchpad）格式化函数，通常用于基于文本的代理（如 `ZeroShotAgent` 或 `ReActAgent`）。

### 1. 函数参数说明
- **`intermediate_steps`**: 代理执行过程中的中间步骤列表，每个元素是一个二元组 `(AgentAction, Observation)`。
- **`observation_prefix`**: 观测结果的前缀。默认为 `"Observation: "`。
- **`llm_prefix`**: 下一次 LLM 调用（通常是 Thought）的前缀。默认为 `"Thought: "`。

### 2. 工作原理
该函数通过遍历 `intermediate_steps`，将每个动作的日志（`action.log`）与对应的观测结果（`observation`）拼接在一起：
1. 追加 `action.log`（包含模型之前的思考和行动指令）。
2. 换行并追加 `observation_prefix` 和实际的工具输出。
3. 换行并追加 `llm_prefix`，引导模型开始下一轮思考。

### 3. 输出示例
```text
Thought: I need to search for the weather.
Action: Search
Action Input: Weather in London
Observation: 15 degrees and cloudy.
Thought: 
```

## 注意事项

- **纯文本模型**: 该函数仅适用于非聊天模型（LLMs），因为它输出的是一个长字符串，而不是消息序列。
- **ReAct 风格**: 这种格式化方式是 ReAct (Reason + Act) 模式的核心，通过不断将先前的思考和结果喂回模型，让模型能够保持上下文。
