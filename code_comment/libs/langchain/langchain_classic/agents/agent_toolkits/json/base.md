# libs\langchain\langchain_classic\agents\agent_toolkits\json\base.py

`json/base.py` 模块定义了创建 JSON 代理的核心函数。

## 核心函数

### `create_json_agent`

创建一个专门用于处理 JSON 数据的 `AgentExecutor`。

#### 函数原型

```python
def create_json_agent(
    llm: BaseLanguageModel,
    toolkit: JsonToolkit,
    callback_manager: Optional[BaseCallbackManager] = None,
    prefix: str = JSON_PREFIX,
    suffix: str = JSON_SUFFIX,
    format_instructions: str = JSON_FORMAT_INSTRUCTIONS,
    input_variables: Optional[List[str]] = None,
    verbose: bool = False,
    agent_executor_kwargs: Optional[Dict[str, Any]] = None,
    **kwargs: Any,
) -> AgentExecutor:
```

#### 参数说明

| 参数 | 类型 | 描述 |
| :--- | :--- | :--- |
| `llm` | `BaseLanguageModel` | 代理使用的语言模型。 |
| `toolkit` | `JsonToolkit` | 包含 JSON 操作工具的工具包，必须包含 `JsonSpec`。 |
| `callback_manager` | `Optional[BaseCallbackManager]` | 回调管理器，用于跟踪代理执行过程。 |
| `prefix` | `str` | 提示词前缀，默认为 `JSON_PREFIX`。 |
| `suffix` | `str` | 提示词后缀，默认为 `JSON_SUFFIX`。 |
| `format_instructions` | `str` | 格式化指令，告知 LLM 如何输出 JSON。 |
| `verbose` | `bool` | 是否打印详细的执行日志。 |
| `agent_executor_kwargs` | `Optional[Dict[str, Any]]` | 传递给 `AgentExecutor` 的额外参数。 |

#### 实现细节

该文件使用了 `create_importer` 实现了动态属性查找。当开发者尝试从 `langchain_classic` 导入 `create_json_agent` 时，系统会发出弃用警告，并自动重定向到 `langchain_community.agent_toolkits.json.base`。

```python
DEPRECATED_LOOKUP = {
    "create_json_agent": "langchain_community.agent_toolkits.json.base",
}
```

## 迁移指南

由于该函数已被弃用，建议直接从 `langchain_community` 导入：

```python
from langchain_community.agent_toolkits.json.base import create_json_agent
```

## 使用场景

- 当你需要让代理根据用户的自然语言请求来查询或操作一个巨大的 JSON 文件时。
- 当 API 响应非常庞大，且只需要其中一小部分信息时。
