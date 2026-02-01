# Model Fallback Middleware (模型降级/备选中间件)

`model_fallback.py` 实现了 `ModelFallbackMiddleware`，它允许代理在主模型调用失败（例如由于速率限制、服务器超时或内容过滤）时，自动尝试使用一组预定义的备选模型。

## 核心功能 (Core Features)

1.  **自动重试机制**: 当模型调用抛出异常时，中间件会捕获异常并尝试列表中的下一个模型。
2.  **模型链式回退**: 支持配置多个备选模型，按顺序尝试直至成功或所有模型都失败。
3.  **模型动态初始化**: 支持传入字符串（自动初始化模型）或现有的 `BaseChatModel` 实例。
4.  **透明性**: 对于代理逻辑层来说，回退过程是透明的，只需关注最终的 `ModelResponse`。

## 类定义与参数 (Class Definition & Parameters)

### `ModelFallbackMiddleware`

| 参数 | 类型 | 说明 |
| :--- | :--- | :--- |
| `first_model` | `str \| BaseChatModel` | 主模型或第一个备选模型。 |
| `*additional_models` | `str \| BaseChatModel` | 额外的备选模型列表。 |

## 执行逻辑 (Execution Logic)

1.  **初始化**: 在 `__init__` 中将所有传入的模型统一转换为 `BaseChatModel` 列表。
2.  **请求包装 (`wrap_model_call`)**:
    - 首先调用 `handler(request)` 使用当前模型发起请求。
    - 如果成功，直接返回结果。
    - 如果失败（抛出 `Exception`），记录异常并进入循环：
        - 遍历 `self.models` 中的每一个备选模型。
        - 使用 `request.override(model=fallback_model)` 创建新的请求对象。
        - 再次调用 `handler`。
    - 如果所有模型都尝试失败，抛出最后一次捕获的异常。

## 使用场景 (Usage Scenarios)

- **提高稳定性**: 应对大模型 API 的偶发性故障（如 500 错误）。
- **配额管理**: 当主模型触发 Rate Limit 时，自动切换到备用模型。
- **混合模型策略**: 主模型使用高性能模型（如 GPT-4），备选模型使用低成本模型（如 GPT-3.5）。

## 注意事项 (Notes)

- **状态一致性**: 中间件只处理模型调用本身。如果模型调用产生了副作用（虽然通常不应该），回退过程可能会变得复杂。
- **性能开销**: 每次回退都会增加端到端的延迟。
- **成本控制**: 需要注意备选模型的成本，避免在不知情的情况下产生大量高昂费用。
