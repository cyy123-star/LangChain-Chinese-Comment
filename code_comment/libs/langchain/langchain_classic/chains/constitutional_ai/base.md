# libs\langchain\langchain_classic\chains\constitutional_ai\base.py

## 文件概述

`base.py` 实现了 `ConstitutionalChain`，这是一种基于“宪法 AI（Constitutional AI）”理念的链。它通过预定义的原则（Principles）对另一个链的输出进行自我监督、自我批评（Critique）和自我修正（Revision），以确保输出符合安全、伦理或特定的风格要求。

## 核心类：ConstitutionalChain (已弃用)

`ConstitutionalChain` 封装了原始链，并在其输出后增加了一个循环处理流程，根据一组“宪法原则”进行迭代优化。

### 核心属性

| 属性名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `chain` | `LLMChain` | 产生初始回答的原始链。 |
| `constitutional_principles` | `list[ConstitutionalPrinciple]` | 宪法原则列表。每个原则包含“批评请求”和“修正请求”。 |
| `critique_chain` | `LLMChain` | 负责根据原则对初始回答提出批评意见的链。 |
| `revision_chain` | `LLMChain` | 负责根据批评意见对初始回答进行修正的链。 |
| `return_intermediate_steps` | `bool` | 是否返回中间的批评和修正过程。 |

### 执行逻辑 (`_call` 方法)

`ConstitutionalChain` 的工作流程如下：

1.  **初始生成**: 运行原始 `chain` 获取初始响应（`initial_response`）。
2.  **迭代原则**: 遍历 `constitutional_principles` 中的每一个原则：
    - **批评 (Critique)**: `critique_chain` 分析当前响应是否违反该原则。
    - **判断**: 如果批评结果包含“无需批评（No critique needed）”，则跳过该原则。
    - **修正 (Revision)**: 如果存在违反，`revision_chain` 根据批评意见对响应进行修改。
3.  **最终输出**: 返回经过所有原则过滤和修正后的最终响应。

### 源码片段：核心循环

```python
for constitutional_principle in self.constitutional_principles:
    # 1. 执行批评
    raw_critique = self.critique_chain.run(
        input_prompt=input_prompt,
        output_from_model=response,
        critique_request=constitutional_principle.critique_request,
    )
    # 2. 解析与判断
    critique = self._parse_critique(output_string=raw_critique).strip()
    if "no critique needed" in critique.lower():
        continue
    # 3. 执行修正
    revision = self.revision_chain.run(
        input_prompt=input_prompt,
        output_from_model=response,
        critique_request=constitutional_principle.critique_request,
        critique=critique,
        revision_request=constitutional_principle.revision_request,
    ).strip()
    response = revision # 更新当前响应
```

## 静态方法：from_llm

便捷的工厂方法，用于快速构建宪法链：

```python
constitutional_chain = ConstitutionalChain.from_llm(
    llm=model,
    chain=qa_chain,
    constitutional_principles=[
        ConstitutionalPrinciple(
            name="Ethical Principle",
            critique_request="指出回答中任何不道德或带有偏见的内容。",
            revision_request="重写回答以消除偏见并确保符合道德规范。"
        )
    ],
)
```

## 迁移建议

该类已被弃用，建议迁移到 **LangGraph** 实现。LangGraph 版本可以使用结构化输出（Structured Output）来替代字符串解析（`_parse_critique`），从而获得更稳定的控制流和更好的流式输出支持。
