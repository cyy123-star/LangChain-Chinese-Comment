# libs\core\langchain_core\runnables\graph_png.py

该模块提供了将 LangChain 的图结构（State Graph）渲染并保存为 PNG 图片的功能。它主要依赖于 `graphviz` 和 `pygraphviz` 库。

## 文件概述

`graph_png.py` 定义了 `PngDrawer` 类，用于将 `langchain_core.runnables.graph.Graph` 对象转换为可视化图形。它支持节点样式定制（如填充颜色、字体）、边样式（实线/虚线）、标签覆盖以及子图嵌套显示。

## 导入依赖

| 依赖模块 | 作用 |
| :--- | :--- |
| `itertools.groupby` | 用于根据节点前缀对节点进行分组，从而构建嵌套子图。 |
| `pygraphviz` | 核心依赖。用于生成和渲染 Graphviz 图形。 |
| `langchain_core.runnables.graph` | 导入 `Graph` 和 `LabelsDict` 类型定义。 |

## 类与函数详解

### PngDrawer 类

负责将图对象绘制为 PNG 格式的助手类。

#### `__init__(self, fontname: str | None = None, labels: LabelsDict | None = None)`
- **功能描述**: 初始化 PNG 绘制器。
- **参数说明**:
  | 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
  | :--- | :--- | :--- | :--- | :--- |
  | `fontname` | `str \| None` | `"arial"` | 否 | 标签使用的字体名称。 |
  | `labels` | `LabelsDict \| None` | - | 否 | 标签重写字典，用于自定义节点和边的显示名称。 |

#### `draw(self, graph: Graph, output_path: str | None = None) -> bytes | None`
- **功能描述**: 将给定的状态图绘制为 PNG。
- **参数说明**:
  | 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
  | :--- | :--- | :--- | :--- | :--- |
  | `graph` | `Graph` | - | 是 | 要绘制的图对象。 |
  | `output_path` | `str \| None` | `None` | 否 | 保存 PNG 的路径。如果为 `None`，则返回图片字节流。 |
- **核心逻辑**:
  1. 检查是否安装了 `pygraphviz`。
  2. 创建 `pgv.AGraph` 实例（有向图）。
  3. 调用 `add_nodes` 添加所有节点，并设置样式（黄色填充）。
  4. 调用 `add_edges` 添加所有边，并设置样式（普通边实线，条件边虚线）。
  5. 调用 `add_subgraph` 根据节点 ID 中的冒号分隔符递归构建嵌套子图。
  6. 调用 `update_styles` 突出显示入口节点（浅蓝色）和出口节点（橙色）。
  7. 使用 `dot` 布局引擎渲染并输出。

#### `add_subgraph(self, viz: Any, nodes: list[list[str]], parent_prefix: list[str] | None = None)`
- **核心逻辑**: 通过对节点 ID 进行拆分和排序，利用 `groupby` 找出具有共同前缀的节点组，并将它们放入 `cluster_` 前缀的子图中。这是一个递归过程，支持无限层级的嵌套。

## 使用示例

```python
from langchain_core.runnables.graph import Graph
from langchain_core.runnables.graph_png import PngDrawer

# 假设已经有一个 Graph 对象 state_graph
drawer = PngDrawer(fontname="Courier", labels={
    "nodes": {"__start__": "开始", "__end__": "结束"}
})

# 直接保存到文件
drawer.draw(state_graph, "my_graph.png")

# 或者获取字节流
# png_data = drawer.draw(state_graph)
```

## 注意事项

- **环境要求**: 系统必须安装 `graphviz` 软件，并且 Python 环境中需安装 `pygraphviz` 库。
- **样式固定**: 节点的填充颜色（黄色/浅蓝/橙色）和字体大小在代码中是硬编码的，目前不支持通过初始化参数完全自定义。
- **子图识别**: 只有 ID 中包含冒号（如 `parent:child`）的节点才会被识别并归类到子图中。

## 内部调用关系

- `draw` 是主入口，依次协调 `add_nodes`、`add_edges`、`add_subgraph` 和 `update_styles`。
- `add_node` 和 `add_edge` 分别被 `add_nodes` 和 `add_edges` 循环调用。
- `get_node_label` 和 `get_edge_label` 用于应用 `labels` 覆盖配置。

## 相关链接

- [Graphviz 官网](https://graphviz.org/)
- [Pygraphviz 文档](https://pygraphviz.github.io/)

***

**最后更新时间**: 2026-01-29
**对应源码版本**: LangChain Core v1.2.7
