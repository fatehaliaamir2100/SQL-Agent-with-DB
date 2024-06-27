from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import create_sql_agent

from app.services.data_ingestion import ingestor
from app.validators.schema.chat_inference import InferenceRequest

class SQLAgent:
    def __init__(self, llm_model_name="gpt-3.5-turbo"):
        self.db = SQLDatabase.from_uri(database_uri = self.get_url())
        self.llm_model_name = llm_model_name

        self.chat_llm = ChatOpenAI(
            openai_api_key="",
            model= self.llm_model_name,
            temperature=0,
            verbose=True,
            model_kwargs={"response_format": {"type": "json_object"}},
        )        

        self.system = """You are an agent designed to interact with a SQL database.
        Given an input question, create a syntactically correct MySQL query to run, then look at the results of the query and return the answer.
        Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most 3 results.
        You can order the results by a relevant column to return the most interesting examples in the database.
        Never query for all the columns from a specific table, only ask for the relevant columns given the question.
        You have access to tools for interacting with the database.
        Only use the given tools. Only use the information returned by the tools to construct your final answer.
        Only use the results of the given SQL query to generate your final answer and return that.
        You MUST double check your query before executing it. If you get an error while executing a query then you should stop!
        
        Your department: {department}
        Your customer Id: {customer_id}
        Your context from previous similar requests: {context}
        Your question: {input}
        
        Return your response in a JSON format
        """

        print(self.system)
        print(self.db)
        print(self.chat_llm)

    def create_sql_agent(self):
        return create_sql_agent(
            llm=self.chat_llm,
            db=self.db,
            prompt=self.prompt,
            agent_type="openai-tools",
            verbose=True,
        )

    def process_inference(self, data: InferenceRequest):
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.system), 
                ("human", "{input}"), 
                ("human", "{department}"),
                ("human", "{customer_id}"),
                ("human", "{context}"),
                MessagesPlaceholder(variable_name="agent_scratchpad")
            ]
        )

        vector_query = f"query: {data.query}, customer_id: {data.customer_id}, department: {data.department}"
        
        documents = []
        
        if data.updated == False:
            documents = ingestor.retrieve_documents(vector_query, data.department)
    
        self.agent = self.create_sql_agent()

        response = self.agent.invoke({"input": data.query, 
                                     "department": data.department, 
                                     "customer_id": data.customer_id, 
                                     "context": documents})

        ingestor.ingest_data(f"query: {data.query}, response: {response}", data.department),

        print(response["output"])
        
        return {"response": response["output"]}

    def get_url(self) -> str:
        """Returns the database url using string interpolation."""
        host = "localhost"
        port = "3306"
        database = "roiforpros_dev"
        username = "root"
        password = "admin"
        return f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}?charset=utf8mb4"


sqlagent = SQLAgent()