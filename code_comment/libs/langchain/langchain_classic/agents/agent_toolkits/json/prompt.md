# libs\langchain\langchain_classic\agents\agent_toolkits\json\prompt.py

`json/prompt.py` 模块定义了 JSON 代理使用的默认提示词模板。

## 导出常量

- **JSON_PREFIX**: JSON 代理的系统提示词前缀，通常包含对代理角色的描述以及如何使用 JSON 工具的指令。
- **JSON_SUFFIX**: JSON 代理的系统提示词后缀，通常包含如何处理最终答案的说明。

## 动态导入机制

该文件使用了 `create_importer` 实现了动态属性查找。当开发者尝试从 `langchain_classic` 导入这些常量时，系统会发出弃用警告，并自动重定向到 `langchain_community.agent_toolkits.json.prompt`。

```python
DEPRECATED_LOOKUP = {
    "JSON_PREFIX": "langchain_community.agent_toolkits.json.prompt",
    "JSON_SUFFIX": "langchain_community.agent_toolkits.json.prompt",
}
```

## 迁移指南

建议直接从 `langchain_community` 导入：

```python
from langchain_community.agent_toolkits.json.prompt import JSON_PREFIX, JSON_SUFFIX
```
