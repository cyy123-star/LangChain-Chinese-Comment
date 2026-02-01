# libs\langchain\langchain_classic\agents\structured_chat\output_parser.py

此文档提供了 `libs\langchain\langchain_classic\agents\structured_chat\output_parser.py` 文件的详细中文注释。该解析器专门设计用于处理结构化对话代理输出的 JSON 格式指令。

## 1. 核心类：`StructuredChatOutputParser`

这是基础解析器，负责从 LLM 输出的文本中提取并解析 JSON。

### 解析逻辑

1. **正则匹配**: 使用 `re.compile(r"```(?:json\s+)?(\W.*?)```", re.DOTALL)` 匹配 Markdown 中的代码块。
2. **JSON 加载**: 
   - 提取代码块内容并使用 `json.loads` 解析。
   - `strict=False` 允许解析包含控制字符（如换行符）的 JSON 字符串。
3. **多动作处理**: 
   - 如果模型返回了一个列表（某些模型即使被要求返回单个 Action 也会返回列表），解析器会记录警告并取列表中的第一个动作。
4. **动作映射**:
   - 如果 `action` 为 `"Final Answer"` -> 返回 `AgentFinish`。
   - 否则 -> 返回 `AgentAction`，其中 `action_input` 是一个包含多个参数的字典。
5. **回退逻辑**: 如果没有匹配到任何代码块，解析器会将整个输出视为 `Final Answer`。

---

## 2. 核心类：`StructuredChatOutputParserWithRetries`

这是一个包装类，增加了基于 LLM 的错误修复能力。

### 关键组件

- **`base_parser`**: 默认使用 `StructuredChatOutputParser`。
- **`output_fixing_parser`**: `OutputFixingParser` 的实例。

### 工作流程

1. 尝试使用 `base_parser` 直接解析。
2. 如果解析失败并抛出异常，且配置了 `output_fixing_parser`，则调用修复解析器。
3. 修复解析器会将错误信息和原始文本发送给另一个 LLM（或同一个 LLM），请求其生成正确的 JSON 格式。

---

## 3. 静态工厂方法：`from_llm`

提供了一种便捷方式来创建带重试功能的解析器。

```python
# 示例：创建一个带修复功能的解析器
parser = StructuredChatOutputParserWithRetries.from_llm(llm=chat_model)
```

## 技术细节

- **类型标识**: `_type` 分别为 `"structured_chat"` 和 `"structured_chat_with_retries"`。
- **异常处理**: 当解析彻底失败（即 LLM 无法输出可识别的代码块或修复失败）时，抛出 `OutputParserException`。

