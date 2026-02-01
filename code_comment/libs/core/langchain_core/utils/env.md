# env.py - 环境配置工具

`env.py` 模块提供了一系列用于读取和验证环境变量及字典配置的实用函数。

## 文件概述

在 LangChain 中，许多配置（如 API 密钥）可以从初始化参数中获取，也可以从环境变量中获取。该模块统一了这种“优先从参数读，其次从环境读”的逻辑。

## 导入依赖

| 依赖模块 | 作用 |
| :--- | :--- |
| `os` | 用于访问操作系统的环境变量。 |
| `typing` | 提供类型注解支持（`Any`, `Optional` 等）。 |

## 函数详解

### `get_from_dict_or_env`

#### 功能描述
从字典中获取指定键的值，如果不存在，则尝试从环境变量中获取。

#### 参数说明
| 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `data` | `dict[str, Any]` | - | 是 | 输入的配置字典。 |
| `key` | `str \| list[str]` | - | 是 | 字典中的键（支持列表形式尝试多个键）。 |
| `env_key` | `str` | - | 是 | 对应的环境变量名称。 |
| `default` | `str \| None` | `None` | 否 | 如果两者都未找到时的默认值。 |

#### 返回值解释
返回查找到的字符串值。

#### 核心逻辑
1. 首先检查 `key` 是否在 `data` 字典中（如果是列表，则依次检查）。
2. 如果找到且不为 `None`，直接返回。
3. 如果字典中没有，调用 `os.getenv(env_key)`。
4. 如果环境变量中也没有，返回 `default`。
5. 如果最终结果仍为 `None`，通常会根据调用方的逻辑抛出异常。

---

### `env_var_is_set`

#### 功能描述
检查特定的环境变量是否被设置为“真”值（如 `true`, `1`, `yes`）。

#### 参数说明
| 参数名 | 类型 | 默认值 | 必填 | 详细用途 |
| :--- | :--- | :--- | :--- | :--- |
| `env_var` | `str` | - | 是 | 要检查的环境变量名。 |

#### 返回值解释
`bool`: 如果环境变量存在且其值在 `{"1", "true", "yes"}` 中，返回 `True`；否则返回 `False`。

---

## 使用示例

```python
import os
from langchain_core.utils.env import get_from_dict_or_env

# 模拟配置
config = {"api_key": "my_secret_key"}

# 从字典获取
val = get_from_dict_or_env(config, "api_key", "OPENAI_API_KEY")
print(val)  # 输出: my_secret_key

# 字典中没有，从环境获取
os.environ["OTHER_API_KEY"] = "env_secret"
val2 = get_from_dict_or_env({}, "other_key", "OTHER_API_KEY")
print(val2)  # 输出: env_secret
```

## 注意事项
- `get_from_dict_or_env` 在找不到值时不会主动抛出异常，通常需要调用方判断返回值是否为 `None`。
- `env_var_is_set` 对大小写敏感（通常环境变量值推荐小写）。

## 相关链接
- [Python os.environ 文档](https://docs.python.org/3/library/os.html#os.environ)

---
**最后更新时间**: 2026-01-29
**对应源码版本**: LangChain Core v1.2.7
