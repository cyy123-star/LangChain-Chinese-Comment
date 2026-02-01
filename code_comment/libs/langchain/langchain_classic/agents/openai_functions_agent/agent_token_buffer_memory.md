# libs\langchain\langchain_classic\agents\openai_functions_agent\agent_token_buffer_memory.py

此文档提供了 `libs\langchain\langchain_classic\agents\openai_functions_agent\agent_token_buffer_memory.py` 文件的详细中文注释。该模块实现了一种特殊的内存管理机制，专门用于保存代理的输出以及中间执行步骤。

## 核心类：`AgentTokenBufferMemory`

`AgentTokenBufferMemory` 继承自 `BaseChatMemory`，它的独特之处在于它不仅记录用户的输入和代理的最终回答，还记录了代理在推理过程中产生的所有中间步骤（Intermediate Steps）。

### 参数说明

| 参数 | 类型 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- |
| `llm` | `BaseLanguageModel` | - | 必填。用于计算 Token 数量的语言模型实例。 |
| `max_token_limit` | `int` | `12000` | 缓冲区允许的最大 Token 数量。超过此限制将弹出最早的消息。 |
| `memory_key` | `str` | `"history"` | 在返回字典中存储历史记录的键名。 |
| `intermediate_steps_key` | `str` | `"intermediate_steps"` | 输入/输出字典中存储中间步骤的键名。 |
| `format_as_tools` | `bool` | `False` | 是否将中间步骤格式化为工具消息（Tool Messages）。如果为 `False`，则格式化为 OpenAI 函数调用消息。 |
| `human_prefix` | `str` | `"Human"` | 人类消息的前缀。 |
| `ai_prefix` | `str` | `"AI"` | AI 消息的前缀。 |
| `return_messages` | `bool` | `True` | 是否以消息列表形式返回历史记录。 |

### 2. 核心逻辑：`save_context`
该方法负责将一轮对话及其推理过程存入内存。
1. **保存用户输入**: 将输入字符串转换为消息并存入缓冲区。
2. **格式化中间步骤**:
   - 根据 `format_as_tools` 标志，选择调用 `format_to_tool_messages` 或 `format_to_openai_function_messages`。
   - 将代理在这一轮中执行的所有工具调用和观察结果（Observation）转换为对应的消息序列。
3. **保存代理输出**: 将最终答案存入缓冲区。
4. **Token 裁剪 (Pruning)**:
   - 调用 `llm.get_num_tokens_from_messages` 计算当前所有消息的总 Token 数。
   - 如果超过 `max_token_limit`，则不断从缓冲区头部弹出（Pop）最早的消息，直到 Token 总数在限制范围内。

## 使用场景

- **长对话管理**: 适用于需要代理记住之前推理过程但又担心上下文窗口溢出的场景。
- **OpenAI 函数/工具调用**: 专门针对 OpenAI 的协议设计，能够完美还原之前的工具调用序列。

## 注意事项

- **Token 计算开销**: 每次保存上下文时都会调用 LLM 的 Token 计算接口，可能会产生轻微的延迟。
- **消息丢失**: 由于采取了从头部弹出的裁剪策略，最早的对话上下文会在达到限制后丢失。
