# langchain_text_splitters.python

`python.py` 专门用于 Python 源代码的切分。它确保代码块在切分时尽可能保留类、函数和逻辑结构的完整性。

## **文件概述**
该文件定义了 `PythonCodeTextSplitter` 类。它实质上是 `RecursiveCharacterTextSplitter` 的一个特化版本，预置了针对 Python 语法优化的分隔符列表。

## **导入依赖**
- `langchain_text_splitters.base.Language`: 包含 Python 语言标识。
- `langchain_text_splitters.character.RecursiveCharacterTextSplitter`: 递归字符切分器基类。

## **类与函数详解**

### **PythonCodeTextSplitter (类)**
**功能描述**：尝试沿着 Python 语法边界（如类定义、函数定义、缩进块等）切分文本。

#### **构造函数 `__init__`**
- **参数**: 接收与 `RecursiveCharacterTextSplitter` 相同的参数（如 `chunk_size`, `chunk_overlap`）。
- **逻辑**: 自动从 `Language.PYTHON` 获取推荐的分隔符：
    1. `\nclass ` (类定义)
    2. `\ndef ` (函数定义)
    3. `\n\tdef ` (类方法)
    4. `\n  def ` (空格缩进的方法)
    5. `\n\n` (段落)
    6. `\n` (换行)
    7. ` ` (空格)
    8. `""` (字符)

## **核心逻辑解析**
1. **语法感知**：相比于普通的文本切分，`PythonCodeTextSplitter` 优先考虑代码的逻辑边界。例如，它会尽量避免在一个函数的中间进行切分，除非函数本身超过了 `chunk_size`。
2. **递归尝试**：如果一个类定义太长，它会尝试在函数定义处切分；如果函数还太长，则在段落或换行处切分。

## **使用示例**
```python
from langchain_text_splitters import PythonCodeTextSplitter

python_code = """
class MyBot:
    def __init__(self, name):
        self.name = name

    def say_hello(self):
        print(f"Hello, I am {self.name}")

def main():
    bot = MyBot("LangChain")
    bot.say_hello()

if __name__ == "__main__":
    main()
"""

splitter = PythonCodeTextSplitter(chunk_size=100, chunk_overlap=0)
docs = splitter.create_documents([python_code])

for i, doc in enumerate(docs):
    print(f"--- Chunk {i} ---")
    print(doc.page_content)
```

## **注意事项**
- 虽然该切分器能识别语法关键字，但它本质上还是基于正则表达式的字符串操作，并不进行真正的抽象语法树（AST）解析。
- 对于包含大量嵌套逻辑的复杂文件，建议适当调大 `chunk_size` 以保持代码的可读性。

## **相关链接**
- [RecursiveCharacterTextSplitter 基类](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/text-splitters/langchain_text_splitters/character.md#2-recursivecharactertextsplitter-类)
- [Language 枚举定义](file:///d:/TraeProjects/langchain_code_comment/code_comment/libs/text-splitters/langchain_text_splitters/base.md#3-language-枚举类)
