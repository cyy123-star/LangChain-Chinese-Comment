# Graph 详解

## 文件概述
`graph.py` 定义了 LangChain 内部用于表示 `Runnable` 结构的有向图（Directed Graph）。这个图结构主要用于可视化（如导出为 Mermaid、PNG 或 ASCII 艺术图）以及对复杂链条结构的内省（Introspection）。

通过将 `Runnable` 序列转换为 `Graph` 对象，开发者可以清晰地看到数据如何在不同的组件之间流转。

---

## 导入依赖
- `NamedTuple`, `TypedDict`, `Protocol`: 用于定义结构化数据类型。
- `Enum`: 用于定义枚举值（如绘图风格、绘图方法）。
- `dataclass`: 用于定义简洁的数据类。
- `Runnable`, `RunnableSerializable`: LangChain 的核心运行单元。
- `to_json_not_implemented`: 处理无法序列化的对象。

---

## 类与函数详解

### 核心数据结构

#### `Node` (NamedTuple)
代表图中的一个节点。
- `id`: 节点的唯一标识符（通常是 UUID 或易读的名称）。
- `name`: 节点的名称。
- `data`: 节点关联的数据，可以是 `Runnable` 对象或 Pydantic 模型。
- `metadata`: 关联的元数据。

#### `Edge` (NamedTuple)
代表图中连接两个节点的边。
- `source`: 源节点 ID。
- `target`: 目标节点 ID。
- `data`: 边上的额外数据（如标签）。
- `conditional`: 标记该边是否为条件分支（用于区分普通流转和条件路由）。

---

### `Graph` 类
图的核心容器，负责管理节点和边。

#### 核心方法
- **`add_node(data, id=None, metadata=None)`**: 向图中添加一个新节点。
- **`add_edge(source, target, data=None, conditional=False)`**: 在两个已存在的节点之间建立连接。
- **`extend(graph, prefix="")`**: 将另一个图的所有节点和边合并到当前图中，支持添加前缀以避免 ID 冲突。
- **`to_json()`**: 将图结构转换为 JSON 序列化格式。
- **可视化方法**:
  - `draw_ascii()`: 返回图的 ASCII 字符表示。
  - `draw_png(output_file_path)`: 将图渲染为 PNG 图片（依赖 PngDrawer）。
  - `draw_mermaid()`: 生成 Mermaid 语法的字符串，常用于 Markdown 或 Web 展示。
  - `draw_mermaid_png()`: 通过 Mermaid API 或 Pyppeteer 生成 PNG 图片。

---

## 使用示例

```python
from langchain_core.runnables.graph import Graph, Node

# 1. 创建图对象
g = Graph()

# 2. 添加节点
n1 = g.add_node(data=None, id="start", metadata={"label": "开始"})
n2 = g.add_node(data=None, id="process", metadata={"label": "处理"})
n3 = g.add_node(data=None, id="end", metadata={"label": "结束"})

# 3. 添加边
g.add_edge(n1, n2)
g.add_edge(n2, n3)

# 4. 打印 ASCII 图
g.print_ascii()

# 5. 获取 Mermaid 源码
mermaid_code = g.draw_mermaid()
print(mermaid_code)
```

---

## 注意事项
- **UUID 与可读 ID**：默认情况下，节点 ID 是自动生成的 UUID。为了生成更美观的可视化图，通常会调用 `reid()` 方法将 UUID 映射为基于 `Runnable` 名称的易读字符串。
- **循环引用**：该模块主要用于展示静态结构。如果链条中存在递归或复杂的循环引用，可视化可能会受到限制。
- **依赖库**：`draw_png` 需要安装 `pygraphviz` 等图形库；`draw_mermaid_png` 可能需要联网（使用 API 模式）或安装浏览器驱动（使用 Pyppeteer 模式）。

---

## 内部调用关系
- **与 `Runnable.get_graph()` 关系**：几乎所有的 `Runnable` 对象都实现了 `get_graph()` 方法，它们内部会根据自身的结构（如 `RunnableSequence` 的线性连接，`RunnableParallel` 的并行连接）调用 `Graph` 的方法来构建出代表自己的图。
- **子模块**：
  - `graph_ascii.py`: 负责 ASCII 渲染。
  - `graph_png.py`: 负责 PNG 渲染。
  - `graph_mermaid.py`: 负责 Mermaid 语法生成。

---

## 相关链接
- [Mermaid.js 官方文档](https://mermaid.js.org/)
- [源码引用: base.py](file:///d:/TraeProjects/langchain_code_comment/langchain_code/libs/core/langchain_core/runnables/base.py)

---
最后更新时间: 2026-01-29
对应源码版本: LangChain Core v1.2.7
