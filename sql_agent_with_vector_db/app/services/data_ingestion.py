import os
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore

class DataIngestor:
    def __init__(self, model="text-embedding-3-small", dimensions=1536):
        self.model = model
        self.dimensions = dimensions
        os.environ["OPENAI_API_KEY"] = ""
        os.environ["PINECONE_API_KEY"] = ""
        self.embedding_model = OpenAIEmbeddings(model=self.model, dimensions=self.dimensions)
        self.pinecone = Pinecone(api_key="")

    def ingest_data(self, data, index_name):
        index = self.pinecone.Index(index_name)

        docs = [data]
        # Splitting data into smaller chunks
        # Embedding documents
        embeddings = self.embedding_model.embed_documents(docs)

        # Preparing documents for upsert
        documents = []
        for i, embedding in enumerate(embeddings):
            documents.append({
                "id": f"doc_{i}",
                "values": embedding,
                "metadata": {
                    "text": docs[i]
                },
            })

        # Upserting documents to the Pinecone index
        index.upsert(documents)
      
    def retrieve_documents(self, query, index_name):
        vectorstore = PineconeVectorStore(index_name=index_name, embedding=self.embedding_model)
        return vectorstore.similarity_search(query)

ingestor = DataIngestor()
