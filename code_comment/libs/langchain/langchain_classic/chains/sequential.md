# libs\langchain\langchain_classic\chains\sequential.py

## 文件概述

`sequential.py` 定义了 LangChain 经典版中用于实现“链式调用”的核心组件：`SequentialChain` 和 `SimpleSequentialChain`。这些类允许开发者将多个独立的链串联起来，使前一个链的输出自动成为后一个链的输入。

该文件的主要职责包括：
1. **流水线构建**：实现链与链之间的自动数据传递。
2. **变量校验**：在链初始化时，自动检查所有步骤所需的输入变量是否在已知变量集中。
3. **输出管理**：支持选择性地返回最终步骤的输出或所有步骤的中间输出。

## 导入依赖

| 模块/类 | :--- |
| :--- | :--- |
| `langchain_classic.chains.base.Chain` | 所有顺序链继承的基础类。 |
| `langchain_core.callbacks` | 用于在流水线执行过程中进行监控的回调管理器。 |
| `pydantic.model_validator` | 用于在初始化时进行复杂的输入输出逻辑验证。 |

## 类与函数详解

### 1. SequentialChain

#### 功能描述
最通用的顺序链，支持多个输入变量和多个输出变量。它维护一个 `known_variables` 集合，确保每个步骤所需的输入都能在前序步骤或初始输入中找到。

#### 核心参数说明
| 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `chains` | `list[Chain]` | - | 是 | 要串联执行的链列表。 |
| `input_variables` | `list[str]` | - | 是 | 整个顺序链接收的初始输入变量名。 |
| `output_variables` | `list[str]` | - | 是 | 整个顺序链最终返回的结果变量名。 |
| `return_all` | `bool` | `False` | 否 | 是否返回执行过程中产生的所有中间变量。 |

#### 核心逻辑

1. **校验阶段 (`validate_chains`)**：
   - 检查初始输入与 Memory 键是否冲突。
   - 遍历 `chains`，验证每个链的 `input_keys` 是否在已有的输入或前序链的输出中。
   - 如果某个子链自带 Memory，校验时会排除 Memory 提供的变量。
   - 确保没有重复定义的输出键（防止覆盖）。
   - 自动推断 `output_variables`（如果用户未指定）：默认取最后一个链的输出键，或所有产生的中间键（如果 `return_all=True`）。

2. **执行阶段 (`_call`)**：

```python
def _call(
    self,
    inputs: dict[str, str],
    run_manager: CallbackManagerForChainRun | None = None,
) -> dict[str, str]:
    known_values = inputs.copy()
    _run_manager = run_manager or CallbackManagerForChainRun.get_noop_manager()
    
    for _i, chain in enumerate(self.chains):
        # 获取子链的回调管理器
        callbacks = _run_manager.get_child()
        # 执行子链，只获取新增输出
        outputs = chain(known_values, return_only_outputs=True, callbacks=callbacks)
        # 更新已知变量库，供后续链使用
        known_values.update(outputs)
    
    # 过滤并返回用户指定的输出变量
    return {k: known_values[k] for k in self.output_variables}
```

---

### 2. SimpleSequentialChain

#### 功能描述
`SequentialChain` 的简化版。它要求每个子链都只能有**一个输入**和**一个输出**。

#### 核心参数说明
| 参数名 | 类型 | 默认值 | 详细用途 |
| :--- | :--- | :--- | :--- |
| `chains` | `list[Chain]` | - | 串联执行的单入单出链列表。 |
| `strip_outputs` | `bool` | `False` | 是否对每个步骤的输出进行 `.strip()` 去除空格处理。 |
| `input_key` | `str` | `"input"` | 初始输入的键名。 |
| `output_key` | `str` | `"output"` | 最终输出的键名。 |

---

## 使用示例

### SequentialChain 示例 (多变量传递)
```python
from langchain_classic.chains import LLMChain, SequentialChain
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate

# 链 1: 根据剧名写大纲
llm = OpenAI(temperature=.7)
template = "你是剧本作家。剧名: {title}\n大纲:"
prompt_template = PromptTemplate(input_variables=["title"], template=template)
synopsis_chain = LLMChain(llm=llm, prompt=prompt_template, output_key="synopsis")

# 链 2: 根据大纲写剧评
template = "你是剧评人。大纲: {synopsis}\n评论:"
prompt_template = PromptTemplate(input_variables=["synopsis"], template=template)
review_chain = LLMChain(llm=llm, prompt=prompt_template, output_key="review")

# 构建顺序链
overall_chain = SequentialChain(
    chains=[synopsis_chain, review_chain],
    input_variables=["title"],
    output_variables=["synopsis", "review"],
    verbose=True
)

res = overall_chain.invoke({"title": "星际穿越 2"})
```

## 注意事项

1. **变量命名冲突**：如果后序链返回的键名与前序步骤已有的键名重复，会抛出 `ValueError`。请确保流水线中的变量名唯一。
2. **单向流动**：数据只能从前向后传递，不支持循环或分支（如需复杂逻辑，请使用 `RouterChain` 或直接使用 LCEL 的 `RunnableBranch`）。
3. **弃用说明**：与 `LLMChain` 类似，顺序执行现在更推荐使用 LCEL 的管道语法：`chain1 | chain2 | chain3`。

## 相关链接
- [LangChain Sequential Chain 官方文档](https://python.langchain.com/docs/concepts/chains/#sequential-chain)
- [LCEL 组合机制](https://python.langchain.com/docs/concepts/lcel/)
