# libs\langchain\langchain_classic\agents\agent_toolkits\github\toolkit.py

此文档提供了 `libs\langchain\langchain_classic\agents\agent_toolkits\github\toolkit.py` 文件的详细中文注释。该模块定义了 GitHub 工具集。

## 核心说明：动态重定向

该模块已被弃用，其核心功能已重定向至 `langchain_community.agent_toolkits.github.toolkit`。

## 主要类

### `GitHubToolkit`

`GitHubToolkit` 封装了一系列用于与 GitHub 仓库交互的工具。它通过 `GitHubAPIWrapper` 与 GitHub 进行底层通信。

#### 功能描述
- **Issue 管理**: 获取、列出和评论 Issue。
- **PR 管理**: 创建 Pull Request。
- **文件操作**: 创建、读取、更新和删除文件。
- **代码搜索**: 在仓库中搜索代码、Issue 和 PR。
- **评审请求**: 创建代码评审请求。

#### 初始化参数
`GitHubToolkit` 通常通过其 `from_github_api_wrapper` 类方法进行初始化。

| 参数 | 类型 | 描述 |
| :--- | :--- | :--- |
| `github_api_wrapper` | `GitHubAPIWrapper` | 封装了 GitHub API 调用的工具类。 |

#### 获取工具
调用 `get_tools()` 方法将返回一个包含所有可用 GitHub 工具的列表。

```python
def get_tools(self) -> List[BaseTool]:
    """获取工具列表。"""
```

## 导出工具列表

该工具包提供的核心工具包括：
- `GetIssue`: 获取单个 Issue。
- `GetIssues`: 列出多个 Issues。
- `CommentOnIssue`: 评论 Issue。
- `CreatePR`: 创建 PR。
- `UpdateFile`: 更新文件。
- `ReadFile`: 读取文件。
- `SearchCode`: 搜索代码。
- `CreateFile`: 创建文件。
- `DeleteFile`: 删除文件。
- `SearchIssuesAndPRs`: 搜索 Issue 和 PR。
- `CreateReviewRequest`: 创建评审请求。

## 迁移建议

建议开发者直接从 `langchain_community` 导入：

```python
from langchain_community.agent_toolkits.github.toolkit import GitHubToolkit
```

## 注意事项
1. **API 限制**: 请注意 GitHub API 的速率限制（Rate Limiting）。
2. **权限**: 确保提供的 GitHub Token 具有执行相关操作（如写权限、删除权限）的足够权限。
3. **安全性**: 妥善保管您的 GitHub 个人访问令牌（Personal Access Token）。
