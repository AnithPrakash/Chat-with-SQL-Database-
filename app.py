#import libraries

import streamlit as st
import mysql.connector

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_groq import ChatGroq
import os 
#load api_key
from dotenv import load_dotenv
load_dotenv()


from langchain_community.llms import GooglePalm
GOOGLE_API_KEY="AIzaSyDE_I7gKf4WE6sW3wuHYFEfDbnACoKKawE"



def init_database(hostname:str, port:str,username:str, password:str, database:str)-> SQLDatabase:
    db_uri=f"mysql+mysqlconnector://{username}:{password}@{hostname}:{port}/{database}"
    return SQLDatabase.from_uri(db_uri)

def get_sql_chain(db):
    template="""
    You are a data analyst at a company. You are interacting with a user who is asking you question about the company's database.
    Based on the table schema below, write a SQL query that would answer the user's question. Take the conversation histroy into account.

    <SCHEMA>{{SCHEMA}}</SCHEMA>

    Conversation histroy : {{chat_histroy}}

    write only SQL query and nothing else. Do not wrap the SQL query in any other text, not even backticks.

    For example:
    qusetion : which 3 tshirt have the lowest price rate?
    SQL Query: select brand,price from t_shirts order by price asc limit 3;
    question : which 3 t shirt have higher discount ?
    SQL Query : SELECT t_shirts.brand, t_shirts.price FROM t_shirts INNER JOIN discounts ON t_shirts.t_shirt_id = discounts.t_shirt_id ORDER BY discounts.pct_discount asc limit 3;

    Your turn:

    Question: {{question}}
    SQL Query:
    """

    prompt=ChatPromptTemplate.from_template(template=template)

    llm=GooglePalm(google_api_key=GOOGLE_API_KEY, temperature=0.2)

    def get_schema(_):
        return db.get_table_info()
    
    return (
        RunnablePassthrough.assign(schema=get_schema)
        | prompt
        | llm
        | StrOutputParser()
    )

def get_response(user_query: str, db: SQLDatabase, chat_histroy: list):
    sql_chain = get_sql_chain(db)

    template="""
     Your a data analyst at a company. You are interacting with a asking you question about the company database.
     Based on the table schema below, question, sql query, and sql response write natural language response. 
     <SCHEMA> {{schema}} <SCHEMA>

     Conversation Histroy : {{chat_history}}
     SQL Query : <SQL> {{query}} </SQL>
     User Question: {{question}}
     SQL Response: {{response}}

     Response Format:
        SQL Query: 
        Natural Language Response:

    """

    prompt=ChatPromptTemplate.from_template(template)


    llm = ChatGroq(model="Mixtral-8x7b-32768", temperature=0.2)

    chain= (
        RunnablePassthrough.assign(query=sql_chain).assign(
            schema=lambda _: db.get_table_info(),
            response=lambda vars:db.run(vars["query"]),
        )
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain.invoke({"question": user_query,
                         "chat_histroy": chat_histroy,
                         })


if "chat_histroy" not in st.session_state:
    st.session_state.chat_histroy=[
        AIMessage(content="Hello !! I am a SQL assitant. Ask me anythings about your database.")
    ]

st.set_page_config(page_title="Chat with MySQL", page_icon=":speech_balloons:")
st.title("Chat with MySQL")


with st.sidebar:
    st.subheader("Settings")
    st.write("Simple chat application using MySql.")

    #connect database
    st.text_input("Host",value="localhost", key="Host")
    st.text_input("Port", value="3306", key="Port")
    st.text_input("User-Name", value="root", key="Username")
    st.text_input("Password",type="password",value="admin", key="password")
    st.text_input("Database", value="atliq_tshirts", key="Database")

    if st.button("Connect"):
        with st.spinner("connecting the database..."):
            
            db=init_database(
                    st.session_state["Host"],
                    st.session_state["Port"],
                    st.session_state["Username"],
                    st.session_state["password"],
                    st.session_state["Database"],
                )
            st.session_state.db = db
            st.success("connected to database")


#interactive chat interface        
for message in st.session_state.chat_histroy:
    if isinstance(message,AIMessage):
        with st.chat_message("AI"):
            st.markdown(message.content)

    elif isinstance(message, HumanMessage):
        with st.chat_message("Human message"):
            st.markdown(message.content)


user_query=st.chat_input("Type a message....🙄")
if user_query is not None and user_query.strip() != "":
    st.session_state.chat_histroy.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        response=get_response(user_query,st.session_state.db,st.session_state.chat_histroy)
        st.markdown(response)

    st.session_state.chat_histroy.append(AIMessage(content=response))