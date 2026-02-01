# libs\langchain\langchain_classic\agents\output_parsers\xml.py

此文档提供了 `libs\langchain\langchain_classic\agents\output_parsers\xml.py` 文件的详细中文注释。该解析器用于从 XML 格式的输出中提取工具调用和最终回答。

## 1. 核心类：`XMLAgentOutputParser`

专门为 XML 风格代理（如针对 Claude 等擅长 XML 的模型）设计的解析器。

### 解析逻辑

1. **工具调用检测**:
   - 寻找 `<tool>...</tool>` 标签。
   - 提取工具名称。
   - 寻找可选的 `<tool_input>...</tool_input>` 标签，提取工具输入。
2. **最终回答检测**:
   - 如果没有工具标签，寻找 `<final_answer>...</final_answer>` 标签。
3. **反转义处理 (Unescaping)**:
   - 支持 `minimal` 转义格式。
   - 使用 `_unescape` 函数将自定义分隔符（如 `[[tool]]`）还原为 XML 标签（如 `<tool>`）。这可以防止工具输入中包含的 XML 标签干扰解析过程。
4. **严格校验**:
   - 必须有且仅有一个工具块或一个最终回答块。
   - 如果格式不符合 XML 预期（如多个标签），抛出 `ValueError`。

---

## 2. 辅助函数：`_unescape`

```python
def _unescape(text: str) -> str:
    # 将 [[tool]] 替换为 <tool>
    # 将 [[tool_input]] 替换为 <tool_input>
    # ...以此类推
```

## 期望的输出格式

### 场景 A：调用工具

```xml
<tool>search</tool>
<tool_input>LangChain documentation</tool_input>
```

### 场景 B：最终回答

```xml
<final_answer>LangChain is a framework for building LLM apps.</final_answer>
```

## 技术细节

- **转义支持**: 通过 `escape_format="minimal"` 处理嵌套 XML 的冲突问题。
- **正则实现**: 使用 `re.findall` 结合 `re.DOTALL` 跨行匹配标签内容。
- **类型标识**: `_type` 为 `"xml-agent"`。

## 关联组件

- [xml/base.py](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/xml/base.md): 该解析器是 XML 代理的核心组件。
