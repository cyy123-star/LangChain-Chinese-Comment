# input.py - 终端输出工具

`input.py` 模块提供了一系列用于在终端中格式化和打印带颜色文本的实用工具。

## 文件概述

该模块主要用于调试和交互式场景，通过 ANSI 转义序列为控制台输出添加颜色、加粗和斜体效果。

## 导入依赖

| 依赖模块 | 作用 |
| :--- | :--- |
| `sys` | 用于访问标准输出（`stdout`）。 |
| `typing` | 提供类型注解支持（`Optional`）。 |

## 函数详解

### `get_colored_text`

#### 功能描述
将文本包裹在指定的颜色 ANSI 转义序列中。

#### 参数说明
| 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `text` | `str` | - | 是 | 要着色的文本内容。 |
| `color` | `str` | - | 是 | 颜色名称（如 "red", "green", "blue", "yellow" 等）。 |

#### 返回值解释
`str`: 带 ANSI 转义序列的字符串。

---

### `print_text`

#### 功能描述
向标准输出打印格式化的文本，支持颜色、加粗和斜体。

#### 参数说明
| 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `text` | `str` | - | 是 | 要打印的文本。 |
| `color` | `str \| None` | `None` | 否 | 文本颜色。 |
| `end` | `str` | `"\n"` | 否 | 打印结束符。 |

#### 核心逻辑
1. 如果指定了 `color`，调用 `get_colored_text`。
2. 使用 `sys.stdout.write` 进行打印。
3. 调用 `sys.stdout.flush` 确保内容立即显示。

---

### `get_bolded_text` / `get_italicized_text`

#### 功能描述
分别为文本添加加粗（Bold）和斜体（Italic）效果。

---

## 使用示例

```python
from langchain_core.utils.input import print_text

# 打印绿色文本
print_text("操作成功！", color="green")

# 打印警告
print_text("警告：发现异常。", color="yellow")
```

## 注意事项
- ANSI 转义序列在某些旧版 Windows 终端（如传统的 `cmd.exe`）中可能无法正常显示，但在大多数现代终端（VS Code, PowerShell, Linux Terminal）中表现良好。
- 过度使用颜色可能会降低日志的可读性。

## 相关链接
- [ANSI 转义码 (Wikipedia)](https://en.wikipedia.org/wiki/ANSI_escape_code)

---
**最后更新时间**: 2026-01-29
**对应源码版本**: LangChain Core v1.2.7
