import unittest
from typing import Any, List, Optional
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.language_models.llms import BaseLLM
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.outputs import ChatResult, ChatGeneration, LLMResult, Generation
from pydantic import Field
from langchain_core.prompts import (
    PromptTemplate, 
    ChatPromptTemplate, 
    FewShotPromptTemplate,
    FewShotChatMessagePromptTemplate
)
from langchain_core.runnables.history import RunnableWithMessageHistory

# 1. 定义 Mock LLM 类
class MockChatOpenAI(BaseChatModel):
    model_name: str = Field(default="gpt-4o-mini", alias="model")
    
    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[Any] = None,
        **kwargs: Any,
    ) -> ChatResult:
        content = "This is a mock response."
        message = AIMessage(content=content)
        generation = ChatGeneration(message=message)
        return ChatResult(generations=[generation])

    @property
    def _llm_type(self) -> str:
        return "mock-chat-openai"

class MockOpenAI(BaseLLM):
    def _generate(
        self,
        prompts: List[str],
        stop: Optional[List[str]] = None,
        run_manager: Optional[Any] = None,
        **kwargs: Any,
    ) -> LLMResult:
        generations = [[Generation(text="This is a mock LLM response.")]]
        return LLMResult(generations=generations)

    @property
    def _llm_type(self) -> str:
        return "mock-openai"

# 2. 模拟 ChatMessageHistory
class MockHistory:
    def __init__(self):
        self.messages = []
    def add_message(self, m):
        self.messages.append(m)
    def add_user_message(self, m):
        self.messages.append(HumanMessage(content=m))
    def add_ai_message(self, m):
        self.messages.append(AIMessage(content=m))
    def clear(self):
        self.messages = []
    def get_messages(self):
        return self.messages

# 3. 测试类
class TestCSDN1Snippets(unittest.TestCase):
    def setUp(self):
        self.llm = MockChatOpenAI()
        self.chat_llm = MockChatOpenAI()

    def test_prompt_template(self):
        """测试基础 PromptTemplate"""
        prompt = PromptTemplate.from_template("请为{product}写一句{style}风格的广告语，不超过{max_length}字。")
        formatted_str = prompt.format(product="智能手表", style="科技感", max_length=20)
        self.assertIn("智能手表", formatted_str)
        
        chain = prompt | self.llm
        response = chain.invoke({"product": "智能手表", "style": "科技感", "max_length": 20})
        self.assertEqual(response.content, "This is a mock response.")

    def test_prompt_composition(self):
        """测试 Prompt 组合 (+)"""
        role_prompt = PromptTemplate.from_template("你是一名{role}专家，擅长{domain}领域。")
        task_prompt = PromptTemplate.from_template("请针对以下背景执行任务：{task}")
        full_prompt = role_prompt + "\n\n" + task_prompt
        
        result = full_prompt.invoke({
            "role": "广告语撰写", 
            "domain": "消费电子", 
            "task": "为智能手表写一句科技感广告语"
        })
        self.assertIn("广告语撰写", result.text)
        self.assertIn("消费电子", result.text)

    def test_chat_prompt(self):
        """测试 ChatPromptTemplate"""
        chat_prompt = ChatPromptTemplate.from_messages([
            ("system", "你是一名专业的广告语撰写师，擅长创作简洁有力的广告语。"),
            ("human", "请为{product}写一句{style}风格的广告语，不超过{max_length}字。")
        ])
        
        chain = chat_prompt | self.chat_llm
        response = chain.invoke({
            "product": "智能手表", 
            "style": "科技感", 
            "max_length": 20
        })
        self.assertEqual(response.content, "This is a mock response.")

    def test_runnable_with_history(self):
        """测试多轮对话 (RunnableWithMessageHistory)"""
        chat_prompt = ChatPromptTemplate.from_messages([
            ("system", "你是一名友好的客服机器人，记住之前的对话内容。"),
            ("placeholder", "{chat_history}"),
            ("human", "{input}")
        ])
        
        store = {}
        def get_session_history(session_id: str):
            if session_id not in store:
                store[session_id] = MockHistory()
            return store[session_id]
        
        chain = chat_prompt | self.chat_llm
        with_message_history = RunnableWithMessageHistory(
            chain,
            get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
        )
        config = {"configurable": {"session_id": "user_123"}}
        response = with_message_history.invoke({"input": "你好"}, config=config)
        self.assertEqual(response.content, "This is a mock response.")

    def test_few_shot_prompt(self):
        """测试 FewShotPromptTemplate"""
        examples = [{"product": "无线耳机", "style": "科技感", "ad_copy": "自由聆听"}]
        example_prompt = PromptTemplate.from_template("产品：{product}\n风格：{style}\n广告语：{ad_copy}")
        few_shot_prompt = FewShotPromptTemplate(
            examples=examples,
            example_prompt=example_prompt,
            prefix="示例：",
            suffix="产品：{product}\n风格：{style}\n广告语：",
            input_variables=["product", "style"]
        )
        chain = few_shot_prompt | self.llm
        response = chain.invoke({"product": "智能手表", "style": "科技感"})
        self.assertEqual(response.content, "This is a mock response.")

    def test_few_shot_chat_prompt(self):
        """测试 FewShotChatMessagePromptTemplate"""
        examples = [
            {"input": "你好", "output": "您好，有什么可以帮您？"}
        ]
        example_prompt = ChatPromptTemplate.from_messages([
            ("human", "{input}"),
            ("ai", "{output}")
        ])
        few_shot_chat_prompt = FewShotChatMessagePromptTemplate(
            examples=examples,
            example_prompt=example_prompt
        )
        final_prompt = ChatPromptTemplate.from_messages([
            ("system", "你是一个助手"),
            few_shot_chat_prompt,
            ("human", "{input}")
        ])
        chain = final_prompt | self.chat_llm
        response = chain.invoke({"input": "我想买手表"})
        self.assertEqual(response.content, "This is a mock response.")

if __name__ == "__main__":
    unittest.main()
