# libs\langchain\langchain_classic\chains\question_answering\chain.py

## 文件概述

`chain.py` 包含了 `load_qa_chain` 工厂方法，它是经典 LangChain 中用于创建“问答（QA）”相关文档组合链的核心入口。它根据用户指定的 `chain_type` 自动构建并配置相应的 `BaseCombineDocumentsChain` 子类。

## 核心方法：load_qa_chain (已弃用)

该方法是一个工厂函数，支持四种主要的问答策略。

### 参数说明

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `llm` | `BaseLanguageModel` | 链中使用的语言模型。 |
| `chain_type` | `str` | 策略类型，可选："stuff", "map_reduce", "refine", "map_rerank"。 |
| `verbose` | `bool` | 是否开启详细日志。 |
| `**kwargs` | `Any` | 传递给具体链构造函数的额外参数（如自定义 Prompt）。 |

### 策略详解

#### 1. Stuff (填充式)
- **实现函数**：`_load_stuff_chain`
- **逻辑**：将所有文档直接放入 Prompt 中一次性交给 LLM。
- **适用场景**：文档数量少、总长度不超限。

#### 2. Map-Reduce (映射-规约)
- **实现函数**：`_load_map_reduce_chain`
- **逻辑**：
    1. **Map**: 分别对每个文档进行摘要/提炼。
    2. **Reduce**: 将所有中间摘要合并，生成最终答案。
- **适用场景**：处理大量文档，受限于上下文窗口。

#### 3. Refine (迭代改进)
- **实现函数**：`_load_refine_chain`
- **逻辑**：遍历文档，第一个文档生成初始答案，后续每个文档根据当前内容对已有答案进行“润色”和“更新”。
- **适用场景**：需要结合多个文档的细节逐步构建答案。

#### 4. Map-Rerank (映射-重排序)
- **实现函数**：`_load_map_rerank_chain`
- **逻辑**：分别对每个文档提问，要求 LLM 给出一个答案及其置信度分数，最后返回分数最高的答案。
- **适用场景**：答案通常存在于单个文档中，且需要自动筛选最相关的那一个。

## 迁移建议 (LCEL)

该方法已被弃用，建议根据具体的 `chain_type` 迁移到现代的 LCEL 构建方式：

- **stuff**: 使用 `create_stuff_documents_chain`。
- **map_reduce**: 参考官方 [Map-Reduce 迁移指南](https://python.langchain.com/docs/versions/migrating_chains/map_reduce_chain)。
- **refine**: 参考官方 [Refine 迁移指南](https://python.langchain.com/docs/versions/migrating_chains/refine_chain)。
- **map_rerank**: 参考官方 [Map-Rerank 迁移指南](https://python.langchain.com/docs/versions/migrating_chains/map_rerank_docs_chain)。

## 内部辅助逻辑

文件内部通过 `loader_mapping` 字典映射 `chain_type` 到对应的私有加载函数（如 `_load_stuff_chain` 等），每个函数负责初始化对应的 LLMChain 和文档组合链。
