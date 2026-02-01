# libs\core\langchain_core\runnables\graph_mermaid.py

该模块提供了将 LangChain 的 Runnable 结构导出为 Mermaid 语法的功能，并支持通过 API 或本地浏览器渲染为图片。

## 文件概述

`graph_mermaid.py` 实现了将复杂的 Runnable 图结构转换为 Mermaid 流程图（Flowchart）语法的逻辑。它支持子图（Subgraphs）、节点样式、条件边以及通过 Mermaid.ink API 或 Pyppeteer 将 Mermaid 语法渲染为 PNG 图片。

## 导入依赖

| 依赖模块 | 作用 |
| :--- | :--- |
| `base64` | 用于对 Mermaid 语法进行编码，以便通过 API 传输。 |
| `urllib.parse` | 用于对 URL 参数进行编码。 |
| `yaml` | 用于生成 Mermaid 的 Frontmatter 配置。 |
| `requests` | 可选依赖。用于调用 Mermaid.ink API 进行远程渲染。 |
| `pyppeteer` | 可选依赖。用于通过无头浏览器在本地渲染 Mermaid 图表。 |
| `langchain_core.runnables.graph` | 导入图结构相关的枚举和类定义（如 `CurveStyle`, `MermaidDrawMethod`）。 |

## 函数详解

### `draw_mermaid(...) -> str`

- **功能描述**: 根据提供的节点和边数据生成 Mermaid 流程图语法。
- **参数说明**:
  | 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
  | :--- | :--- | :--- | :--- | :--- |
  | `nodes` | `dict[str, Node]` | - | 是 | 节点映射表。 |
  | `edges` | `list[Edge]` | - | 是 | 边列表。 |
  | `first_node` | `str \| None` | `None` | 否 | 入口节点 ID，将应用特定的样式。 |
  | `last_node` | `str \| None` | `None` | 否 | 出口节点 ID，将应用特定的样式。 |
  | `with_styles` | `bool` | `True` | 否 | 是否包含样式定义。 |
  | `curve_style` | `CurveStyle` | `LINEAR` | 否 | 边的弯曲样式（如 `linear`, `basis`）。 |
  | `node_styles` | `NodeStyles \| None` | `None` | 否 | 自定义节点颜色配置。 |
  | `wrap_label_n_words` | `int` | `9` | 否 | 边标签自动换行的单词数。 |
  | `frontmatter_config` | `dict \| None` | `None` | 否 | Mermaid 的 Frontmatter 配置（YAML 格式）。 |
- **核心逻辑**:
  1. 初始化 Mermaid 配置，包括 Frontmatter 和流程图方向（默认为 `TD`，即从上到下）。
  2. 将节点分类为普通节点和子图节点（基于节点 ID 中的冒号 `:`）。
  3. 定义节点渲染模板，为入口和出口节点分配特殊的 CSS 类。
  4. 递归处理子图结构，生成嵌套的 `subgraph` 语法。
  5. 处理边逻辑，包括条件边（虚线）和普通边（实线），并对长标签进行换行处理。
  6. 添加节点样式定义（`classDef`）。

### `draw_mermaid_png(...) -> bytes`

- **功能描述**: 将 Mermaid 语法渲染为 PNG 图片。
- **参数说明**:
  | 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
  | :--- | :--- | :--- | :--- | :--- |
  | `mermaid_syntax` | `str` | - | 是 | Mermaid 语法字符串。 |
  | `output_file_path` | `str \| None` | `None` | 否 | 图片保存路径。 |
  | `draw_method` | `MermaidDrawMethod` | `API` | 否 | 渲染方法：`API` (远程) 或 `PYPPETEER` (本地)。 |
  | `background_color` | `str \| None` | `"white"` | 否 | 背景颜色。 |
  | `max_retries` | `int` | `1` | 否 | API 请求的最大重试次数。 |

### 核心私有函数

- **`_to_safe_id(label: str) -> str`**: 将包含特殊字符的节点 ID 转换为 Mermaid 安全的 ID（使用十六进制转义）。
- **`_render_mermaid_using_api(...)`**: 调用 `https://mermaid.ink` 的接口进行在线渲染，支持指数退避重试。
- **`_render_mermaid_using_pyppeteer(...)`**: 在本地启动 Chromium 浏览器，通过 `mermaid.js` 渲染 SVG 并截图。

## 使用示例

```python
from langchain_core.runnables.graph import Graph, Node, Edge
from langchain_core.runnables.graph_mermaid import draw_mermaid

# 创建一个简单的图
nodes = {"a": Node(id="a", name="Input"), "b": Node(id="b", name="Process")}
edges = [Edge(source="a", target="b", data="send data")]

# 生成 Mermaid 语法
mermaid_code = draw_mermaid(nodes, edges)
print(mermaid_code)
```

## 注意事项

- **特殊字符**: 节点名称中如果包含 Mermaid 的特殊字符（如 `*_`），会被自动处理以确保正确渲染。
- **子图命名**: 不支持重复的子图名称，如果检测到重复会抛出 `ValueError`。
- **渲染依赖**:
    - `API` 模式需要网络连接和 `requests` 库。
    - `PYPPETEER` 模式需要安装 `pyppeteer` 及其依赖的 Chromium。
- **ID 转换**: 系统会自动将复杂的节点 ID 转换为安全格式，用户通常无需担心 ID 冲突。

## 内部调用关系

- `draw_mermaid` 内部通过递归函数 `add_subgraph` 构建层级结构。
- `draw_mermaid_png` 根据 `draw_method` 参数分发到 `_render_mermaid_using_api` 或 `_render_mermaid_using_pyppeteer`。

## 相关链接

- [Mermaid 官方文档](https://mermaid.js.org/)
- [Mermaid.ink 在线渲染服务](https://mermaid.ink/)

***

**最后更新时间**: 2026-01-29
**对应源码版本**: LangChain Core v1.2.7
