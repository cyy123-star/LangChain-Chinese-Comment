# libs\langchain\langchain_classic\chains\summarize\chain.py

## 文件概述

`chain.py` 包含了 `load_summarize_chain` 工厂方法，它是经典 LangChain 中用于创建“摘要（Summarization）”相关文档组合链的核心入口。

## 核心方法：load_summarize_chain

该方法是一个工厂函数，支持三种主要的摘要策略。

### 参数说明

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `llm` | `BaseLanguageModel` | 链中使用的语言模型。 |
| `chain_type` | `str` | 策略类型，可选："stuff", "map_reduce", "refine"。 |
| `verbose` | `bool` | 是否开启详细日志。 |
| `**kwargs` | `Any` | 额外参数，如自定义 Prompt。 |

### 策略详解

#### 1. Stuff (填充式)
- **逻辑**：将所有待摘要文本直接拼接到一个 Prompt 中，让 LLM 生成摘要。
- **默认变量名**：`text` (在 Prompt 中占位符为 `{text}`)。
- **适用场景**：文本总量较短。

#### 2. Map-Reduce (映射-规约)
- **逻辑**：
    1. **Map**: 分别对每个分段（文档）生成中间摘要。
    2. **Reduce**: 将所有中间摘要合并成最终的大摘要。
- **参数控制**：`token_max` 决定了何时触发中间合并（Collapse）步骤。
- **适用场景**：超长文本摘要。

#### 3. Refine (迭代改进)
- **逻辑**：
    1. 对第一个分段生成初始摘要。
    2. 对后续每个分段，将“当前分段内容”和“已生成的摘要”一起交给 LLM 进行迭代更新。
- **适用场景**：需要保留跨分段的连续细节，或希望摘要逐步演进。

## 迁移建议 (LCEL)

虽然 `load_summarize_chain` 仍在使用，但现代 LangChain 推荐使用 LCEL 显式构建链以获得更好的灵活性：

- **Stuff**: 使用 `create_stuff_documents_chain`。
- **Map-Reduce**: 建议参考 [Map-Reduce 摘要实现](https://python.langchain.com/docs/how_to/summarize/#map-reduce)。

## 内部辅助逻辑

- 通过 `loader_mapping` 自动分发到对应的加载函数（`_load_stuff_chain`, `_load_map_reduce_chain`, `_load_refine_chain`）。
- 默认 Prompt 来源于 `langchain_classic.chains.summarize` 下的预定义模板。
