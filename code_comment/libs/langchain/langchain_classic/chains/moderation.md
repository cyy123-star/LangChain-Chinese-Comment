# libs\langchain\langchain_classic\chains\moderation.py

## 文件概述

`moderation.py` 定义了 `OpenAIModerationChain`，这是一个专门用于内容审核的链。它封装了 OpenAI 的审核 API，用于检测输入文本是否包含暴力、仇恨言论、自残等违规内容。

## 核心类：OpenAIModerationChain

### 功能描述

`OpenAIModerationChain` 接收一段文本，调用 OpenAI 的 `moderations` 端点进行评估。如果文本违规，它可以根据配置抛出异常或返回特定的错误消息。

### 核心属性

| 属性名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `client` | `Any` | OpenAI 客户端实例。 |
| `model_name` | `str` | 使用的审核模型，默认为 `text-moderation-latest`。 |
| `error` | `bool` | 如果为 `True`，当内容不合规时抛出 `ValueError`。默认为 `False`。 |
| `input_key` | `str` | 输入字典中的键，默认为 `input`。 |
| `output_key` | `str` | 输出字典中的键，默认为 `output`。 |

### 核心逻辑

```python
def _call(
    self,
    inputs: dict[str, Any],
    run_manager: CallbackManagerForChainRun | None = None,
) -> dict[str, str]:
    text = inputs[self.input_key]
    
    # 调用 OpenAI 审核接口
    results = self.client.create(input=text, model=self.model_name)
    
    # 提取评估结果
    output = results["results"][0]
    
    # 如果发现违规内容且 error=True，则抛出异常
    if output["flagged"] and self.error:
        raise ValueError(
            f"The following text was flagged by OpenAI's moderation API: {text}"
        )
    
    # 返回审核结果字符串（或违规警告）
    return {self.output_key: text}
```

## 使用示例

```python
from langchain_classic.chains import OpenAIModerationChain

moderation_chain = OpenAIModerationChain(error=True)

try:
    # 如果输入违规内容，将抛出异常
    moderation_chain.invoke({"input": "一段包含违规内容的文本..."})
except ValueError as e:
    print(f"检测到违规: {e}")
```

## 注意事项

1. **API 密钥**：使用此链需要配置 `OPENAI_API_KEY` 环境变量。
2. **合规性检查**：这是将 LLM 应用投入生产前的关键安全步骤。
3. **LCEL 替代方案**：目前 OpenAI 审核功能更多地通过独立的 `OpenAIModerationChain` 或自定义的 `RunnableLambda` 实现。
