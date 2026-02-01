# libs\langchain\langchain_classic\chains\router\base.py

## 文件概述

`base.py` 定义了 LangChain 路由机制的基础抽象。路由链（Router Chain）的核心职责是根据输入动态决定下一步该调用哪个目标链（Destination Chain）。

## 核心数据结构：Route

`Route` 是一个 `NamedTuple`，用于表示路由决策的结果：

- `destination`: 目标链的名称（字符串）。如果为 `None`，通常表示路由失败或应跳转到默认链。
- `next_inputs`: 传递给目标链的输入字典。

## 核心抽象类：RouterChain

### 功能描述

`RouterChain` 是所有路由器的基类。它的输出必须包含 `destination` 和 `next_inputs`。

### 核心逻辑

```python
class RouterChain(Chain, ABC):
    def route(self, inputs: dict[str, Any], callbacks: Callbacks = None) -> Route:
        # 1. 调用自身逻辑（如 LLM 预测）
        result = self(inputs, callbacks=callbacks)
        # 2. 封装为 Route 对象返回
        return Route(result["destination"], result["next_inputs"])
```

## 核心类：MultiRouteChain

### 功能描述

`MultiRouteChain` 是一个完整的控制器，它持有一个 `RouterChain` 和一组 `destination_chains`。它协调路由决策的执行和目标链的调用。

### 核心属性

| 属性名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `router_chain` | `RouterChain` | 负责做决策的链。 |
| `destination_chains` | `Mapping[str, Chain]` | 可选的目标链集合，键为名称。 |
| `default_chain` | `Chain` | 兜底链，当路由无法匹配时使用。 |
| `silent_errors` | `bool` | 如果为 `True`，路由失败时使用默认链而不报错。 |

### 执行逻辑 (`_call`)

```python
def _call(
    self,
    inputs: dict[str, Any],
    run_manager: CallbackManagerForChainRun | None = None,
) -> dict[str, Any]:
    # 1. 获取子链的回调
    callbacks = run_manager.get_child()
    # 2. 调用路由器决定去向
    route = self.router_chain.route(inputs, callbacks=callbacks)

    # 3. 根据决策结果选择目标链
    if not route.destination:
        return self.default_chain(route.next_inputs, callbacks=callbacks)
    
    if route.destination in self.destination_chains:
        return self.destination_chains[route.destination](
            route.next_inputs, callbacks=callbacks
        )
    
    # 4. 异常处理
    if self.silent_errors:
        return self.default_chain(route.next_inputs, callbacks=callbacks)
    raise ValueError(f"Received invalid destination chain name '{route.destination}'")
```

## 注意事项

1. **输入转发**：路由器不仅决定去哪，还可以修改传递给下一个链的 `next_inputs`。
2. **解耦**：这种架构允许决策逻辑（路由器）与执行逻辑（目标链）完全解耦。
3. **现代替代**：在 LCEL 中，路由通常通过 `RunnableBranch` 或 `RunnableLambda` 实现，更加灵活且支持流式输出。
