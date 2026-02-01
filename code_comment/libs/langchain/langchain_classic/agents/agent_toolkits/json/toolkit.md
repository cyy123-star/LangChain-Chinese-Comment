# libs\langchain\langchain_classic\agents\agent_toolkits\json\toolkit.py

`json/toolkit.py` 模块定义了 `JsonToolkit` 类，该类整合了多个用于操作 JSON 的工具。

## 核心类

### `JsonToolkit`

`JsonToolkit` 为代理提供了一组能够通过 `JsonSpec` 访问和查询 JSON 数据的工具。

#### 初始化参数

```python
def __init__(self, spec: JsonSpec):
    self.spec = spec
```

- **spec**: 一个 `JsonSpec` 实例，它封装了 JSON 数据并提供了访问接口。

#### 主要工具

`JsonToolkit.get_tools()` 会返回以下工具：
- **`json_spec_list_keys`**: 用于列出 JSON 对象在给定路径下的所有键。
- **`json_spec_get_value`**: 用于获取 JSON 对象在给定路径下的值。

#### 工作原理

1. **JsonSpec**: 首先需要将原始 JSON 字典包装在 `JsonSpec` 中。
2. **渐进式探索**: 代理不会一次性读取整个 JSON，而是使用 `list_keys` 查看结构，再使用 `get_value` 获取具体数据。这种方式能有效处理数 MB 甚至更大的 JSON 文件。

## 动态导入机制

该文件使用了 `create_importer` 实现了动态属性查找。当开发者尝试从 `langchain_classic` 导入 `JsonToolkit` 时，系统会发出弃用警告，并自动重定向到 `langchain_community.agent_toolkits.json.toolkit`。

```python
DEPRECATED_LOOKUP = {"JsonToolkit": "langchain_community.agent_toolkits.json.toolkit"}
```

## 迁移指南

由于该模块已被弃用，建议直接从 `langchain_community` 导入：

```python
from langchain_community.agent_toolkits.json.toolkit import JsonToolkit
```

## 注意事项

- **数据结构**: `JsonToolkit` 需要一个 `JsonSpec` 实例，该实例包装了原始的 JSON 字典。
- **效率**: 通过工具逐步探索 JSON，比将整个大型 JSON 直接传递给 LLM 更节省 Token 且更可靠。

