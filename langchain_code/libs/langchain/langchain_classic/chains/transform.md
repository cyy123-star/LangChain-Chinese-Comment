# Transform Chain

`transform` 模块提供了一个特殊的 Chain，它不调用 LLM，而是允许用户在 Chain 流中插入任意的 Python 函数来对数据进行转换。

## 核心组件

### 1. `TransformChain`
该类封装了一个同步或异步的回调函数。

| 参数/属性 | 类型 | 描述 |
| :--- | :--- | :--- |
| `input_variables` | `List[str]` | 输入字典中预期的键。 |
| `output_variables` | `List[str]` | 转换后返回字典中的键。 |
| `transform` | `Callable` | 同步转换函数。接收 `dict` 返回 `dict`。 |
| `atransform` | `Callable` | 异步转换函数。如果未提供，异步调用将回退到同步函数。 |

## 执行逻辑 (Verbatim Snippet)

`TransformChain` 的实现非常直接，它只是简单地调用用户提供的回调函数：

```python
class TransformChain(Chain):
    # ...
    @override
    def _call(
        self,
        inputs: dict[str, str],
        run_manager: CallbackManagerForChainRun | None = None,
    ) -> dict[str, str]:
        return self.transform_cb(inputs)

    @override
    async def _acall(
        self,
        inputs: dict[str, Any],
        run_manager: AsyncCallbackManagerForChainRun | None = None,
    ) -> dict[str, Any]:
        if self.atransform_cb is not None:
            return await self.atransform_cb(inputs)
        return self.transform_cb(inputs)
```

## 使用示例

```python
from langchain_classic.chains import TransformChain

def transform_func(inputs: dict) -> dict:
    text = inputs["text"]
    # 执行一些处理，例如清洗、格式化或调用外部 API
    shortened_text = "\n".join(text.split("\n")[:3])
    return {"output_text": shortened_text}

transform_chain = TransformChain(
    input_variables=["text"],
    output_variables=["output_text"],
    transform=transform_func
)
```

## 迁移指南 (LCEL)

在 LCEL 中，`TransformChain` 的功能完全被 `RunnableLambda` 所取代。`RunnableLambda` 更简洁，且能够更好地处理异步和流式调用。

### LCEL 迁移示例
```python
from langchain_core.runnables import RunnableLambda

def transform_func(inputs: dict) -> dict:
    return {"output_text": inputs["text"][:100]}

# 现代写法
runnable = RunnableLambda(transform_func)

# 或者直接在 pipe 中使用函数
chain = some_llm_chain | (lambda x: {"processed": x["text"].upper()})
```
