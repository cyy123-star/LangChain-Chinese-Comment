# LLM Requests Chain

`LLMRequestsChain` 是一个将 LLM 与 HTTP 请求结合的链。它允许 LLM 生成 URL、发送请求并处理返回的响应内容（通常是 HTML 或 JSON）。

> **注意**：此组件已迁移到 `langchain-community`。

## 功能描述

该模块定义了 `LLMRequestsChain`，其核心流程如下：
1. **URL 生成**：LLM 根据输入信息生成需要访问的 URL。
2. **HTTP 请求**：使用 `requests` 库发送 GET 或 POST 请求。
3. **响应处理**：LLM 接收请求返回的原始内容，并根据用户需求提取信息或生成总结。

## 迁移指南

该组件现在维护在 `langchain-community` 包中。

### 1. 安装依赖
```bash
pip install langchain-community requests
```

### 2. 代码迁移
```python
# 旧写法 (已弃用)
# from langchain.chains import LLMRequestsChain

# 新写法
from langchain_community.chains.llm_requests import LLMRequestsChain
```

## 执行逻辑 (Verbatim Snippet)

在 `langchain_classic` 中，该模块使用了动态导入器来兼容旧版调用并发出警告：

```python
DEPRECATED_LOOKUP = {
    "LLMRequestsChain": "langchain_community.chains.llm_requests",
}

_import_attribute = create_importer(__package__, deprecated_lookups=DEPRECATED_LOOKUP)

def __getattr__(name: str) -> Any:
    """Look up attributes dynamically."""
    return _import_attribute(name)
```

## 注意事项

- **内容长度**：HTTP 响应内容（如大型 HTML 页面）可能会超过 LLM 的上下文窗口。通常需要配合 `BeautifulSoup` 等工具进行预处理。
- **安全性**：确保对生成的 URL 进行校验，防止请求恶意地址或内网敏感接口。

