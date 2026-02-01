# ConstitutionalChain (Deprecated)

`ConstitutionalChain` 用于根据一系列“原则”（宪法）对 LLM 的输出进行自我审查和修改。它通常用于确保输出符合道德、法律或特定的风格指南。

> **警告**: 该类自 v0.2.13 起已弃用，建议使用 [LangGraph](https://langchain-ai.github.io/langgraph/) 实现更灵活的审查循环。

## 核心组件

| 参数 | 类型 | 说明 |
| :--- | :--- | :--- |
| `chain` | `LLMChain` | 产生初始回答的基础链。 |
| `constitutional_principles` | `List[ConstitutionalPrinciple]` | 包含 `critique_request`（审查请求）和 `revision_request`（修改请求）的原则列表。 |
| `critique_chain` | `LLMChain` | 用于执行审查逻辑的链。 |
| `revision_chain` | `LLMChain` | 用于根据审查结果执行修改逻辑的链。 |

## 执行逻辑

`ConstitutionalChain` 采用迭代式的工作流：

1. **初始生成**: 调用 `chain` 生成初始回答。
2. **循环审查**: 遍历每个 `ConstitutionalPrinciple`：
   - **审查 (Critique)**: `critique_chain` 评估当前回答是否违反了原则。
   - **判断**: 如果审查结果包含 "no critique needed"，则跳过该原则。
   - **修改 (Revision)**: `revision_chain` 根据审查意见修改当前回答。
3. **最终输出**: 返回经过所有原则过滤和修改后的最终回答。

```python
# 核心循环逻辑 (简化)
for principle in self.constitutional_principles:
    # 1. 审查
    critique = self.critique_chain.run(
        input_prompt=input_prompt,
        output_from_model=response,
        critique_request=principle.critique_request
    )
    
    if "no critique needed" in critique.lower():
        continue
        
    # 2. 修改
    revision = self.revision_chain.run(
        input_prompt=input_prompt,
        output_from_model=response,
        critique_request=principle.critique_request,
        critique=critique,
        revision_request=principle.revision_request
    )
    response = revision
```

## 预定义原则

LangChain 在 `principles.py` 中内置了一些常用原则，可以通过 `ConstitutionalChain.get_principles()` 获取。

| 名称 | 说明 |
| :--- | :--- |
| `harmful-content` | 识别并拒绝生成有害、非法或暴力内容。 |
| `pii` | 识别并移除个人身份信息 (PII)。 |
| `ethical` | 确保回答符合基本的伦理标准。 |

## 迁移方案 (LangGraph)

LangGraph 版本可以通过 `with_structured_output` 更精确地控制审查逻辑，避免字符串解析的不可靠性。

```python
# 推荐使用 LangGraph 实现，支持更复杂的条件分支和状态管理
# 示例参考 constitutional_ai/base.py 中的 docstring 示例
```
