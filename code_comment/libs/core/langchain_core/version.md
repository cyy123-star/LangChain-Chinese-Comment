# version.py - 版本信息

- **最后更新时间**: 2026-01-29
- **对应源码版本**: LangChain Core v1.2.7

## 文件概述

`version.py` 定义了当前 `langchain-core` 软件包的版本号字符串。它是整个包版本控制的单一事实来源（Single Source of Truth）。

## 关键常量

### 1. VERSION
- **类型**: `str`
- **当前值**: `"1.2.7"`
- **作用**: 
    - 被 `setup.py` 或 `pyproject.toml` 用于构建发布包。
    - 被 `langchain_core.__init__` 导入并暴露为 `__version__`。
    - 被 `sys_info.py` 和 `env.py` 用于诊断和上报环境信息。

## 内部调用关系

该模块被 LangChain Core 内部几乎所有需要识别自身版本的组件所引用，例如：
- `env.py`: 获取运行时环境信息。
- `sys_info.py`: 打印系统诊断信息。

## 相关链接
- [langchain_core.env](env.md)
- [langchain_core.sys_info](sys_info.md)
