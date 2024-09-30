# services/chatbot_service.py
from ..models.chat_message import ChatMessage

# from openai import OpenAI
import os
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from ..extensions import db as alchemy_db  # Import your Flask SQLAlchemy db
from .. import mysql_db  # Import the db instances
from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

# from langchain.chains import ConversationChain, LLMChain
# from langchain.memory import ConversationBufferMemory
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage
from langchain_core.chat_history import BaseChatMessageHistory
from typing import Dict, Any, List
from langchain_core.pydantic_v1 import BaseModel, Field


import logging

store = {}


def get_by_session_id(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryHistory()
    return store[session_id]


class InMemoryHistory(BaseChatMessageHistory, BaseModel):
    """In memory implementation of chat message history."""

    messages: List[BaseMessage] = Field(default_factory=list)

    def add_messages(self, messages: List[BaseMessage]) -> None:
        """Add a list of messages to the store"""
        self.messages.extend(messages)

    def clear(self) -> None:
        self.messages = []


def create_chat_model() -> ChatOpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    return ChatOpenAI(model="gpt-4o-mini", temperature=0.5, api_key=api_key)


def create_chain_with_history(chain, session_id: str):
    """Create a chain with chat history, passing the session ID."""
    return RunnableWithMessageHistory(
        chain,
        lambda: get_by_session_id(session_id),  # Pass the session_id here
        input_messages_key="question",
        history_messages_key="history",
    )


def build_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages(
        [
            ("system", "You're an assistant who's good at answering questions."),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}"),
        ]
    )


def process_chatbot1(llm: ChatOpenAI, question: str, chatbot_id: str) -> Dict[str, Any]:
    """Process interaction for chatbot1."""
    prompt = build_prompt()
    chain = prompt | llm
    chain_with_history = create_chain_with_history(chain, chatbot_id)
    inputs = {"question": question}
    response_content = chain_with_history.invoke(
        inputs, config={"configurable": {"session_id": chatbot_id}}
    )
    return {"response": response_content.content}


def process_chatbot2(llm: ChatOpenAI, question: str, chatbot_id: str) -> Dict[str, Any]:
    """Process interaction for chatbot2."""
    prompt = build_prompt()
    chain = prompt | llm
    chain_with_history = create_chain_with_history(chain, chatbot_id)
    inputs = {"question": question}
    response_content = chain_with_history.invoke(
        inputs, config={"configurable": {"session_id": chatbot_id}}
    )

    new_message = ChatMessage(question=question, response=response_content.content)
    alchemy_db.session.add(new_message)
    alchemy_db.session.commit()

    return {"response": response_content.content}


def process_chatbot3(llm: ChatOpenAI, question: str, chatbot_id: str) -> Dict[str, Any]:
    """Process interaction for chatbot3."""
    generate_query = create_sql_query_chain(llm, mysql_db)
    execute_query = QuerySQLDataBaseTool(db=mysql_db)

    answer_prompt = ChatPromptTemplate.from_template(
        """
        Given the following user question, corresponding SQL query, and SQL result, answer the user question.
        Conversation history: {history}
        Question: {question}
        SQL Query: {query}
        SQL Result: {result}
        Answer: 
    """
    )

    # Chain setup
    rephrase_answer = answer_prompt | llm | StrOutputParser()
    chain = (
        RunnablePassthrough.assign(query=generate_query).assign(
            result=itemgetter("query") | execute_query
        )
        | rephrase_answer
    )
    chain_with_history = create_chain_with_history(chain, chatbot_id)  # Pass chatbot_id

    inputs = {"question": question}
    response_content = chain_with_history.invoke(
        inputs, config={"configurable": {"session_id": chatbot_id}}
    )

    return {"response": response_content}
