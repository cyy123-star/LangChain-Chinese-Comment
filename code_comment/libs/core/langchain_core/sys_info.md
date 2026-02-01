# sys_info.py - 系统与包信息调试工具

- **最后更新时间**: 2026-01-29
- **对应源码版本**: LangChain Core v1.2.7

## 文件概述

`sys_info.py` 是一个实用的调试工具模块，用于打印当前运行环境的系统信息和 LangChain 相关包的版本信息。它能够自动识别已安装的 LangChain 系列包（如 `langchain-core`, `langchain-community`, `langgraph` 等）及其子依赖，为开发者排查版本兼容性问题或报告 Bug 提供标准化的环境快照。

## 导入依赖

| 依赖模块 | 作用 |
| :--- | :--- |
| `pkgutil` | 用于遍历已安装的 Python 模块，查找以 "langchain" 或 "langgraph" 开头的包。 |
| `platform` | 获取操作系统名称、版本等底层平台信息。 |
| `re` | 使用正则表达式解析依赖包名称中的版本约束。 |
| `sys` | 获取 Python 解释器版本及路径信息。 |
| `importlib.metadata` | 获取已安装包的元数据，如版本号和依赖列表。 |
| `importlib.util` | 检查特定包是否已安装在当前环境中。 |

## 类与函数详解

### `print_sys_info` (函数)

**功能描述**：
打印详细的系统和包信息到控制台。输出分为三部分：系统信息（OS、Python版本）、已安装的 LangChain 包信息（包名、版本）以及可选的未安装包提示。

**参数说明**：

| 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `additional_pkgs` | `Sequence[str]` | `()` | 否 | 除内置列表外，用户想要检查的其他额外包名。 |

**返回值解释**：
无（直接打印到 stdout）。

**核心逻辑**：
1. **系统信息获取**：使用 `platform` 和 `sys` 模块获取 OS 和 Python 环境的基本参数。
2. **包搜索**：利用 `pkgutil.iter_modules()` 动态搜索当前 Python 路径下所有以 `langchain` 和 `langgraph` 开头的包。
3. **包排序**：将核心包（如 `langchain_core`）排在输出的最前面。
4. **版本查询**：对每个找到的包，使用 `importlib.metadata.version` 获取其版本号。
5. **依赖分析**：通过 `_get_sub_deps` 函数分析这些包的公共依赖项（如 `httpx`, `pydantic` 等）。

**使用示例**：

```python
from langchain_core.sys_info import print_sys_info

# 打印默认的系统信息
print_sys_info()

# 包含额外的包进行检查
print_sys_info(additional_pkgs=["numpy", "pandas"])
```

**注意事项**：
- 该函数会尝试查找所有可能的 LangChain 扩展包，因此输出可能较长。
- 对于未安装的包，它会将其归类到 "Optional packages not installed" 部分。
- 依赖于 `importlib.metadata`，在不同 Python 版本中行为可能略有差异（Python 3.8+ 推荐使用）。

---

### `_get_sub_deps` (内部函数)

**功能描述**：
分析指定包列表的子依赖项，并提取非 LangChain 家族的通用依赖（如网络库、解析库等）。

**参数说明**：

| 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `packages` | `Sequence[str]` | 无 | 是 | 需要分析依赖的包名序列。 |

**返回值解释**：
`list[str]`：按字母顺序排序的子依赖包名列表。

## 内部调用关系

- `print_sys_info` 内部调用 `_get_sub_deps` 来完善其 "Other Dependencies" 部分的输出。
- 使用 `pkgutil` 动态扫描本地安装情况，而不是硬编码包名。

## 相关链接

- [Python importlib.metadata 文档](https://docs.python.org/3/library/importlib.metadata.html)
- [LangChain 官方安装指南](https://python.langchain.com/docs/get_started/installation)
