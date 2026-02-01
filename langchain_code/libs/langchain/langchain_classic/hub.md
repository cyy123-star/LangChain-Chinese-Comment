# Hub (提示词仓库集成)

`hub` 模块是 LangChain 与 [LangChain Hub](https://smith.langchain.com/hub) 交互的官方接口。它允许开发者像拉取代码仓库一样，轻松地上传、下载和共享高质量的提示词模板。

## 核心功能

1. **`pull`**: 从 Hub 拉取提示词模板。
2. **`push`**: 将本地定义的提示词模板发布到 Hub。

## 为什么使用 Hub？

- **版本控制**: 提示词的每次修改都有记录，方便回滚和对比。
- **团队协作**: 团队成员可以共享同一套经过优化的提示词。
- **社区力量**: 可以直接使用社区公开的优秀提示词（如 RAG 专用提示词）。

## 使用示例

### 拉取提示词
```python
from langchain import hub

# 拉取一个公开的 RAG 提示词
prompt = hub.pull("rlm/rag-prompt")

# 使用拉取的提示词
# chain = prompt | llm | output_parser
```

### 推送提示词
```python
from langchain import hub
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template("Hello, {name}!")
hub.push("my-username/my-awesome-prompt", prompt)
```

## 注意事项

- **身份验证**: 使用 `push` 或拉取私有提示词时，需要设置环境变量 `LANGCHAIN_API_KEY`。
- **客户端库**: 该模块依赖于 `langsmith` 或 `langchainhub` SDK。推荐安装最新的 `langsmith`。
