# libs\langchain\langchain_classic\chains\api\base.py

## 文件概述

`base.py` 实现了 `APIChain`，这是一种能够根据自然语言问题，自动生成 API 请求 URL、执行请求并总结响应结果的链。它通常用于让 LLM 与 RESTful API 进行交互。

## 核心类：APIChain (已弃用)

`APIChain` 继承自 `Chain`，通过两个内部的 `LLMChain` 分别负责生成 URL 和解析响应。

### 核心属性

| 属性名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `api_request_chain` | `LLMChain` | 负责将问题和 API 文档转换为请求 URL 的链。 |
| `api_answer_chain` | `LLMChain` | 负责将 API 响应结果结合原始问题总结为最终答案的链。 |
| `requests_wrapper` | `TextRequestsWrapper` | 实际执行 HTTP 请求的工具类（来自 `langchain_community`）。 |
| `api_docs` | `str` | API 的文档说明（通常是 OpenAPI/Swagger 的简化版）。 |
| `limit_to_domains` | `Sequence[str]` | **安全性设置**：限制该链允许访问的域名列表。 |

### 执行逻辑 (`_call` 方法)

`APIChain` 的执行过程分为三个主要步骤：

1.  **预测 URL**: 调用 `api_request_chain.predict`，根据用户问题和 `api_docs` 生成目标 API 的 URL。
2.  **执行请求**:
    - 校验生成的 URL 是否在 `limit_to_domains` 允许范围内（**安全检查**）。
    - 使用 `requests_wrapper` 执行 HTTP GET 请求。
3.  **总结答案**: 调用 `api_answer_chain.predict`，将问题、生成的 URL 和 API 返回的内容整合，输出最终答案。

### 源码片段：执行流程

```python
def _call(
    self,
    inputs: dict[str, Any],
    run_manager: CallbackManagerForChainRun | None = None,
) -> dict[str, str]:
    # 1. 生成 URL
    api_url = self.api_request_chain.predict(
        question=question,
        api_docs=self.api_docs,
        callbacks=_run_manager.get_child(),
    )
    # 2. 安全检查与执行
    if self.limit_to_domains and not _check_in_allowed_domain(api_url, self.limit_to_domains):
        raise ValueError(f"{api_url} is not in the allowed domains")
    api_response = self.requests_wrapper.get(api_url)
    # 3. 总结响应
    answer = self.api_answer_chain.predict(
        question=question,
        api_docs=self.api_docs,
        api_url=api_url,
        api_response=api_response,
        callbacks=_run_manager.get_child(),
    )
    return {self.output_key: answer}
```

## 静态方法：from_llm_and_api_docs

便捷的工厂方法，只需提供 LLM 和 API 文档即可快速创建实例：

```python
chain = APIChain.from_llm_and_api_docs(
    llm=llm,
    api_docs=OPENAPI_DOCS,
    limit_to_domains=["https://api.example.com"]
)
```

## 安全性警告

- **任意请求风险**: 该链允许模型生成 URL。如果未设置 `limit_to_domains` 或设置不当，恶意用户可能通过该链探测内网服务或发送非法请求。
- **推荐迁移**: 官方建议迁移到 **LangGraph**，利用其工具调用（Tool Calling）功能来更精准地控制 API 交互。
