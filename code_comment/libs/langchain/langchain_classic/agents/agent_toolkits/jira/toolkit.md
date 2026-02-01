# libs\langchain\langchain_classic\agents\agent_toolkits\jira\toolkit.py

此文档提供了 `libs\langchain\langchain_classic\agents\agent_toolkits\jira\toolkit.py` 文件的详细中文注释。该模块定义了 Jira 工具集。

## 核心说明：动态重定向

该模块已被弃用，其核心功能已重定向至 `langchain_community.agent_toolkits.jira.toolkit`。

## 主要类

### `JiraToolkit`

`JiraToolkit` 封装了一系列用于与 Jira 任务管理系统交互的工具。它通过 `JiraAPIWrapper` 与 Jira API 进行底层通信。

#### 功能描述
- **Issue 操作**: 创建新 Issue、获取 Issue 详情、列出项目下的 Issue。
- **搜索能力**: 使用 JQL (Jira Query Language) 搜索 Issue。
- **评论管理**: 为 Issue 添加评论。
- **通用操作**: 通过 `JiraAction` 执行各种 Jira API 操作。

#### 初始化参数
`JiraToolkit` 通常通过其 `from_jira_api_wrapper` 类方法进行初始化。

| 参数 | 类型 | 描述 |
| :--- | :--- | :--- |
| `jira_api_wrapper` | `JiraAPIWrapper` | 封装了 Jira API 调用的工具类。 |

#### 获取工具
调用 `get_tools()` 方法将返回一个包含所有可用 Jira 工具的列表。

```python
def get_tools(self) -> List[BaseTool]:
    """获取工具列表。"""
```

## 导出工具列表

该工具包提供的核心工具包括：
- `JiraAction`: 执行通用的 Jira 操作。
- `search_issues`: 搜索问题。
- `create_issue`: 创建问题。
- `update_issue`: 更新问题。
- `add_comment`: 添加评论。

## 迁移建议

建议开发者直接从 `langchain_community` 导入：

```python
from langchain_community.agent_toolkits.jira.toolkit import JiraToolkit
```

## 注意事项
1. **认证配置**: 确保已设置 `JIRA_API_TOKEN`、`JIRA_USERNAME` 和 `JIRA_INSTANCE_URL` 环境变量，或在 `JiraAPIWrapper` 中直接提供。
2. **依赖库**: 此工具包依赖于 `atlassian-python-api` 库，请确保已安装。
3. **权限**: 执行操作的账户必须在 Jira 实例中拥有相应的项目权限。
