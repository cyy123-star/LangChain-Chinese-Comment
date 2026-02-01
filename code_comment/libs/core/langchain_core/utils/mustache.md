# mustache.py - Mustache 模板渲染工具

`mustache.py` 模块实现了一个轻量级的 Mustache 模板引擎。

## 文件概述

Mustache 是一种“无逻辑”的模板语法（Logic-less templates）。该模块允许开发者使用 `{{variable}}` 这种简洁的语法进行字符串替换，支持变量插值、逻辑块（如 if/for）以及反向块。

## 导入依赖

| 依赖模块 | 作用 |
| :--- | :--- |
| `re` | 用于解析和匹配模板标签。 |
| `typing` | 提供类型注解支持。 |

## 函数详解

### `render_mustache`

#### 功能描述
使用给定的上下文数据渲染 Mustache 模板字符串。

#### 参数说明
| 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `template` | `str` | - | 是 | 包含 Mustache 语法的模板字符串。 |
| `data` | `dict` | - | 是 | 用于替换模板变量的上下文字典。 |

#### 返回值解释
`str`: 渲染后的最终字符串。

#### 语法支持
- `{{var}}`: 变量替换。
- `{{#section}} ... {{/section}}`: 逻辑块。如果 `section` 为真或非空列表，内容将被渲染（对于列表会进行循环）。
- `{{^section}} ... {{/section}}`: 反向块。如果 `section` 为假或空列表，内容将被渲染。
- `{{! comment }}`: 注释，渲染时会被忽略。

---

## 核心算法流程
1. **词法分析**：扫描模板字符串，识别普通文本、标签、块开始、块结束等 Token。
2. **语法树构建**：将 Token 转换为嵌套的结构（树状结构），处理块的配对。
3. **递归渲染**：根据传入的 `data`，递归地处理每个节点：
   - 如果是文本，直接拼接。
   - 如果是变量，从 `data` 中查找值。
   - 如果是块，根据值的类型（列表、字典、布尔值）决定渲染次数和作用域。

---

## 使用示例

```python
from langchain_core.utils.mustache import render_mustache

template = "Hello, {{name}}! {{#items}}- {{.}}\n{{/items}}"
data = {
    "name": "LangChain",
    "items": ["Prompt", "Chain", "Agent"]
}

result = render_mustache(template, data)
print(result)
# 输出:
# Hello, LangChain! - Prompt
# - Chain
# - Agent
```

## 注意事项
- 与 Jinja2 等重型引擎相比，Mustache 不支持在模板中执行复杂的表达式或函数调用，这使得它更安全但也更受限。
- 变量查找支持点路径（如 `{{user.name}}`）。

## 相关链接
- [Mustache 官方规范](https://mustache.github.io/mustache.5.html)

---
**最后更新时间**: 2026-01-29
**对应源码版本**: LangChain Core v1.2.7
