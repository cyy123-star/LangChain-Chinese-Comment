# libs\langchain\langchain_classic\agents\openai_functions_multi_agent\base.py

此文档提供了 `libs\langchain\langchain_classic\agents\openai_functions_multi_agent\base.py` 文件的详细中文注释。该模块实现了一个能够一次性决定并执行多个动作（函数调用）的 OpenAI 代理。

## 核心功能

传统的代理通常每一轮只能执行一个工具调用。而 `OpenAIFunctionsMultiAgent` 利用 OpenAI 的函数调用能力，允许代理在单次模型响应中提出多个工具调用请求，从而提高效率。

## 核心逻辑：消息解析

该模块的核心在于 `_parse_ai_message` 函数，它负责将模型的原始输出解析为代理指令。

### 解析步骤
1. **类型检查**: 确保输入是 `AIMessage`。
2. **提取函数调用**: 检查消息的 `additional_kwargs` 中是否存在 `function_call`。
3. **处理多动作**:
   - 解析 `arguments` 字段中的 JSON 字符串。
   - 提取 `actions` 列表，其中包含了所有待执行的工具信息。
   - **特殊处理**: 处理旧版工具使用的 `__arg1` 参数包装。
4. **生成动作列表**: 将每个待执行项转换为 `AgentActionMessageLog`（内部别名为 `_FunctionsAgentAction`），并保留原始消息日志以便追溯。
5. **任务完成**: 如果没有函数调用，则返回 `AgentFinish`。

## 主要组件

### `OpenAIMultiFunctionsAgent`

这是该模块的核心类，继承自 `BaseMultiActionAgent`。它通过构造一个特殊的 `tool_selection` 函数模式，强制模型返回一个包含多个动作的列表。

#### 参数说明

| 参数 | 类型 | 说明 |
| :--- | :--- | :--- |
| `llm` | `BaseLanguageModel` | 必须是支持 `functions` 调用能力的 OpenAI 模型实例（如 `ChatOpenAI`）。 |
| `tools` | `Sequence[BaseTool]` | 代理可以使用的工具列表。 |
| `prompt` | `BasePromptTemplate` | 代理使用的提示词模板。必须包含 `agent_scratchpad` 变量。 |

#### 核心方法

- **`create_prompt`**: 类方法，用于创建适合此代理的提示词模板。
  - `system_message`: 可选，系统消息。默认为 "You are a helpful AI assistant."。
  - `extra_prompt_messages`: 可选，在系统消息和人类输入之间插入的额外消息。
- **`plan` / `aplan`**: 根据当前输入和中间步骤，决定下一步要执行的一个或多个动作。

## 核心逻辑：消息解析与单动作代理的区别

- **接口不同**: 继承自 `BaseMultiActionAgent` 而非 `BaseSingleActionAgent`。
- **返回类型**: 其 `plan` 方法返回的是 `List[AgentAction]` 而不是单个 `AgentAction`。
- **效率**: 适用于需要同时启动多个独立任务（如并行搜索、并行数据抓取）的场景。

## 注意事项

- **JSON 严格性**: 解析 JSON 时设置了 `strict=False`，以提高对模型微小格式错误的容忍度。
- **参数解包**: 内部逻辑会自动解包 `__arg1`，这保证了与 LangChain 早期定义的单参数工具的兼容性。
