# libs\langchain\langchain_classic\agents\openai_functions_agent\base.py

此文档提供了 `libs\langchain\langchain_classic\agents\openai_functions_agent\base.py` 文件的详细中文注释。该模块实现了基于 OpenAI Function Calling 能力的代理，这是处理工具调用最可靠、最高效的方式之一。

## 主要组件

### `OpenAIFunctionsAgent`

这是基于 OpenAI 函数调用逻辑的核心代理类，继承自 `BaseSingleActionAgent`。

#### 参数说明

| 参数 | 类型 | 说明 |
| :--- | :--- | :--- |
| `llm` | `BaseLanguageModel` | 必须是支持 `functions` 调用能力的 OpenAI 模型实例（如 `ChatOpenAI`）。 |
| `tools` | `Sequence[BaseTool]` | 代理可以使用的工具列表。 |
| `prompt` | `BasePromptTemplate` | 代理使用的提示词模板。必须包含 `agent_scratchpad` 变量。 |
| `output_parser` | `type[OpenAIFunctionsAgentOutputParser]` | 输出解析器，默认为 `OpenAIFunctionsAgentOutputParser`。 |

#### 核心方法

- **`create_prompt`**: 类方法，用于快速构建适配该代理的提示词模板。
  - `system_message`: 可选，系统消息。默认为 "You are a helpful AI assistant."。
  - `extra_prompt_messages`: 可选，在系统消息和人类输入之间插入的额外消息。
- **`from_llm_and_tools`**: 类方法，通过 LLM 和工具列表直接构造代理实例。
- **`plan` / `aplan`**: 根据当前输入和中间步骤，决定下一步要执行的一个动作。

### `create_openai_functions_agent`

这是一个工厂函数，用于创建符合 LCEL（LangChain Expression Language）标准的 OpenAI 函数调用代理。它是目前推荐的创建方式。

#### 参数说明

| 参数 | 类型 | 说明 |
| :--- | :--- | :--- |
| `llm` | `BaseLanguageModel` | 支持 OpenAI 函数调用的语言模型。 |
| `tools` | `Sequence[BaseTool]` | 工具列表。 |
| `prompt` | `ChatPromptTemplate` | 提示词模板，应包含 `agent_scratchpad`。 |

## 核心逻辑

## 注意事项

1. **弃用说明**: 该类自 0.1.0 版本起已被弃用。
2. **现代替代方案**: 
   - 官方强烈建议迁移到 `create_openai_functions_agent` 函数（用于 LCEL 构建）。
   - 更进一步，推荐使用更通用的 `create_tool_calling_agent`，它支持 OpenAI 的新版 Tool Calling API（`tools` 参数替代了旧的 `functions` 参数）。
3. **模型兼容性**: 仅适用于支持 OpenAI Function Calling 协议的模型。
