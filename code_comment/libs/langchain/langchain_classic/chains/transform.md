# Transform Chain

`TransformChain` 是一个通用的功能链，允许用户在 Chain 流中运行任意的 Python 函数。它通常用于在不同 Chain 之间进行数据格式化、清洗或复杂的业务逻辑处理。

## 核心组件

- **transform**: 一个 Python 可调用对象（函数），接收一个字典并返回一个字典。
- **atransform**: (可选) 异步版本的转换函数。
- **input_variables**: 转换函数期望从输入字典中获取的键列表。
- **output_variables**: 转换函数将返回的键列表。

## 参数表

| 参数 | 类型 | 说明 |
| :--- | :--- | :--- |
| `input_variables` | `list[str]` | 输入键列表。 |
| `output_variables` | `list[str]` | 输出键列表。 |
| `transform` | `Callable` | 具体的转换逻辑函数。 |
| `atransform` | `Callable` | (可选) 异步转换逻辑函数。 |

## 执行逻辑 (Verbatim Snippet)

```python
@override
def _call(
    self,
    inputs: dict[str, str],
    run_manager: CallbackManagerForChainRun | None = None,
) -> dict[str, str]:
    # 直接调用用户定义的转换回调函数
    return self.transform_cb(inputs)

@override
async def _acall(
    self,
    inputs: dict[str, Any],
    run_manager: AsyncCallbackManagerForChainRun | None = None,
) -> dict[str, Any]:
    # 如果定义了异步回调则调用，否则回退到同步调用
    if self.atransform_cb is not None:
        return await self.atransform_cb(inputs)
    return self.transform_cb(inputs)
```

## 迁移指南 (LCEL)

在 LCEL 中，`TransformChain` 的功能可以直接通过 `RunnableLambda` 或简单的函数调用来实现，这更加直观且灵活：

```python
from langchain_core.runnables import RunnableLambda

def transform_func(inputs: dict) -> dict:
    text = inputs["text"]
    return {"short_text": text[:10]}

# 现代 LCEL 方式
chain = RunnableLambda(transform_func)

# 或者在链中使用
full_chain = some_llm_chain | RunnableLambda(transform_func) | next_step

result = chain.invoke({"text": "This is a very long sentence that needs shortening."})
# result: {'short_text': 'This is a '}
```
