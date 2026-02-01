# APIChain (Deprecated)

`APIChain` 用于通过 LLM 与 REST API 进行交互。它将用户的问题转换为 API 请求，执行请求，并将响应转换回自然语言回答。

> **警告**: 该类自 v0.2.13 起已弃用，并将于 v1.0 中移除。建议使用 [LangGraph](https://langchain-ai.github.io/langgraph/) 或带有 `RequestsToolkit` 的智能体。

## 核心组件

| 参数 | 类型 | 说明 |
| :--- | :--- | :--- |
| `api_request_chain` | `LLMChain` | 用于根据用户输入和 API 文档生成 API URL 的链。 |
| `api_answer_chain` | `LLMChain` | 用于根据 API 响应和原始问题生成最终回答的链。 |
| `requests_wrapper` | `TextRequestsWrapper` | 封装了 HTTP 请求逻辑的包装器。 |
| `api_docs` | `str` | 描述 API 接口、参数和用法的手册。 |
| `limit_to_domains` | `Optional[Sequence[str]]` | 安全限制，仅允许访问指定的域名列表。 |

## 执行逻辑

1. **生成请求**: `api_request_chain` 接收用户输入和 `api_docs`，输出一个 API URL 字符串。
2. **执行请求**: `requests_wrapper` 执行生成的 URL（默认为 GET 请求）。
3. **生成回答**: `api_answer_chain` 接收原始问题、生成的 URL 和 API 响应内容，生成最终回复。

```python
# 核心调用逻辑 (简化)
def _call(self, inputs: dict[str, Any]) -> dict[str, Any]:
    question = inputs[self.input_key]
    # 1. 生成 URL
    api_url = self.api_request_chain.predict(question=question, api_docs=self.api_docs)
    # 2. 调用 API
    api_response = self.requests_wrapper.get(api_url)
    # 3. 总结结果
    answer = self.api_answer_chain.predict(
        question=question, 
        api_url=api_url, 
        api_response=api_response
    )
    return {self.output_key: answer}
```

## 安全提示

由于 LLM 生成的代码直接控制网络请求，请务必设置 `limit_to_domains` 以防止服务器端请求伪造 (SSRF) 攻击。

## 迁移方案 (LangGraph)

现代做法是使用智能体，使其能够根据 API 文档动态决定调用哪些接口。

```python
from langchain_community.agent_toolkits.openapi import planner
from langgraph.prebuilt import create_react_agent

# 使用 RequestsToolkit 替代 APIChain
# 这种方式更灵活，支持 POST/PUT/DELETE 且能处理复杂的 API 链式调用
```
