# OpenAIModerationChain

`OpenAIModerationChain` 用于将文本输入发送到 OpenAI 的审核端点（Moderation Endpoint）。它能够自动检测输入内容是否违反 OpenAI 的内容政策（如暴力、色情、仇恨言论等）。

## 核心功能

该链主要用于安全合规性检查：
1. **内容分类**: 识别输入文本是否属于敏感类别。
2. **违规阻断**: 如果检测到违规内容，可以配置为直接抛出异常或仅返回标记结果。

## 核心参数

| 参数 | 类型 | 说明 |
| :--- | :--- | :--- |
| `model_name` | `Optional[str]` | 指定使用的审核模型名称（如 `text-moderation-latest`）。 |
| `error` | `bool` | 如果发现违规内容，是否抛出 `ValueError`。默认为 `False`。 |
| `input_key` | `str` | 输入键名，默认为 `"input"`。 |
| `output_key` | `str` | 输出键名，默认为 `"output"`。 |

## 执行逻辑

1. **调用 API**: 将输入文本发送至 OpenAI 审核接口。
2. **结果处理**:
   - 如果 `results.flagged` 为 `True` 且 `self.error` 为 `True`，则抛出异常。
   - 如果 `results.flagged` 为 `True` 且 `self.error` 为 `False`，则将输出替换为警告提示语。
   - 如果未违规，则原样返回输入文本或返回审核详情。

```python
# 核心逻辑 (简化)
def _call(self, inputs: dict[str, Any]) -> dict[str, Any]:
    text = inputs[self.input_key]
    results = self.client.moderations.create(input=text)
    
    if results.flagged:
        if self.error:
            raise ValueError("违规内容已阻断")
        return {self.output_key: "该内容违反政策，已隐藏。"}
    
    return {self.output_key: text}
```

## 使用场景

- **用户输入过滤**: 在将用户提问发送给 LLM 之前进行审核。
- **输出安全检查**: 在将 LLM 生成的回答展示给用户之前进行审核。

## 依赖要求

需要安装 `openai` 包并配置 API Key：
```bash
pip install openai
export OPENAI_API_KEY='...'
```
