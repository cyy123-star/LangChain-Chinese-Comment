# Load (序列化与加载)

`load` 模块负责 LangChain 对象的序列化（Serialization）和反序列化（Deserialization）。它确保复杂的链、提示词模板和消息可以被保存为 JSON 并重新加载，而不会丢失结构信息。

## 核心功能

1. **`dumpd` / `dumps`**: 将 LangChain 对象转换为可序列化的字典或 JSON 字符串。
2. **`load` / `loads`**: 从字典或 JSON 字符串中还原 LangChain 对象。
3. **安全加载**: 在加载过程中验证类路径，防止执行恶意代码。

## 核心概念：`Serializable`

大多数 LangChain 核心类都继承自 `Serializable` 基类。这使得它们能够携带有关其所属包和类的元数据，从而实现跨环境的精准还原。

## 使用示例

```python
from langchain.load import dumpd, load
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template("Tell me a joke about {topic}")

# 序列化
data = dumpd(prompt)

# 反序列化
new_prompt = load(data)
```

## 应用场景

- **提示词管理**: 将复杂的提示词模板保存到文件或数据库中。
- **配置持久化**: 保存整个 LCEL 链的配置。
- **跨语言/环境通信**: 在不同系统间传递结构化的 LangChain 对象。

## 迁移指南

- **标准化**: 序列化逻辑现在已迁移至 `langchain-core`。
- **LangSmith 兼容**: 该模块生成的 JSON 格式与 LangSmith 平台完全兼容，便于在平台上进行版本控制。
