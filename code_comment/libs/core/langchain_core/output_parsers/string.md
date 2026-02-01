# langchain_core.output_parsers.string

## 文件概述
`string.py` 包含 `StrOutputParser`，这是 LangChain 中最简单且最常用的输出解析器之一。它的主要职责是将模型输出（如 `AIMessage` 或 `AIMessageChunk` 对象）直接转换为纯文本字符串。

---

## 导入依赖
| 模块 | 作用 |
| :--- | :--- |
| `typing_extensions` | 提供 `override` 装饰器。 |
| `langchain_core.output_parsers.transform` | 导入 `BaseTransformOutputParser` 基类。 |

---

## 类与函数详解

### 1. StrOutputParser
**功能描述**: 从模型输出中提取文本内容并作为字符串返回。它继承自 `BaseTransformOutputParser`，因此原生支持流式输出。

#### 核心方法
- **`parse`**:
    - **功能**: 接收模型生成的文本并原样返回。
    - **参数**: `text: str` (模型生成的文本)。
    - **返回值**: `str` (相同的文本)。
- **`is_lc_serializable`**: 类方法，返回 `True`，表示该解析器支持序列化。
- **`get_lc_namespace`**: 返回序列化命名空间 `["langchain", "schema", "output_parser"]`。

---

## 核心逻辑
1. **直接提取**: 当在 LCEL 链中使用时，`StrOutputParser` 会自动从 `AIMessage` 的 `.content` 字段中提取文本。
2. **流式支持**: 作为一个转换解析器（Transform Parser），它能够逐块（chunk）接收模型的流式输出，并立即产生相应的文本块，这对于实时显示聊天结果非常有用。

---

## 使用示例

### 基本使用
```python
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o")
parser = StrOutputParser()

# 获取普通字符串输出
message = model.invoke("讲个笑话")
result = parser.invoke(message)
print(result)  # 这是一个纯字符串，而不是 AIMessage 对象
```

### 流式处理
```python
# 使用 transform() 处理流
stream = model.stream("写一个小故事")
for chunk in parser.transform(stream):
    print(chunk, end="", flush=True)
```

---

## 注意事项
- **简单性**: 该解析器不进行任何格式校验或结构化转换，仅负责类型转换（从消息对象到字符串）。
- **默认类型**: 在序列化时，其类型标识为 `"default"`。

---

## 内部调用关系
- `StrOutputParser` 继承自 `BaseTransformOutputParser`，后者处理了大部分流式处理和输入映射逻辑。
- 在 LangChain 的许多内置链中，它被用作默认的输出处理器，以确保最终返回给用户的是字符串。

---

## 元信息
- **最后更新时间**: 2026-01-29
- **对应源码版本**: LangChain Core v1.2.7
