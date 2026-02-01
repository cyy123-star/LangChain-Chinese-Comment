# File Search Middleware (文件搜索中间件)

`file_search.py` 实现了 `FilesystemFileSearchMiddleware`，它为代理提供了在本地文件系统中进行高效文件路径匹配（Glob）和内容搜索（Grep）的能力。

## 核心功能 (Core Features)

1.  **Glob 搜索**: 支持标准 Glob 模式（如 `**/*.js`），快速查找文件。
2.  **Grep 搜索**: 支持正则表达式搜索文件内容，性能优化的实现。
3.  **多后端支持**: Grep 搜索优先使用 `ripgrep` (rg)，如果不可用则回退到 Python 原生实现。
4.  **安全限制**: 支持设置根路径 (`root_path`) 限制搜索范围，并可设置最大文件搜索大小。
5.  **虚拟路径映射**: 自动将本地绝对路径映射为相对于根路径的虚拟路径（以 `/` 开头）。

## 核心组件 (Core Components)

### `FilesystemFileSearchMiddleware`

| 参数 | 类型 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- |
| `root_path` | `str` | - | 搜索的根目录，代理只能访问此目录下的文件。 |
| `use_ripgrep` | `bool` | `True` | 是否尝试使用 `ripgrep` 提升 Grep 速度。 |
| `max_file_size_mb` | `int` | `10` | 单个文件搜索的最大大小限制。 |

## 注入的工具 (Injected Tools)

中间件会自动向代理注入以下两个工具：

### 1. `glob_search`
- **功能**: 按路径模式匹配文件。
- **参数**:
    - `pattern`: Glob 模式（如 `src/**/*.ts`）。
    - `path`: 起始搜索目录（相对于根路径）。
- **返回**: 按修改时间排序的文件路径列表。

### 2. `grep_search`
- **功能**: 在文件内容中搜索正则模式。
- **参数**:
    - `pattern`: 正则表达式。
    - `path`: 起始搜索目录。
    - `include`: 文件名过滤模式（如 `*.py`）。
    - `output_mode`: 输出模式 (`files_with_matches`, `content`, `count`)。

## 使用示例 (Example Usage)

```python
from langchain.agents.middleware import FilesystemFileSearchMiddleware

# 限制代理只能搜索 /project 目录下的文件
search_mw = FilesystemFileSearchMiddleware(root_path="/project")

agent = create_agent(model, tools=[], middleware=[search_mw])
```

