# libs\core\langchain_core\runnables\graph_ascii.py

该模块提供了将有向无环图 (DAG) 绘制为 ASCII 文本的功能。它主要用于在终端或纯文本环境中可视化 LangChain 的 Runnable 结构。

## 文件概述

`graph_ascii.py` 实现了将图结构转换为 ASCII 字符画的逻辑。它适配自 `dvc` 项目的 `dagascii.py` 实现，利用 `grandalf` 库（如果已安装）进行图布局计算，并提供了一个简单的 ASCII 画布 (`AsciiCanvas`) 来渲染最终结果。

## 导入依赖

| 依赖模块 | 作用 |
| :--- | :--- |
| `math` | 用于计算画布尺寸（向上取整）。 |
| `os` | 用于获取系统换行符 (`os.linesep`)。 |
| `typing` | 提供类型注解支持。 |
| `grandalf` | 可选依赖。用于执行 Sugiyama 布局算法，计算节点位置。 |

## 类与函数详解

### VertexViewer 类

用于定义节点框的边界，供 `grandalf` 在构建图时参考。

- **HEIGHT**: 常量，定义节点框的高度（默认为 3，包括上下边框和一行文本）。

#### `__init__(self, name: str)`
- **功能描述**: 初始化节点的查看器。
- **参数说明**:
  | 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
  | :--- | :--- | :--- | :--- | :--- |
  | `name` | `str` | - | 是 | 节点的名称。 |

### AsciiCanvas 类

用于在 ASCII 环境中绘制点、线、文本和方框的画布类。

#### `__init__(self, cols: int, lines: int)`
- **功能描述**: 创建一个指定行列数的 ASCII 画布。
- **参数说明**:
  | 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
  | :--- | :--- | :--- | :--- | :--- |
  | `cols` | `int` | - | 是 | 画布的列数（宽度），必须 > 1。 |
  | `lines` | `int` | - | 是 | 画布的行数（高度），必须 > 1。 |

#### `draw(self) -> str`
- **功能描述**: 将画布内容合并为最终的字符串。
- **返回值**: `str`，包含换行符的 ASCII 字符画。

#### `point(self, x: int, y: int, char: str)`
- **功能描述**: 在画布的指定坐标处放置一个字符。

#### `line(self, x0: int, y0: int, x1: int, y1: int, char: str)`
- **功能描述**: 使用 Bresenham 算法的简化版在画布上绘制直线。

#### `text(self, x: int, y: int, text: str)`
- **功能描述**: 在指定位置水平绘制一段文本。

#### `box(self, x0: int, y0: int, width: int, height: int)`
- **功能描述**: 在画布上绘制一个带边框的方框，顶点使用 `+`，边框使用 `-` 和 `|`。

### 核心函数

#### `draw_ascii(vertices: Mapping[str, str], edges: Sequence[LangEdge]) -> str`
- **功能描述**: 构建 DAG 并将其绘制为 ASCII 字符串。
- **参数说明**:
  | 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
  | :--- | :--- | :--- | :--- | :--- |
  | `vertices` | `Mapping[str, str]` | - | 是 | 节点 ID 到显示文本的映射。 |
  | `edges` | `Sequence[LangEdge]` | - | 是 | 边列表，每个元素包含源节点、目标节点等信息。 |
- **核心逻辑**:
  1. 调用 `_build_sugiyama_layout` 使用 `grandalf` 计算节点的布局位置。
  2. 计算所有节点和边的坐标范围，确定画布大小。
  3. 创建 `AsciiCanvas` 实例。
  4. 遍历所有边，在画布上绘制点线（如果是有条件的边使用 `.`，否则使用 `*`）。
  5. 遍历所有节点，在画布上绘制方框和节点文本。
  6. 返回画布的字符串表示。

## 使用示例

```python
from langchain_core.runnables.graph_ascii import draw_ascii

# 定义节点
vertices = {"1": "Start", "2": "Process", "3": "End"}
# 定义边 (source, target, data, conditional)
edges = [
    ("1", "2", None, False),
    ("2", "3", None, False)
]

print(draw_ascii(vertices, edges))
```

输出效果示例：
```txt
 +-------+
 | Start |
 +-------+
     *
     *
 +---------+
 | Process |
 +---------+
     *
     *
  +-----+
  | End |
  +-----+
```

## 注意事项

- **环境要求**: 必须安装 `grandalf` 库才能进行布局计算（`pip install grandalf`）。
- **坐标偏移**: 布局算法产生的坐标可能为负数，函数内部会自动进行平移处理，确保所有内容都在画布的可视区域内。
- **性能**: 对于非常庞大的图，ASCII 渲染可能会产生非常长的字符串，且布局计算时间会增加。

## 内部调用关系

- `draw_ascii` 调用 `_build_sugiyama_layout` 获取布局信息。
- `_build_sugiyama_layout` 内部实例化 `grandalf.graphs.Graph` 并应用 `SugiyamaLayout`。
- `draw_ascii` 使用 `AsciiCanvas` 进行具体的字符填充。

## 相关链接

- [grandalf GitHub](https://github.com/mvallet91/grandalf)
- [dvc dagascii 实现参考](https://github.com/iterative/dvc/blob/main/dvc/dagascii.py)

***

**最后更新时间**: 2026-01-29
**对应源码版本**: LangChain Core v1.2.7
