# html.py - HTML 处理工具

`html.py` 模块提供了用于解析和提取 HTML 内容的基础工具。

## 文件概述

该文件目前主要用于从原始 HTML 文本中提取超链接。它使用了正则表达式来实现轻量级的提取逻辑，而无需依赖复杂的 HTML 解析库（如 BeautifulSoup）。

## 导入依赖

| 依赖模块 | 作用 |
| :--- | :--- |
| `re` | 提供正则表达式支持，用于匹配 HTML 标签。 |
| `typing` | 提供类型注解支持（`List`, `Optional`, `Union` 等）。 |

## 函数详解

### `find_all_links`

#### 功能描述
从给定的原始 HTML 字符串中提取所有的超链接（`href` 属性的值）。

#### 参数说明
| 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `raw_html` | `str` | - | 是 | 待解析的 HTML 字符串。 |
| `pattern` | `str \| re.Pattern \| None` | `None` | 否 | 自定义的链接匹配正则表达式。如果为 `None`，则使用默认模式。 |

#### 返回值解释
`list[str]`: 返回所有匹配到的链接列表。

#### 核心逻辑
1. 如果未提供 `pattern`，使用预定义的正则表达式：`r'<a\s+(?:[^>]*?\s+)?href="([^"]*)"'`。
2. 该正则表达式会匹配 `<a>` 标签，并捕获 `href` 属性中的双引号内容。
3. 使用 `re.findall` 提取所有捕获组的内容。

---

## 使用示例

```python
from langchain_core.utils.html import find_all_links

html_content = """
<html>
    <body>
        <a href="https://example.com">Example</a>
        <a class="nav" href="/about">About Us</a>
    </body>
</html>
"""

links = find_all_links(html_content)
print(links)  # 输出: ['https://example.com', '/about']
```

## 注意事项
- 默认的正则表达式仅支持提取由双引号包裹的 `href` 属性。
- 对于非标准的 HTML（例如单引号包裹或没有引号的 `href`），默认模式可能无法识别。
- 该工具不处理相对路径到绝对路径的转换，仅提取原始字符串。

## 相关链接
- [Python re 模块文档](https://docs.python.org/3/library/re.html)

---
**最后更新时间**: 2026-01-29
**对应源码版本**: LangChain Core v1.2.7
