# libs\langchain\langchain_classic\agents\agent_toolkits\gmail\toolkit.py

此文档提供了 `libs\langchain\langchain_classic\agents\agent_toolkits\gmail\toolkit.py` 文件的详细中文注释。该模块定义了 Gmail 工具集。

## 核心说明：动态重定向

该模块已被弃用，其核心功能已重定向至 `langchain_community.agent_toolkits.gmail.toolkit`。

## 主要类

### `GmailToolkit`

`GmailToolkit` 封装了一系列用于与 Gmail 交互的工具。它通过 `GmailAPIWrapper` 与 Google Gmail API 进行底层通信。

#### 功能描述
- **邮件操作**: 发送邮件、获取单封邮件详细内容、列出邮件。
- **搜索能力**: 搜索符合特定条件的邮件。
- **草稿管理**: 创建邮件草稿。
- **会话管理**: 获取邮件会话（Thread）信息。

#### 初始化参数
`GmailToolkit` 通常通过其 `from_gmail_api_wrapper` 类方法进行初始化。

| 参数 | 类型 | 描述 |
| :--- | :--- | :--- |
| `api_wrapper` | `GmailAPIWrapper` | 封装了 Google Gmail API 调用的工具类。 |

#### 获取工具
调用 `get_tools()` 方法将返回一个包含所有可用 Gmail 工具的列表。

```python
def get_tools(self) -> List[BaseTool]:
    """获取工具列表。"""
```

## 导出工具列表

该工具包提供的核心工具包括：
- `GmailCreateDraft`: 创建草稿。
- `GmailSendMessage`: 发送邮件。
- `GmailSearch`: 搜索邮件。
- `GmailGetMessage`: 获取邮件内容。
- `GmailListMessages`: 列出邮件。
- `GmailGetThread`: 获取邮件会话。

## 迁移建议

建议开发者直接从 `langchain_community` 导入：

```python
from langchain_community.agent_toolkits.gmail.toolkit import GmailToolkit
```

## 注意事项
1. **身份验证**: 使用此工具包之前，必须完成 Google Cloud Console 中的 OAuth2 认证配置，并下载 `credentials.json`。
2. **权限范围 (Scopes)**: 确保您的应用申请了必要的权限，例如 `https://www.googleapis.com/auth/gmail.modify`（用于读写操作）或 `https://www.googleapis.com/auth/gmail.readonly`。
3. **API 启用**: 必须在 Google Cloud 项目中显式启用 "Gmail API"。
