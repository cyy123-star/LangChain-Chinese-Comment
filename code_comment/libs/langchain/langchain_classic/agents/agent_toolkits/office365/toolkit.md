# libs\langchain\langchain_classic\agents\agent_toolkits\office365\toolkit.py

`office365/toolkit.py` 模块定义了 `O365Toolkit` 类，该类整合了多个用于操作 Microsoft 365 服务的工具。

## 核心类

### `O365Toolkit`

`O365Toolkit` 继承自 `BaseToolkit`，它通过封装 `O365` 库的各种操作，使代理能够与用户的 Office 365 账户进行交互。

#### 主要工具

该工具包通常包含以下核心工具：
- **`O365SearchEvents`**: 搜索日历事件，支持过滤条件。
- **`O365CreateEvent`**: 在指定日历中创建新事件。
- **`O365SearchEmails`**: 搜索电子邮件，可按发件人、日期等搜索。
- **`O365SendEmail`**: 发送电子邮件。
- **`O365CreateDraft`**: 创建邮件草稿而不立即发送。

#### 核心方法

##### `get_tools`

返回工具包中配置的所有工具列表。

```python
def get_tools(self) -> List[BaseTool]:
    """获取工具列表。"""
    return self.tools
```

## 动态导入机制

该文件使用了 `create_importer` 实现了动态属性查找。当开发者尝试从 `langchain_classic` 导入 `O365Toolkit` 时，系统会发出弃用警告，并自动重定向到 `langchain_community.agent_toolkits.office365.toolkit`。

```python
DEPRECATED_LOOKUP = {
    "O365Toolkit": "langchain_community.agent_toolkits.office365.toolkit",
}

# 动态属性查找逻辑
_import_attribute = create_importer(__package__, deprecated_lookups=DEPRECATED_LOOKUP)

def __getattr__(name: str) -> Any:
    """动态获取属性。"""
    return _import_attribute(name)
```

## 迁移指南

由于该模块已被弃用，建议直接从 `langchain_community` 导入。

```python
from langchain_community.agent_toolkits.office365.toolkit import O365Toolkit
```

## 注意事项

- **身份验证**: 使用前必须完成 Microsoft OAuth2 流程。通常需要 `client_id` 和 `client_secret`，并在首次运行时进行交互式授权。
- **权限范围 (Scopes)**: 确保在 Azure 门户中注册的应用程序具有正确的 API 权限，例如：
    - `Mail.ReadWrite`
    - `Mail.Send`
    - `Calendars.ReadWrite`
- **安全建议**: 严禁将 `client_secret` 硬编码在代码中。应使用环境变量或安全的服务端存储。
- **Token 管理**: `O365` 库会自动处理 Token 的存储和刷新，默认存储在本地 `o365_token.txt` 文件中。

