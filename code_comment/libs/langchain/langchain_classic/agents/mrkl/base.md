# libs\langchain\langchain_classic\agents\mrkl\base.py

此文档提供了 `libs\langchain\langchain_classic\agents\mrkl\base.py` 文件的详细中文注释。该文件包含了 MRKL 系统的核心实现，即 `ZeroShotAgent` 类。

## 弃用说明

⚠️ **重要提示**: `ZeroShotAgent` 和 `MRKLChain` 已被标记为弃用（从 v0.1.0 开始）。
- **建议迁移**: 请使用 [create_react_agent](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/react/agent.md) 配合 LCEL 构建方式。
- **原因**: 现代的 `create_react_agent` 提供了更好的扩展性、更清晰的逻辑流以及对不同模型更好的适配。

---

## 核心类：`ZeroShotAgent`

`ZeroShotAgent` 是一个基于 ReAct 框架的经典代理。它不需要为每个工具提供示例，而是通过分析工具的名称和描述来决定如何使用它们。

### 1. 主要属性

- `output_parser`: 默认使用 `MRKLOutputParser`。
- `observation_prefix`: 默认值为 `"Observation: "`。
- `llm_prefix`: 默认值为 `"Thought:"`。

### 2. 核心方法

#### `create_prompt`
创建一个符合 ReAct 格式的提示词模板。
- **逻辑**: 将 `PREFIX`（开头）、工具列表描述、`FORMAT_INSTRUCTIONS`（格式说明）和 `SUFFIX`（结尾）拼接在一起。
- **变量要求**: 提示词中必须包含 `{input}` 和 `{agent_scratchpad}`。

#### `from_llm_and_tools` (工厂方法)
这是初始化代理的最常用方法。
- **参数**:
    - `llm`: 语言模型。
    - `tools`: 工具列表（每个工具必须有明确的 `description`）。
    - `prefix/suffix/format_instructions`: 可选，用于覆盖默认提示词。
- **验证逻辑**: 该方法会调用 `_validate_tools` 确保所有工具都仅接受单一输入字符串（MRKL 代理的限制）。

## 辅助类：`MRKLChain` (已弃用)

它是 `AgentExecutor` 的子类，提供了一个快捷方式 `from_chains` 来初始化 MRKL 系统。它接受 `ChainConfig` 对象列表，每个配置包含动作名称、函数和描述。

## 技术细节

- **工具验证**: `ZeroShotAgent` 要求所有工具必须有描述，因为模型是靠描述来“学习”工具用途的。
- **提示词组装**: 该代理通过渲染工具列表并注入到提示词中，向模型展示当前可用的所有能力。
- **ReAct 循环**: 模型输出 `Thought`（思考）后，必须紧跟 `Action`（行动）和 `Action Input`（行动输入），否则 `MRKLOutputParser` 会抛出异常。

## 关联文件

- [output_parser.py](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/mrkl/output_parser.md): 负责处理模型生成的 ReAct 文本。
- [prompt.py](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/mrkl/prompt.md): 定义了默认的模板字符串。

