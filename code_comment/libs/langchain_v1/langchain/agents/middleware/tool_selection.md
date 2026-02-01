# Tool Selection Middleware (工具预选中间件)

`tool_selection.py` 实现了 `LLMToolSelectorMiddleware`，它在主模型运行前，先使用一个（通常是更小更快的）模型从大量备选工具中筛选出最相关的工具。

## 核心功能 (Core Features)

1.  **工具过滤**: 应对“工具爆炸”问题（即工具数量超过模型上下文限制或导致模型注意力分散）。
2.  **Token 优化**: 仅将筛选后的工具定义发送给主模型，显著减少输入 Token。
3.  **强制包含**: 支持设置 `always_include` 列表，确保某些核心工具始终可用。
4.  **数量限制**: 支持 `max_tools` 参数，限制发送给主模型的工具总数。

## 类定义与参数 (Class Definition & Parameters)

### `LLMToolSelectorMiddleware`

| 参数 | 类型 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- |
| `model` | `str \| BaseChatModel \| None` | 主模型 | 用于执行筛选任务的模型。推荐使用 mini 系列。 |
| `system_prompt` | `str` | 默认指令 | 引导筛选模型的提示词。 |
| `max_tools` | `int \| None` | `None` | 最大筛选数量。 |
| `always_include` | `list[str]` | `[]` | 始终包含的工具名称列表。 |

## 执行逻辑 (Execution Logic)

1.  **请求预处理**:
    - 在 `before_model` 钩子中拦截 `ModelRequest`。
    - 检查可用工具数量。如果工具较少，可能直接跳过筛选。
2.  **筛选调用**:
    - 构造一个结构化输出请求。
    - 将所有可用工具的名称和描述发送给筛选模型。
    - 模型返回一个排序后的相关工具列表。
3.  **请求修改**:
    - 根据筛选结果和 `always_include` 策略，重新构建 `ModelRequest.tools` 列表。
    - 如果设置了 `max_tools`，则进行截断。
4.  **传递执行**: 将精简后的请求交给主模型执行。

## 使用场景 (Usage Scenarios)

- **大型工具库**: 当系统拥有成百上千个工具时。
- **降低成本**: 使用廉价模型预选，使用昂贵模型决策。
- **提高准确率**: 减少无关工具的干扰，让主模型更专注于关键信息。

## 注意事项 (Notes)

- **筛选精度**: 预选模型的误判可能导致主模型拿不到需要的工具。
- **首字延迟 (TTFT)**: 增加了一个额外的前置模型调用，会略微增加响应延迟。

