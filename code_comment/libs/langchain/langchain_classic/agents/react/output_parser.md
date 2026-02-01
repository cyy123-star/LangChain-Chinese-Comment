# libs\langchain\langchain_classic\agents\react\output_parser.py

此文档提供了 `libs\langchain\langchain_classic\agents\react\output_parser.py` 文件的详细中文注释。该解析器专门用于处理早期 ReAct 架构中常见的 `Action[input]` 格式。

## 核心类：`ReActOutputParser`

这是一个经典的输出解析器，用于将 LLM 生成的文本解析为代理行动 (`AgentAction`) 或最终结果 (`AgentFinish`)。

### 解析逻辑说明

该解析器期望 LLM 输出的最后一行遵循特定的格式：

1. **预期格式**: `Action: 工具名称[工具输入]`
2. **解析步骤**:
    - 检查文本是否以 `Action: ` 开头。
    - 使用正则表达式 `(.*?)\[(.*?)\]` 提取括号外的工具名称和括号内的输入内容。
    - 如果工具名称为 `Finish`，则返回 `AgentFinish`，其中包含最终答案。
    - 否则，返回 `AgentAction`。

### 代码实现示例

```python
def parse(self, text: str) -> AgentAction | AgentFinish:
    action_prefix = "Action: "
    # 获取最后一行
    action_block = text.strip().split("\n")[-1]
    
    # 提取内容并正则匹配
    action_str = action_block[len(action_prefix) :]
    re_matches = re.search(r"(.*?)\[(.*?)\]", action_str)
    
    # 返回对应的对象
    ...
```

### 限制与异常

- **异常处理**: 如果最后一行不以 `Action: ` 开头，或者正则表达式匹配失败，会抛出 `OutputParserException`。
- **单输入局限**: 该解析器仅支持提取单个括号内的内容作为工具输入。

## 与现代解析器的区别

虽然此解析器在 `ReActDocstoreAgent` 中被广泛使用，但现代的 `create_react_agent` 默认使用的是 `ReActSingleInputOutputParser` (位于 `langchain_classic.agents.output_parsers`)。

- **旧版 (`ReActOutputParser`)**: 期望 `Action: Name[Input]`。
- **现代版 (`ReActSingleInputOutputParser`)**: 期望更通用的多行格式：
  ```text
  Action: name
  Action Input: input
  ```

## 关联文件

- [base.py](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/react/base.md): 使用此解析器的早期代理实现。
- [agent.py](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/react/agent.md): 现代 ReAct 代理工厂函数。
