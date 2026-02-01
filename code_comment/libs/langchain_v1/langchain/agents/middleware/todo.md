# Todo List Middleware (待办事项/规划中间件)

`todo.py` 实现了 `TodoListMiddleware`，它为代理提供了结构化任务规划和进度跟踪的能力。这对于处理复杂的多步骤任务非常有用。

## 核心功能 (Core Features)

1.  **任务规划**: 允许代理通过 `write_todos` 工具创建、更新和删除待办事项。
2.  **状态跟踪**: 每个任务支持 `pending`, `in_progress`, `completed` 三种状态。
3.  **用户可见性**: 任务列表存储在 `AgentState` 中，可以方便地展示给最终用户。
4.  **智能引导**: 自动注入系统提示词，引导模型在处理复杂任务时先进行规划，并及时更新状态。

## 核心组件 (Core Components)

### `TodoListMiddleware`

| 参数 | 类型 | 说明 |
| :--- | :--- | :--- |
| `system_prompt` | `str` | 引导模型使用 Todo 工具的系统提示词。 |
| `tool_description` | `str` | `write_todos` 工具的详细描述。 |

### `Todo` (数据结构)
- `content`: 任务描述文本。
- `status`: `pending` | `in_progress` | `completed`。

## 注入的工具 (Injected Tools)

### `write_todos`
- **功能**: 创建或管理任务列表。
- **参数**: `todos: list[Todo]`（全量覆盖更新）。
- **说明**: 中间件会自动限制模型在单轮对话中最多调用一次该工具，以防止并行冲突。

## 执行逻辑 (Execution Logic)

1.  **状态初始化**: 定义 `PlanningState` 包含 `todos` 列表。
2.  **工具注入**: 在初始化时将 `write_todos` 加入代理的工具箱。
3.  **Prompt 增强**: 在 `before_model` 钩子中，将当前任务列表状态和引导提示词注入到模型的上下文。
4.  **状态更新**: 当模型调用 `write_todos` 时，工具会通过 LangGraph 的 `Command` 更新全局状态中的 `todos`。

## 使用场景 (Usage Scenarios)

- **多步骤重构**: 分阶段跟踪代码修改进度。
- **长流程研究**: 记录已搜索的信息和待验证的假设。
- **复杂部署**: 确保所有前置检查项都已完成。

## 注意事项 (Notes)

- **避免滥用**: 引导词中明确指出，对于 3 步以内的简单任务，不建议模型使用该工具以节省 Token。
- **及时更新**: 模型需要养成“开始工作前标记 in_progress，完成后标记 completed”的习惯。

