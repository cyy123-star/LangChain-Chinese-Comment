# XML Agent

`XMLAgent` 是一种使用 XML 标签（如 `<tool>`、`<tool_input>`）来结构化其思考和行动过程的代理。这种格式特别适合那些对 XML 结构化数据处理较好的模型（如 Anthropic 的 Claude 系列）。

## 核心工作流

1. **Prompt**: 指示模型使用 XML 标签来调用工具。
2. **Execution**: 模型生成类似 `<tool>search</tool><tool_input>weather</tool_input>` 的内容。
3. **Parsing**: `XMLAgentOutputParser` 提取标签内容并转换为 `AgentAction`。
4. **Observation**: 工具结果被包装在 `<observation>` 标签中反馈给模型。

## 核心实现 (Verbatim Snippet)

### 1. 计划逻辑 (plan)
XML Agent 手动拼接中间步骤的 XML 字符串，而不是依赖通用的 Scratchpad 格式化函数。
```python
def plan(
    self,
    intermediate_steps: list[tuple[AgentAction, str]],
    callbacks: Callbacks = None,
    **kwargs: Any,
) -> AgentAction | AgentFinish:
    log = ""
    for action, observation in intermediate_steps:
        # 手动构建 XML 历史记录
        log += (
            f"<tool>{action.tool}</tool><tool_input>{action.tool_input}"
            f"</tool_input><observation>{observation}</observation>"
        )
    inputs = {
        "intermediate_steps": log,
        "tools": tools,
        "question": kwargs["input"],
        "stop": ["</tool_input>", "</final_answer>"],
    }
    response = self.llm_chain(inputs, callbacks=callbacks)
    return response[self.llm_chain.output_key]
```

## 迁移指南 (Migration)

现代 LangChain 推荐使用 `create_xml_agent` 工厂函数，或者直接使用原生支持 Tool Calling 的模型。

### 现代 XML Agent 创建
```python
from langchain.agents import create_xml_agent
from langchain_anthropic import ChatAnthropic

model = ChatAnthropic(model="claude-3-opus-20240229")
agent = create_xml_agent(model, tools, prompt)
```

**为什么迁移？**
1. **LCEL 支持**: `create_xml_agent` 返回的是一个 `Runnable` 对象，可以轻松与其他组件集成。
2. **异步支持**: 现代实现对异步 `aplan` 有更好的原生支持。
3. **鲁棒性**: 新的 `XMLAgentOutputParser` 在处理不完整的 XML 或格式微调方面更加健壮。
