# libs\langchain\langchain_classic\chains\api\openapi\chain.py

`OpenAPIEndpointChain` 是一个用于根据 OpenAPI 规范（Swagger）与 API 接口进行交互的链。它能够解析 API 文档，根据用户问题选择合适的端点（Endpoint），构造请求参数并解析返回结果。

## 功能描述

该模块目前作为 `langchain_community` 中对应功能的动态导入层。其核心业务流程包括：
1.  **端点识别**：解析 OpenAPI 定义，找到能回答用户问题的 API 路径和方法。
2.  **请求构造**：利用 LLM 生成符合接口定义的 JSON 请求体或查询参数。
3.  **请求执行**：通过 HTTP 客户端发送请求。
4.  **响应总结**：将 API 返回的原始数据转换为人类可读的自然语言回答。

## 弃用说明

该文件已标记为弃用。相关逻辑已迁移至 `langchain_community`。

| 类/属性 | 迁移目标 |
| :--- | :--- |
| `OpenAPIEndpointChain` | `langchain_community.chains.openapi.chain.OpenAPIEndpointChain` |

## 迁移建议 (LangGraph)

传统的 `OpenAPIEndpointChain` 结构较硬。现代做法是使用 LangGraph 结合工具调用，或者使用专门的 OpenAPI Toolkit。

### 现代替代方案：使用 OpenAPI Toolkit

```python
from langchain_community.agent_toolkits.openapi.toolkit import RequestsToolkit
from langchain_community.utilities.requests import TextRequestsWrapper
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

# 1. 准备工具
toolkit = RequestsToolkit(
    requests_wrapper=TextRequestsWrapper(headers={}),
    allow_dangerous_requests=True # 注意安全性
)
tools = toolkit.get_tools()

# 2. 创建智能体
llm = ChatOpenAI(model="gpt-4o")
agent = create_react_agent(llm, tools)

# 3. 执行
response = agent.invoke({"messages": [("user", "Fetch the list of users from the API")]})
```

## 注意事项

1.  **安全性 (重要)**：允许 LLM 构造并发送 HTTP 请求具有潜在风险（SSRF、未授权访问等）。必须严格控制 `allow_dangerous_requests` 开关，并确保 API 凭证权限最小化。
2.  **规范完整性**：OpenAPI 文档（YAML/JSON）必须包含清晰的 `description` 字段，否则 LLM 无法准确判断每个端点的用途。
3.  **复杂请求处理**：对于需要多步调用（例如先登录获取 Token，再查询数据）的场景，建议使用 Agent 而非单一的 Chain。

