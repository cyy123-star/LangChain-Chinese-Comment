# message.py

## 文件概述
`message.py` 模块定义了消息提示词模板的基础抽象类 `BaseMessagePromptTemplate`。该类是所有能够生成单个或多个聊天消息（`BaseMessage`）的模板类的基石，为 LangChain 的对话式提示词系统提供了统一的接口。

---

## 导入依赖
- `abc`: 用于定义抽象基类和抽象方法。
- `langchain_core.load.Serializable`: 提供序列化功能。
- `langchain_core.utils.interactive_env`: 用于检测当前是否处于交互式环境（如 Jupyter Notebook）。
- `langchain_core.messages`: 导入基础消息类型。
- `langchain_core.prompts.chat`: 导入聊天提示词模板类（用于类型提示和动态组合）。

---

## 类与函数详解

### 1. `BaseMessagePromptTemplate` (类)
所有消息提示词模板的抽象基类。

#### 核心属性与方法
| 名称 | 类型 | 描述 |
| :--- | :--- | :--- |
| `input_variables` | `property` (抽象) | 返回该模板所需的输入变量名列表。 |
| `format_messages` | `method` (抽象) | 将传入的关键字参数格式化为 `BaseMessage` 对象列表。 |
| `aformat_messages` | `async method` | `format_messages` 的异步版本，默认直接调用同步版本。 |
| `pretty_repr` | `method` | 返回模板的人类可读表示。 |
| `pretty_print` | `method` | 打印模板的人类可读表示，在交互式环境下支持 HTML 格式。 |
| `__add__` | `method` | 重载 `+` 运算符，支持将消息模板与其他模板组合成 `ChatPromptTemplate`。 |

#### 核心逻辑
- **组合机制**：通过 `__add__` 方法，开发者可以使用 `template1 + template2` 的方式轻松构建复杂的对话模板。该方法内部会动态导入 `ChatPromptTemplate` 并将当前对象包装其中。
- **序列化**：继承自 `Serializable`，确保模板可以被保存和加载。

#### 注意事项
- 这是一个抽象类，不能直接实例化。常用的具体实现包括 `HumanMessagePromptTemplate`、`AIMessagePromptTemplate` 等（通常在 `chat.py` 中定义）。

---

## 内部调用关系
- **继承体系**:
  - `BaseMessagePromptTemplate` 继承自 `Serializable`。
  - 具体的消息模板类（如 `HumanMessagePromptTemplate`）继承自此类。
- **与 ChatPromptTemplate 的关系**:
  - `ChatPromptTemplate` 实际上是由一个或多个 `BaseMessagePromptTemplate` 对象组成的列表。

---

## 相关链接
- [LangChain 官方文档 - Chat Prompt Templates](https://python.langchain.com/docs/modules/model_io/prompts/chat_prompt_template/)
- [langchain_core.messages 源码](../messages/base.py)

---
**对应源码版本**: LangChain Core v1.2.7
**最后更新时间**: 2026-01-29
