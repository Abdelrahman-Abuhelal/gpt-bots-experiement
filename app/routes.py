from flask import Flask, request, session, Blueprint, render_template, jsonify
from .models import ChatMessage
from . import db
from openai import OpenAI
import os
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from . import db as alchemy_db  # Import your Flask SQLAlchemy db
from . import mysql_db    # the SQLDatabase instance
from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.chains import ConversationChain,LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import HumanMessage, SystemMessage,BaseMessage
from langchain_core.chat_history import BaseChatMessageHistory

from typing import List
from langchain_core.pydantic_v1 import BaseModel,Field
#from pydantic import BaseModel, Field


main = Blueprint("main", __name__)

# client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

store = {}

def get_by_session_id(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryHistory()
    return store[session_id]

class InMemoryHistory(BaseChatMessageHistory,BaseModel):
    """In memory implementation of chat message history."""
    messages: List[BaseMessage] = Field(default_factory=list)

    def add_messages(self, messages: List[BaseMessage]) -> None:
        """Add a list of messages to the store"""
        self.messages.extend(messages)

    def clear(self) -> None:
        self.messages = []


@main.route("/")
def index():
    return render_template("./index.html")
    

@main.route("/api/<chatbot_id>", methods=["POST"])
def api(chatbot_id):
    question = request.json.get("message")
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5, api_key=os.environ.get("OPENAI_API_KEY"))
    
    if chatbot_id == 'chatbot1':
        
        prompt = ChatPromptTemplate.from_messages([
        ("system", "You're an assistant who's good at answering questions."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
        ])
        chain = prompt | llm
        
        chain_with_history = RunnableWithMessageHistory(
        chain,
        get_by_session_id,
        input_messages_key="question",
        history_messages_key="history",
        )

        history = get_by_session_id(chatbot_id)
        print(history)
        inputs = {
        "question": question
         }
        response_content = chain_with_history.invoke(
        inputs,
        config={"configurable": {"session_id": chatbot_id}}
        )
        return response_content.content

    if chatbot_id == 'chatbot2':
        # Use the conversation chain to get a response
        history = get_by_session_id(chatbot_id)
        
        prompt = ChatPromptTemplate.from_messages([
        ("system", "You're an assistant who's good at answering questions."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
        ])
        chain = prompt | llm
        chain_with_history = RunnableWithMessageHistory(
        chain,
        get_by_session_id,
        input_messages_key="question",
        history_messages_key="history",
        )

        print(history)
        inputs = {
        "question": question
        }
    
        response_content = chain_with_history.invoke(
        inputs,
        config={"configurable": {"session_id": chatbot_id}}
        )
        
        new_message = ChatMessage(question=question, response=response_content.content)
        alchemy_db.session.add(new_message)
        alchemy_db.session.commit()

        return response_content.content
    
    if chatbot_id == 'chatbot3':
        # memory = ConversationBufferMemory()
        history = get_by_session_id(chatbot_id) 

        generate_query = create_sql_query_chain(llm, mysql_db)
        # print(query)
        execute_query = QuerySQLDataBaseTool(db=mysql_db)
        # result = execute_query.invoke(query)
        # print(result)
        answer_prompt = ChatPromptTemplate.from_template(
        """Given the following user question, corresponding SQL query, and SQL result, answer the user question.
        Conversation history: {history}
        Question: {question}        
        SQL Query: {query}
        SQL Result: {result}
        Answer: """
    )
        rephrase_answer = answer_prompt | llm | StrOutputParser()
        chain = (
            RunnablePassthrough.assign(query=generate_query).assign(
            result=itemgetter("query") | execute_query
            ) | rephrase_answer )
        
        chain_with_history = RunnableWithMessageHistory(
        chain,
        get_by_session_id,
        input_messages_key="question",
        history_messages_key="history",
        )

        print(history)
        inputs = {
        "question": question
        }
     

        response_content = chain_with_history.invoke(
        inputs,
        config={"configurable": {"session_id": chatbot_id}}
        )
        
        return response_content
    
    else:
        return "Failed to Generate response!"


@main.route("/messages", methods=["GET"])
def get_messages():
    messages = ChatMessage.query.all()
    return jsonify(
        [
            {"id": msg.id, "question": msg.question, "response": msg.response}
            for msg in messages
        ]
    )


@main.route("/messages/<int:id>", methods=["GET"])
def get_message(id):
    message = ChatMessage.query.get(id)
    if message:
        return jsonify(
            {
                "id": message.id,
                "question": message.question,
                "response": message.response,
            }
        )
    else:
        return jsonify({"error": "Message not found"}), 404


@main.route("/messages/<int:id>", methods=["PUT"])
def update_message(id):
    message = ChatMessage.query.get(id)
    if message:
        data = request.json
        message.question = data.get("question", message.question)
        message.response = data.get("response", message.response)
        db.session.commit()
        return jsonify(
            {
                "id": message.id,
                "question": message.question,
                "response": message.response,
            }
        )
    else:
        return jsonify({"error": "Message not found"}), 404


@main.route("/messages/<int:id>", methods=["DELETE"])
def delete_message(id):
    message = ChatMessage.query.get(id)
    if message:
        db.session.delete(message)
        db.session.commit()
        return jsonify({"message": "Message deleted"})
    else:
        return jsonify({"error": "Message not found"}), 404
