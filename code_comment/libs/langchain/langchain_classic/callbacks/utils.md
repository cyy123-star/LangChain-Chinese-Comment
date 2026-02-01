# libs\langchain\langchain_classic\callbacks\utils.py

`utils.py` 包含了一系列用于回调处理器的内部实用工具函数。

## 核心功能

### 1. 字典处理
- **flatten_dict**: 将嵌套的字典展平为单层字典，这在将日志导出到 CSV 或某些监控系统（如 W&B, Comet）时非常有用。

### 2. 依赖项动态加载
- **import_pandas**: 尝试导入 `pandas`。
- **import_spacy**: 尝试导入 `spacy`。
- **import_textstat**: 尝试导入 `textstat`。
这些函数允许回调处理器在运行时按需加载可选依赖，而不是在模块顶层强制要求安装。

### 3. 数据处理
- **hash_string**: 为字符串生成哈希值，常用于混淆敏感信息或生成唯一标识符。
- **load_json**: 安全地从文件或字符串加载 JSON 数据。

### 4. 基础类
- **BaseMetadataCallbackHandler**: 一个基础类，帮助处理器管理和注入元数据（Metadata）。

## 注意事项

- **内部使用**: 该模块中的大部分函数主要供 `langchain_community` 中的集成回调处理器（如 `WandbCallbackHandler`）内部使用。
- **迁移**: 这里的很多逻辑已经迁移到了 `langchain_community.callbacks.utils`。
