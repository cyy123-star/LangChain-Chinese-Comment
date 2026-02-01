# Redaction Utilities (敏感信息脱敏工具)

`_redaction.py` 提供了中间件系统中通用的敏感信息（PII）检测和脱敏处理工具。它主要用于在代理输出返回给模型之前，自动过滤或隐藏电子邮件、信用卡号、IP 地址等敏感数据。

## 核心功能
- **多类型检测**: 内置了对常见敏感数据类型的正则检测及校验逻辑（如信用卡号的 Luhn 算法校验）。
- **多种脱敏策略**: 支持对检测到的内容进行屏蔽、掩码、哈希或直接阻塞。
- **可扩展性**: 允许用户通过正则表达式或自定义函数定义新的检测器。

## 脱敏策略 (`RedactionStrategy`)

| 策略 | 说明 | 示例 |
| :--- | :--- | :--- |
| `redact` | 使用预定义的标签替换 | `[REDACTED_EMAIL]` |
| `mask` | 保留部分特征，隐藏大部分内容 | `user@****.com` |
| `hash` | 使用 SHA-256 哈希值的前 8 位替换 | `<email_hash:a1b2c3d4>` |
| `block` | 发现敏感信息时直接抛出异常 | 抛出 `PIIDetectionError` |

## 内置检测器

- **`email`**: 检测标准的电子邮件地址。
- **`credit_card`**: 检测 13-19 位的信用卡号，并使用 **Luhn 算法** 验证其有效性，以减少误报。
- **`ip`**: 检测 IPv4 和 IPv6 地址。
- **`mac_address`**: 检测标准的 MAC 地址格式。
- **`url`**: 检测 http/https 链接以及常见的域名格式。

## 核心数据结构

### 1. `PIIMatch`
记录检测到的敏感信息位置和类型：
- `type`: PII 类型（如 `"email"`）。
- `value`: 原始文本内容。
- `start`/`end`: 在字符串中的起止索引。

### 2. `RedactionRule`
用于配置如何处理特定的 PII 类型。
- `pii_type`: 要处理的类型。
- `strategy`: 使用的脱敏策略。
- `detector`: 可选的自定义检测器（函数或正则）。

### 3. `ResolvedRedactionRule`
已解析的规则，包含了可执行的检测函数。通过调用 `apply(content)` 方法对文本执行检测和脱敏。

## 异常处理
- **`PIIDetectionError`**: 当策略设置为 `block` 且检测到敏感信息时抛出。

## 使用场景
主要被 `ShellToolMiddleware` 和 `PIIMiddleware` 使用，确保代理在执行 Shell 命令或进行对话时，不会将宿主机的敏感环境信息或用户隐私泄露给 LLM。
