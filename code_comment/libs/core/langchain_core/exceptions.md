# exceptions.py - 异常定义

- **最后更新时间**: 2026-01-29
- **对应源码版本**: LangChain Core v1.2.7

## 文件概述

`exceptions.py` 定义了 LangChain 框架中使用的自定义异常类。这些异常类帮助开发者更精确地捕获和处理在链（Chains）、模型（Models）和输出解析器（Output Parsers）执行过程中可能出现的特定错误。

## 导入依赖

| 模块 | 作用 |
| :--- | :--- |
| `enum.Enum` | 用于定义错误代码枚举。 |
| `typing.Any` | 用于类型提示。 |

## 类与函数详解

### 1. ErrorCode (枚举)
- **功能描述**: 定义了 LangChain 内部错误代码，用于标识不同类型的错误。
- **成员**:
  - `INVALID_PROMPT_INPUT`: 提示词输入无效。
  - `INVALID_TOOL_RESULTS`: 工具执行结果无效。
  - `MESSAGE_COERCION_FAILURE`: 消息强制类型转换失败。
  - `MODEL_AUTHENTICATION`: 模型认证失败。
  - `MODEL_NOT_FOUND`: 未找到模型。
  - `MODEL_RATE_LIMIT`: 模型请求频率限制。
  - `OUTPUT_PARSING_FAILURE`: 输出解析失败。

### 2. LangChainException (基类)
- **功能描述**: 所有 LangChain 相关异常的基类。继承自 Python 的内置 `Exception`。
- **设计目的**: 允许用户通过捕获此异常来处理所有由 LangChain 框架抛出的非标准 Python 错误。

### 3. TracerException
- **功能描述**: 与追踪（Tracing）功能相关的异常。
- **应用场景**: 在回调处理器或追踪逻辑执行出错时抛出。

### 4. OutputParserException
- **功能描述**: 输出解析器在无法将模型输出解析为预期格式时抛出的异常。
- **参数说明**:
  | 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
  | :--- | :--- | :--- | :--- | :--- |
  | `error` | `Any` | - | 是 | 原始错误消息或错误对象。如果是字符串，将自动转换为带错误代码的消息。 |
  | `observation` | `str | None` | `None` | 否 | 发生错误时的观察结果（通常用于 Agent 循环）。 |
  | `llm_output` | `str | None` | `None` | 否 | 导致解析失败的原始 LLM 输出。 |
  | `send_to_llm` | `bool` | `False` | 否 | 是否应将此错误信息发送回 LLM 以尝试自我修正。 |

### 5. create_message
- **功能描述**: 创建一个包含排错指南链接的错误消息。
- **参数说明**:
  | 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
  | :--- | :--- | :--- | :--- | :--- |
  | `message` | `str` | - | 是 | 原始错误描述。 |
  | `error_code` | `ErrorCode` | - | 是 | 关联的错误代码。 |

## 核心逻辑

- **异常初始化**: `OutputParserException` 在初始化时会检查 `send_to_llm` 标志。如果设为 `True`，则必须同时提供 `observation` 和 `llm_output`，以便 Agent 系统能够利用这些上下文引导模型修正输出。
- **错误代码集成**: 字符串类型的错误消息会自动通过 `create_message` 包装，附加上官方排错文档的 URL。

## 使用示例

```python
from langchain_core.exceptions import OutputParserException, ErrorCode

try:
    # 模拟解析失败并请求 Agent 自我修正
    raise OutputParserException(
        error="JSON 格式不正确",
        observation="请确保输出是有效的 JSON 对象，包含 'answer' 字段。",
        llm_output='{"ans": "hello"}',
        send_to_llm=True
    )
except OutputParserException as e:
    print(f"错误内容: {e}")
    if e.send_to_llm:
        print(f"建议反馈给模型: {e.observation}")
```

## 相关链接
- [LangChain 故障排除指南](https://docs.langchain.com/oss/python/langchain/errors/)
