# base.py

## 文件概述
`base.py` 是 LangChain 框架中工具（Tools）系统的基石。它定义了所有工具必须遵循的核心接口 `BaseTool`，以及相关的异常处理、架构（Schema）生成工具和工具集（Toolkit）基类。

工具是 LangChain 中 Agent 或其他组件执行具体动作（如搜索、计算、数据库查询等）的单元。通过继承 `BaseTool`，开发者可以将任何 Python 函数封装为模型可调用的工具。

## 导入依赖
该文件导入了大量核心模块，主要包括：
- `abc`: 用于定义抽象基类。
- `pydantic`: 用于输入验证和架构定义（兼容 v1 和 v2）。
- `langchain_core.callbacks`: 处理工具执行过程中的回调追踪。
- `langchain_core.messages.tool`: 定义 `ToolCall` 和 `ToolMessage`，用于与模型交互。
- `langchain_core.runnables`: 工具本身也是 `Runnable` 对象，支持 LCEL 语法。

## 类与函数详解

### 1. BaseTool (抽象基类)
**功能描述**: 所有 LangChain 工具的抽象基类。它继承自 `RunnableSerializable`，这意味着工具可以被序列化、配置，并作为 Chain 的一部分运行。

#### 核心属性
| 参数名 | 类型 | 默认值 | 是否必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `name` | `str` | - | 是 | 工具的唯一名称，用于向模型标识该工具。 |
| `description` | `str` | - | 是 | 工具的功能描述，模型根据此描述决定何时、为何使用该工具。 |
| `args_schema` | `Type[BaseModel]` | `None` | 否 | 用于验证和解析工具输入参数的 Pydantic 模型类。 |
| `return_direct` | `bool` | `False` | 否 | 若为 `True`，工具执行后将直接返回结果并停止 Agent 循环。 |
| `handle_tool_error` | `bool \| str \| Callable` | `False` | 否 | 如何处理工具内部抛出的 `ToolException`。 |
| `response_format` | `Literal["content", "content_and_artifact"]` | `"content"` | 否 | 指定返回结果是纯内容还是包含原始构件（Artifact）的元组。 |

#### 核心方法
- **`run` / `arun`**:
    - **功能**: 执行工具逻辑。内部负责处理回调管理、输入验证、异常捕获和结果格式化。
    - **参数**: `tool_input` (输入数据), `callbacks` (可选回调), `config` (运行时配置) 等。
    - **返回值**: 工具执行的结果，通常被包装成 `ToolMessage`。
- **`_run` / `_arun` (抽象方法)**:
    - **功能**: 子类必须实现的具体业务逻辑。
- **`invoke` / `ainvoke`**:
    - **功能**: 实现 `Runnable` 接口，使工具支持 `tool.invoke(input)` 调用方式。
- **`_parse_input`**:
    - **功能**: 使用 `args_schema` 验证和清理输入参数，处理字符串输入到字典输入的转换。

### 2. ToolException
**功能描述**: 工具执行过程中抛出的自定义异常。使用此异常可以让 Agent 优雅地处理错误（通过 `handle_tool_error` 逻辑）而不会中断整个程序运行。

### 3. create_schema_from_function
**功能描述**: 从一个普通的 Python 函数签名中自动推导并创建一个 Pydantic 模型类。这在将普通函数转换为工具时非常有用。

### 4. InjectedToolArg / InjectedToolCallId
**功能描述**: 用于类型标注（Type Annotation）的特殊标记类。
- **`InjectedToolArg`**: 标记该参数应在运行时由框架注入，而不应出现在发送给模型的工具定义（Schema）中。
- **`InjectedToolCallId`**: 专门用于注入当前工具调用的唯一 ID（`tool_call_id`）。

### 5. BaseToolkit (抽象基类)
**功能描述**: 相关工具的集合基类。
- **方法 `get_tools`**: 抽象方法，返回该工具集包含的所有工具列表。

## 核心逻辑解读
1. **输入解析与验证**: 当工具被调用时，`_parse_input` 会根据 `args_schema` 检查输入。如果输入是字符串但 Schema 期望多个参数，它会尝试将字符串映射到第一个参数。
2. **注入参数处理**: 在生成发送给模型（如 OpenAI）的 JSON Schema 时，所有被标记为 `InjectedToolArg` 的参数都会被过滤掉。而在实际调用 `_run` 时，框架会负责将这些运行时信息（如 `tool_call_id`）填入。
3. **错误处理流程**: 
    - 捕获 `ValidationError`（输入验证错误）和 `ToolException`（执行错误）。
    - 根据配置的 `handle_validation_error` 或 `handle_tool_error` 标志返回错误描述字符串或调用自定义函数。
4. **输出格式化**: `_format_output` 确保输出符合模型要求。如果提供了 `tool_call_id`，它会将结果包装成 `ToolMessage`；如果设置了 `content_and_artifact`，则支持分离展示内容和原始数据。

## 使用示例
### 创建自定义工具
```python
from typing import Type, Annotated
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool, InjectedToolCallId

class SearchInput(BaseModel):
    query: str = Field(description="搜索关键词")

class MySearchTool(BaseTool):
    name: str = "my_search"
    description: str = "在自定义数据库中搜索信息"
    args_schema: Type[BaseModel] = SearchInput

    def _run(self, query: str, tool_call_id: Annotated[str, InjectedToolCallId]) -> str:
        # 这里可以使用注入的 tool_call_id
        return f"搜索结果: {query} (ID: {tool_call_id})"

tool = MySearchTool()
print(tool.run({"query": "LangChain"}))
```

## 注意事项
- **名称唯一性**: `name` 在整个 Agent 运行环境中必须唯一，否则模型可能会产生混淆。
- **描述的重要性**: `description` 是模型进行工具路由的唯一依据，编写清晰、准确的描述至关重要。
- **Pydantic 版本**: `BaseTool` 内部处理了 Pydantic v1 和 v2 的兼容性，但在自定义 `args_schema` 时建议统一使用一个版本。

## 内部调用关系
- **调用者**: `AgentExecutor`, `RunnableBinding`, `ChatModel` 等。
- **内部依赖**: `CallbackManager` 处理追踪，`ToolMessage` 处理输出通信。

## 相关链接
- [LangChain Tools 官方概念指南](https://python.langchain.com/docs/concepts/#tools)
- [如何创建自定义工具](https://python.langchain.com/docs/how_to/custom_tools/)

---
最后更新时间: 2026-01-29
对应源码版本: LangChain Core v1.2.7
