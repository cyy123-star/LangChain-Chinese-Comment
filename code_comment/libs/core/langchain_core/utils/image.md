# image.py - 图像处理工具（安全性限制版）

`image.py` 模块原本用于图像数据的编码和转换，但由于安全原因，目前已移除核心功能，仅保留属性拦截逻辑。

## 文件概述

为了防止由于不安全的图像路径处理导致的本地文件泄露或 SSRF 攻击，LangChain 在该模块中禁用了 `encode_image` 和 `image_to_data_url` 函数。

## 导入依赖

| 依赖模块 | 作用 |
| :--- | :--- |
| `typing` | 提供 `Any` 类型注解。 |

## 核心逻辑

### 属性拦截 (`__getattr__`)

该模块通过重写 `__getattr__` 方法，在尝试访问已移除的函数时抛出显式的错误信息。

#### 拦截逻辑
1. 当代码尝试访问 `encode_image` 或 `image_to_data_url` 时。
2. 抛出 `ValueError`，提示该函数已因安全原因被移除。
3. 对于其他不存在的属性，正常抛出 `AttributeError`。

---

## 注意事项
- **安全警告**：不要尝试在旧版本中使用这两个函数来处理不受信任的本地文件路径。
- 如果需要将图像传递给模型，建议先手动将图像转换为 Base64 字符串，并使用多模态消息格式（如 `HumanMessage` 中的 `content` 列表）。

## 相关链接
- [LangChain 安全指南](https://python.langchain.com/docs/security)

---
**最后更新时间**: 2026-01-29
**对应源码版本**: LangChain Core v1.2.7
