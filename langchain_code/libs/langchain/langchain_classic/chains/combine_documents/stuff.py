"""Chain that combines documents by stuffing into context."""

from typing import Any

from langchain_core._api import deprecated
from langchain_core.callbacks import Callbacks
from langchain_core.documents import Document
from langchain_core.language_models import LanguageModelLike
from langchain_core.output_parsers import BaseOutputParser, StrOutputParser
from langchain_core.prompts import BasePromptTemplate, format_document
from langchain_core.runnables import Runnable, RunnablePassthrough
from pydantic import ConfigDict, Field, model_validator
from typing_extensions import override

from langchain_classic.chains.combine_documents.base import (
    DEFAULT_DOCUMENT_PROMPT,
    DEFAULT_DOCUMENT_SEPARATOR,
    DOCUMENTS_KEY,
    BaseCombineDocumentsChain,
    _validate_prompt,
)
from langchain_classic.chains.llm import LLMChain


def create_stuff_documents_chain(
    llm: LanguageModelLike,
    prompt: BasePromptTemplate,
    *,
    output_parser: BaseOutputParser | None = None,
    document_prompt: BasePromptTemplate | None = None,
    document_separator: str = DEFAULT_DOCUMENT_SEPARATOR,
    document_variable_name: str = DOCUMENTS_KEY,
) -> Runnable[dict[str, Any], Any]:
    r"""创建一个用于将文档列表传递给模型的链。

    参数:
        llm: 语言模型。
        prompt: 提示词模板。必须包含输入变量 `"context"`（通过设置 document_variable 覆盖），该变量将用于传递格式化后的文档。
        output_parser: 输出解析器。默认为 `StrOutputParser`。
        document_prompt: 用于将每个文档格式化为字符串的提示词。输入变量可以是 "page_content" 或所有文档中存在的任何元数据键。
            "page_content" 将自动获取 `Document.page_content`，所有其他输入变量将自动从 `Document.metadata` 字典中获取。
            默认为仅包含 `Document.page_content` 的提示词。
        document_separator: 格式化后的文档字符串之间使用的字符串分隔符。
        document_variable_name: 用于提示词中格式化文档的变量名。默认为 `"context"`。

    返回:
        一个 LCEL Runnable。输入是一个字典，必须包含一个映射到 `list[Document]` 的 `"context"` 键，以及提示词中预期的任何其他输入变量。
        `Runnable` 的返回类型取决于所使用的 `output_parser`。

    示例:
        ```python
        # pip install -U langchain langchain-openai

        from langchain_openai import ChatOpenAI
        from langchain_core.documents import Document
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_classic.chains.combine_documents import (
            create_stuff_documents_chain,
        )

        prompt = ChatPromptTemplate.from_messages(
            [("system", "所有人最喜欢的颜色是什么：\n\n{context}")]
        )
        model = ChatOpenAI(model="gpt-3.5-turbo")
        chain = create_stuff_documents_chain(model, prompt)

        docs = [
            Document(page_content="Jesse 喜欢红色但不喜欢黄色"),
            Document(
                page_content="Jamal 喜欢绿色，但不如他喜欢橙色那样喜欢"
            ),
        ]

        chain.invoke({"context": docs})
        ```
    """
    _validate_prompt(prompt, document_variable_name)
    _document_prompt = document_prompt or DEFAULT_DOCUMENT_PROMPT
    _output_parser = output_parser or StrOutputParser()

    def format_docs(inputs: dict) -> str:
        return document_separator.join(
            format_document(doc, _document_prompt)
            for doc in inputs[document_variable_name]
        )

    return (
        RunnablePassthrough.assign(**{document_variable_name: format_docs}).with_config(
            run_name="format_inputs",
        )
        | prompt
        | llm
        | _output_parser
    ).with_config(run_name="stuff_documents_chain")


@deprecated(
    since="0.2.13",
    removal="1.0",
    message=(
        "This class is deprecated. Use the `create_stuff_documents_chain` constructor "
        "instead. See migration guide here: "
        "https://python.langchain.com/docs/versions/migrating_chains/stuff_docs_chain/"
    ),
)
class StuffDocumentsChain(BaseCombineDocumentsChain):
    """通过将文档填充到上下文来合并文档的链。

    此链接收文档列表，并首先将它们合并为单个字符串。
    它通过使用 `document_prompt` 将每个文档格式化为字符串，然后使用 `document_separator` 将它们连接在一起来实现。
    然后，它将该新字符串添加到输入中，变量名由 `document_variable_name` 设置。
    这些输入随后被传递给 `llm_chain`。

    注意：此类已被弃用，建议使用 `create_stuff_documents_chain`。

    示例:
        ```python
        from langchain_classic.chains import StuffDocumentsChain, LLMChain
        from langchain_core.prompts import PromptTemplate
        from langchain_openai import OpenAI

        # 这控制每个文档的格式。具体来说，它将被传递给 `format_document`。
        document_prompt = PromptTemplate(
            input_variables=["page_content"], template="{page_content}"
        )
        document_variable_name = "context"
        model = OpenAI()
        # 这里的提示词应将 `document_variable_name` 作为输入变量
        prompt = PromptTemplate.from_template("总结以下内容：{context}")
        llm_chain = LLMChain(llm=model, prompt=prompt)
        chain = StuffDocumentsChain(
            llm_chain=llm_chain,
            document_prompt=document_prompt,
            document_variable_name=document_variable_name,
        )
        ```
    """

    llm_chain: LLMChain
    """调用格式化后的文档字符串以及任何其他输入的 LLM 链。"""
    document_prompt: BasePromptTemplate = Field(
        default_factory=lambda: DEFAULT_DOCUMENT_PROMPT,
    )
    """用于格式化每个文档的提示词，传递给 `format_document`。"""
    document_variable_name: str
    """llm_chain 中用于放置文档的变量名。如果 llm_chain 中只有一个变量，则无需提供。"""
    document_separator: str = "\n\n"
    """用于连接格式化后的文档的字符串分隔符。"""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra="forbid",
    )

    @model_validator(mode="before")
    @classmethod
    def get_default_document_variable_name(cls, values: dict) -> Any:
        """如果未提供，获取默认文档变量名。

        如果 llm_chain.prompt 中只存在一个变量，我们可以推断格式化后的文档应使用此变量名传递。
        """
        llm_chain_variables = values["llm_chain"].prompt.input_variables
        if "document_variable_name" not in values:
            if len(llm_chain_variables) == 1:
                values["document_variable_name"] = llm_chain_variables[0]
            else:
                msg = (
                    "document_variable_name must be provided if there are "
                    "multiple llm_chain_variables"
                )
                raise ValueError(msg)
        elif values["document_variable_name"] not in llm_chain_variables:
            msg = (
                f"document_variable_name {values['document_variable_name']} was "
                f"not found in llm_chain input_variables: {llm_chain_variables}"
            )
            raise ValueError(msg)
        return values

    @property
    @override
    def input_keys(self) -> list[str]:
        """期望的输入键。"""
        extra_keys = [
            k for k in self.llm_chain.input_keys if k != self.document_variable_name
        ]
        return super().input_keys + extra_keys

    def _get_inputs(self, docs: list[Document], **kwargs: Any) -> dict:
        """从参数和文档构建输入。

        格式化并将所有文档连接成一个名为 `self.document_variable_name` 的输入。
        同时从 **kwargs 中提取任何其他变量。

        参数:
            docs: 要格式化并连接为单个输入的文档列表
            **kwargs: 链的其他输入，将从中提取任何其他必需的参数。

        返回:
            LLMChain 的输入字典
        """
        # 根据提示词格式化每个文档
        doc_strings = [format_document(doc, self.document_prompt) for doc in docs]
        # 将文档连接起来放入提示词。
        inputs = {
            k: v
            for k, v in kwargs.items()
            if k in self.llm_chain.prompt.input_variables
        }
        inputs[self.document_variable_name] = self.document_separator.join(doc_strings)
        return inputs

    def prompt_length(self, docs: list[Document], **kwargs: Any) -> int | None:
        """返回给定文档列表生成的提示词长度。

        调用者可以使用此方法来确定传入文档列表是否会超过特定的提示词长度限制。
        这在确保提示词大小保持在特定上下文限制内时非常有用。

        参数:
            docs: 用于计算总提示词长度的文档列表。
            **kwargs: 用于获取 LLMChain 输入的其他参数。

        返回:
            如果该方法不依赖于提示词长度，则返回 None，否则返回以 token 为单位的提示词长度。
        """
        inputs = self._get_inputs(docs, **kwargs)
        prompt = self.llm_chain.prompt.format(**inputs)
        return self.llm_chain._get_num_tokens(prompt)  # noqa: SLF001

    def combine_docs(
        self,
        docs: list[Document],
        callbacks: Callbacks = None,
        **kwargs: Any,
    ) -> tuple[str, dict]:
        """将所有文档填充到一个提示词中并传递给 LLM。

        参数:
            docs: 要连接成单个变量的文档列表
            callbacks: 可选的回调函数
            **kwargs: 用于获取 LLMChain 输入的其他参数。

        返回:
            返回的第一个元素是单个字符串输出。第二个元素是其他要返回的键的字典。
        """
        inputs = self._get_inputs(docs, **kwargs)
        # 调用 LLM 的 predict。
        return self.llm_chain.predict(callbacks=callbacks, **inputs), {}

    async def acombine_docs(
        self,
        docs: list[Document],
        callbacks: Callbacks = None,
        **kwargs: Any,
    ) -> tuple[str, dict]:
        """异步将所有文档填充到一个提示词中并传递给 LLM。

        参数:
            docs: 要连接成单个变量的文档列表
            callbacks: 可选的回调函数
            **kwargs: 用于获取 LLMChain 输入的其他参数。

        返回:
            返回的第一个元素是单个字符串输出。第二个元素是其他要返回的键的字典。
        """
        inputs = self._get_inputs(docs, **kwargs)
        # 调用 LLM 的 predict。
        return await self.llm_chain.apredict(callbacks=callbacks, **inputs), {}

    @property
    def _chain_type(self) -> str:
        return "stuff_documents_chain"
