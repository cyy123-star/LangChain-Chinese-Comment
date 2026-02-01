# Configurable 详解

## 文件概述
`configurable.py` 模块定义了 LangChain 中用于动态配置 `Runnable` 对象的机制。它允许开发者在运行时通过 `config` 参数动态修改组件的属性（字段）或直接替换整个组件（备选方案）。

这是实现高度灵活、可定制化 AI 工作流的核心工具。

---

## 导入依赖
- `Runnable`, `RunnableSerializable`: 核心运行单元。
- `RunnableConfig`, `merge_configs`: 运行时配置及其合并逻辑。
- `ConfigurableField`, `ConfigurableFieldSpec`: 用于描述可配置字段的规范。
- `WeakValueDictionary`, `threading`: 用于管理枚举类型和线程安全。

---

## 类与函数详解

### `DynamicRunnable` (基类)
这是一个抽象基类，用于所有可以被动态配置的 `Runnable` 对象。
- **核心逻辑**：它并不直接执行逻辑，而是在调用 `invoke`、`stream` 等方法前，先调用 `prepare()` 方法。`prepare()` 会根据传入的 `config` 动态生成一个具体的、已经绑定好参数的 `Runnable` 对象。

---

### `RunnableConfigurableFields`
用于动态修改一个 `Runnable` 内部的字段。

**使用场景**：比如你想在运行时动态调整 LLM 的 `temperature` 或 `max_tokens`。

#### 核心方法 `_prepare`
- **逻辑描述**：
  1. 从 `config["configurable"]` 中提取对应的值。
  2. 使用这些新值创建一个原 `Runnable` 类的全新实例。
  3. 如果没有提供配置，则使用默认实例。

---

### `RunnableConfigurableAlternatives`
用于在运行时从多个备选组件中选择一个。

**使用场景**：比如你想根据用户的偏好动态切换不同的 Prompt 模板或不同的 LLM 模型。

#### 核心属性
- `which`: 一个 `ConfigurableField` 对象，用于指定在配置字典中查找哪个 ID。
- `alternatives`: 一个字典，包含所有候选的 `Runnable` 对象。
- `default_key`: 默认使用的组件键名。

#### 核心方法 `_prepare`
- **逻辑描述**：
  1. 查看 `config["configurable"][which.id]` 的值。
  2. 如果该值存在于 `alternatives` 字典中，则返回对应的组件。
  3. 否则，返回默认组件。

---

## 使用示例

### 1. 动态配置字段 (Configurable Fields)
```python
from langchain_openai import ChatOpenAI
from langchain_core.runnables import ConfigurableField

model = ChatOpenAI(temperature=0).configurable_fields(
    temperature=ConfigurableField(
        id="llm_temp",
        name="Temperature",
        description="LLM 的温度参数"
    )
)

# 正常调用（使用默认值 0）
model.invoke("你好")

# 运行时修改温度为 0.9
model.with_config(configurable={"llm_temp": 0.9}).invoke("你好")
```

### 2. 动态切换组件 (Configurable Alternatives)
```python
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import ConfigurableField

prompt = PromptTemplate.from_template(
    "讲一个关于 {topic} 的笑话"
).configurable_alternatives(
    ConfigurableField(id="my_prompt"),
    default_key="joke",
    poem=PromptTemplate.from_template("写一首关于 {topic} 的诗")
)

# 默认使用笑话 Prompt
chain = prompt | model
chain.invoke({"topic": "熊"})

# 运行时切换到诗歌 Prompt
chain.with_config(configurable={"my_prompt": "poem"}).invoke({"topic": "熊"})
```

---

## 注意事项
- **序列化**：`DynamicRunnable` 是可序列化的，这意味着包含动态配置的链可以被保存并重新加载。
- **作用域**：通过 `with_config` 传入的配置仅对当前调用有效。
- **前缀机制**：在嵌套使用 `ConfigurableAlternatives` 时，建议开启 `prefix_keys=True`，以避免不同层级之间的 ID 冲突（例如 `model==gpt3/temperature`）。

---

## 内部调用关系
- **与 `Runnable` 接口关系**：它是通过 `Runnable.configurable_fields` 和 `Runnable.configurable_alternatives` 这两个快捷方法创建出来的。
- **与 `config.py` 关系**：深度依赖 `RunnableConfig` 中的 `configurable` 字典来获取运行时指令。

---

## 相关链接
- [LangChain 官方指南 - Runtime Configuration](https://python.langchain.com/docs/expression_language/how_to/configure)
- [源码引用: base.py](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/core/langchain_core/runnables/base.py)

---
最后更新时间: 2026-01-29
对应源码版本: LangChain Core v1.2.7
