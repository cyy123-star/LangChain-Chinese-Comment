# libs\langchain\langchain_classic\agents\format_scratchpad\xml.py

此文档提供了 `libs\langchain\langchain_classic\agents\format_scratchpad\xml.py` 文件的详细中文注释。该模块用于将代理的中间步骤格式化为 XML 标签序列。

## 核心函数：`format_xml`

该函数将代理执行的每一个步骤（Action + Observation）转化为 XML 格式的字符串，供模型（特别是 Claude）进行下一步推理。

### 1. 函数参数说明
- **`intermediate_steps`**: 代理执行的中间步骤列表。
- **`escape_format`**: 转义格式。默认为 `"minimal"`，会将 XML 标签替换为安全的占位符，以防止模型输出的内容干扰标签解析。

### 2. 工作原理
1. **标签转义**: 如果启用了 `minimal` 转义，函数会调用 `_escape` 将内容中的 `<tool>`, `</tool>` 等标签替换为 `[[tool]]`, `[[/tool]]` 等。
2. **标签构建**: 将工具名、输入参数和观测结果拼接成标准的 XML 结构：
   ```xml
   <tool>工具名</tool><tool_input>参数</tool_input><observation>结果</observation>
   ```
3. **日志累积**: 将所有步骤拼接成一个完整的字符串。

### 3. 输出示例
```xml
<tool>search</tool><tool_input>weather in Paris</tool_input><observation>20 degrees</observation>
```

## 内部辅助函数

- **`_escape`**: 核心转义函数。它能防止“注入攻击”——即如果工具输出的内容恰好包含 `<tool>` 等标签，它会将其替换为安全的自定义界定符（如 `[[tool]]`），确保解析器的稳定性。

## 注意事项

- **Claude 优化**: 这种格式化方式最适合那些经过 XML 指令微调的模型。
- **解析对称性**: 输出的 XML 格式必须与 `XMLAgentOutputParser` 预期的格式完全匹配。
- **安全性**: `escape_format` 是为了处理复杂的工具输出（如代码片段或包含 HTML 的内容）而设计的。
