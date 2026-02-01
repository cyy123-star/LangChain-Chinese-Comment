# ModelLaboratory (模型实验室)

`ModelLaboratory` 是一个用于横向对比不同 LLM 或 Chain 表现的实用工具。它可以让你在相同的输入下，直观地观察多个模型的输出差异。

## 核心职责

- **多模型对比**: 同时运行多个模型或 Chain。
- **彩色输出**: 使用不同的颜色区分不同模型的返回内容。
- **输入一致性**: 确保所有待测模型接收到的输入文本完全一致。

## 使用场景

- **模型选型**: 对比 GPT-4、Claude 和 Llama 在特定任务上的优劣。
- **提示词调优**: 对比同一个模型在不同提示词模板下的表现差异。
- **链效果评估**: 对比基础 LLMChain 与带有记忆或搜索能力的复杂 Chain。

## 使用示例

```python
from langchain_openai import OpenAI
from langchain_anthropic import Anthropic
from langchain_classic.model_laboratory import ModelLaboratory

# 1. 准备要对比的模型
llms = [
    OpenAI(temperature=0),
    Anthropic(temperature=0)
]

# 2. 创建实验室
lab = ModelLaboratory.from_llms(llms)

# 3. 运行对比
lab.compare("用一句话解释量子纠缠。")
```

## 限制与建议

- **输入限制**: 目前主要支持单输入、单输出的场景。
- **可视化**: 结果直接打印到控制台，适合快速调试。对于大规模、可量化的评估，建议使用 `evaluation` 模块或 LangSmith 平台。
