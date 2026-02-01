# libs\langchain\langchain_classic\agents\structured_chat\prompt.py

此文档提供了 `libs\langchain\langchain_classic\agents\structured_chat\prompt.py` 文件的详细中文注释。该文件定义了结构化对话代理使用的标准提示词模板。

## 1. 核心常量：`PREFIX`

定义了系统的核心背景。

- **内容**: 引导模型尽可能提供帮助，并说明其可以访问的一系列工具。
- **作用**: 设定代理的角色和能力范围。

---

## 2. 核心常量：`FORMAT_INSTRUCTIONS`

这是该代理最重要的部分，定义了模型如何使用工具。

### 指令要求

1. **JSON 块格式**: 模型必须通过一个 JSON 块来指定动作，包含 `action` 和 `action_input` 两个键。
2. **多参数支持**: `action_input` 不再是一个简单的字符串，而是一个对象，其内容必须符合工具定义的参数 Schema。
3. **固定格式**:
   - `Question`: 输入问题。
   - `Thought`: 思考过程。
   - `Action`:
     ```
     $JSON_BLOB
     ```
   - `Observation`: 动作结果。
4. **Final Answer**: 当模型知道答案时，必须返回 `action: "Final Answer"`。

---

## 3. 核心常量：`SUFFIX`

定义了对话的收尾和提醒。

- **内容**: 提醒模型始终以 JSON 块形式响应，并提示“开始！”。
- **作用**: 确保模型在每一轮对话中都遵循格式约束。

## 设计意图

结构化对话代理的提示词设计的关键在于 **严格的格式约束** 和 **Schema 注入**。通过在 `FORMAT_INSTRUCTIONS` 中明确指定 JSON 格式，并结合 `base.py` 中注入的工具详细参数定义，它使得模型能够处理极其复杂的任务流。

## 关联组件

- [base.py](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/langchain/langchain_classic/agents/structured_chat/base.md): 在创建提示词时，会将 `PREFIX`、工具列表、`FORMAT_INSTRUCTIONS` 和 `SUFFIX` 拼接在一起。

