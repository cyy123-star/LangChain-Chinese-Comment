# libs\langchain\langchain_classic\agents\react\agent.py

此文档提供了 `libs\langchain\langchain_classic\agents\react\agent.py` 文件的详细中文注释。该文件包含了创建基于 ReAct 提示策略的代理的现代工厂函数。

## 核心函数：`create_react_agent`

`create_react_agent` 是用于创建遵循 ReAct (Reasoning and Acting) 框架的代理的推荐方式（在 `langchain_classic` 范围内）。

### 函数签名

```python
def create_react_agent(
    llm: BaseLanguageModel,
    tools: Sequence[BaseTool],
    prompt: BasePromptTemplate,
    output_parser: AgentOutputParser | None = None,
    tools_renderer: ToolsRenderer = render_text_description,
    *,
    stop_sequence: bool | list[str] = True,
) -> Runnable
```

### 参数说明

- **`llm`**: 作为代理核心的语言模型。
- **`tools`**: 代理可以访问的工具列表。
- **`prompt`**: 使用的提示模板。必须包含特定的变量（见下文）。
- **`output_parser`**: 用于解析 LLM 输出的解析器。默认为 `ReActSingleInputOutputParser`。
- **`tools_renderer`**: 控制如何将工具列表转换为字符串并传递给 LLM。默认为 `render_text_description`。
- **`stop_sequence`**: 
    - 如果为 `True`（默认），则添加 `\nObservation:` 作为停止序列，以防止模型产生幻觉（自我模拟工具输出）。
    - 如果为 `False`，则不添加停止序列。
    - 也可以提供字符串列表作为自定义停止序列。

### 提示模板要求

传入的 `prompt` 必须包含以下输入变量：
- **`tools`**: 包含每个工具的描述和参数。
- **`tool_names`**: 包含所有工具的名称。
- **`agent_scratchpad`**: 包含代理之前的行动和工具输出的字符串记录。

### 代码实现细节

1. **变量校验**: 检查提示模板是否包含所有必需的变量。
2. **提示词预填充**: 使用 `tools_renderer` 处理工具信息，并将其预填充到提示模板中。
3. **模型绑定**: 如果启用了 `stop_sequence`，则将停止序列绑定到 LLM 实例。
4. **构造 Runnable 链**:
    - 使用 `RunnablePassthrough.assign` 将 `intermediate_steps` 格式化为 `agent_scratchpad`。
    - 将处理后的输入传递给 `prompt`。
    - 调用绑定了停止词的 `llm`。
    - 最后使用 `output_parser` 解析结果。

## 弃用警告

!!! warning "弃用说明"
    虽然 `create_react_agent` 是此模块中的现代实现，但对于生产环境，官方强烈建议迁移到 **LangGraph** 的 `create_react_agent` 实现，因为它更加稳健且功能丰富。

## 关联文件

- [__init__.py](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/react/__init__.md): 模块入口。
- [output_parser.py](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/react/output_parser.md): 默认的输出解析逻辑。
- [format_scratchpad](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/format_scratchpad/__init__.md): 提供 `format_log_to_str` 用于格式化思考过程。
