# structured.py

## 文件概述
`structured.py` 模块定义了 `StructuredPrompt` 类，这是一种处于 Beta 阶段的特殊提示词模板。它的设计目标是简化“提示词 + 结构化输出”的链式调用流程。

传统的做法是先定义提示词模板，再对模型调用 `with_structured_output`。而 `StructuredPrompt` 将两者合二为一：它在内部持有输出架构（Schema），并在通过 LCEL（`|` 运算符）连接模型时，自动配置模型以生成符合该架构的结果。

---

## 导入依赖
- `pydantic`: 用于定义输出架构（`BaseModel`）和数据验证。
- `langchain_core.language_models.base`: 导入基础语言模型类，用于类型检查。
- `langchain_core.prompts.chat`: 继承自 `ChatPromptTemplate`，支持多轮对话消息。
- `langchain_core.runnables.base`: 支持 LCEL 运行环境。

---

## 类与函数详解

### 1. `StructuredPrompt` (类)
集成结构化输出架构的聊天提示词模板。

#### 属性说明
| 属性名 | 类型 | 默认值 | 是否必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `schema_` | `dict \| type` | - | 是 | 输出数据的架构。可以是 Pydantic 模型类或 JSON Schema 字典。 |
| `structured_output_kwargs` | `dict[str, Any]` | `{}` | 否 | 传递给 `with_structured_output` 方法的额外参数。 |

#### 核心方法
- `__init__`: 初始化方法。确保必须传入非空的 `schema_`，并自动将多余的关键字参数归类到 `structured_output_kwargs` 中。
- `from_messages_and_schema`: 类方法，提供更直观的实例化方式。
- `pipe` / `__or__`: **核心逻辑实现**。
    - 当使用 `structured_prompt | model` 时，它会检查 `model` 是否支持 `with_structured_output`。
    - 如果支持，它会自动调用 `model.with_structured_output(self.schema_, **self.structured_output_kwargs)`，并返回一个完整的 `RunnableSequence`。

#### 使用示例
```python
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import StructuredPrompt

# 1. 定义输出架构
class UserInfo(BaseModel):
    name: str
    age: int

# 2. 创建结构化提示词
prompt = StructuredPrompt.from_messages_and_schema(
    [("human", "提取用户信息: {text}")],
    schema=UserInfo
)

# 3. 直接连接模型（无需手动调用 with_structured_output）
model = ChatOpenAI(model="gpt-4o")
chain = prompt | model

# 4. 调用并获得 Pydantic 对象
result = chain.invoke({"text": "我叫小明，今年 18 岁。"})
print(result) # 输出: UserInfo(name='小明', age=18)
```

---

## 注意事项
- **Beta 阶段**：该类目前被标记为 `@beta()`，未来 API 可能会有变动。
- **管道约束**：`StructuredPrompt` 必须连接到实现了 `with_structured_output` 接口的语言模型。如果连接的是普通 Runnable 或不支持该接口的模型，将抛出 `NotImplementedError`。

---

## 内部调用关系
- **继承关系**: `StructuredPrompt` -> `ChatPromptTemplate` -> `BaseChatPromptTemplate`。
- **自动配置机制**: 利用 `RunnableSequence` 将自身与经过 `with_structured_output` 装饰后的模型连接。

---

## 相关链接
- [LangChain 官方文档 - Structured Output](https://python.langchain.com/docs/modules/model_io/output_parsers/structured/)
- [langchain_core.runnables.base 源码](../runnables/base.py)

---
**对应源码版本**: LangChain Core v1.2.7
**最后更新时间**: 2026-01-29
