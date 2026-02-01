# interactive_env.py - 交互式环境公用程序

## 文件概述

`interactive_env.py` 是 LangChain 提供的一个小巧的工具模块，主要用于检测当前的 Python 运行环境是否为交互式环境（如 IPython 或 Jupyter Notebook）。这在某些需要根据运行环境调整输出行为或显示方式的场景中非常有用。

## 导入依赖

| 依赖模块 | 作用 |
| :--- | :--- |
| `sys` | 用于访问与 Python 解释器紧密相关的变量和函数，此处用于检查 `ps2` 属性。 |

## 函数详解

### 1. is_interactive_env
- **功能描述**: 判断当前程序是否在 IPython 或 Jupyter 等交互式环境中运行。
- **参数说明**: 无参数。
- **返回值**: `bool`。如果处于交互式环境则返回 `True`，否则返回 `False`。
- **核心逻辑**:
    - 通过检查 `sys` 模块是否具有 `ps2` 属性来判断。
    - `sys.ps2` 通常只在交互式解释器中定义，代表次级提示符（默认为 `... `）。
- **使用示例**:
    ```python
    from langchain_core.utils.interactive_env import is_interactive_env

    if is_interactive_env():
        print("正在交互式环境中运行（如 Jupyter）")
    else:
        print("正在标准脚本环境中运行")
    ```

## 内部调用关系

该模块是一个独立的工具函数，被 LangChain 内部其他需要环境感知的组件调用。

## 相关链接
- [Python sys 模块文档](https://docs.python.org/3/library/sys.html#sys.ps2)

---
**最后更新时间**: 2026-01-29
**对应源码版本**: LangChain Core v1.2.7
