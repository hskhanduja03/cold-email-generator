import os
import uuid
import pandas as pd
from dotenv import load_dotenv

from langchain_community.vectorstores import Qdrant
from langchain_huggingface import HuggingFaceEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

load_dotenv()

class Portfolio:
    def __init__(self, file_path="app/resource/my_portfolio.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)

        self.qdrant = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY"),
        )

        self.collection_name = "portfolio"

        try:
            self.qdrant.get_collection(self.collection_name)
        except:
            self.qdrant.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE),
            )

        self.embedding_fn = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vectorstore = Qdrant(
            client=self.qdrant,
            collection_name=self.collection_name,
            embeddings=self.embedding_fn,
        )

    def load_portfolio(self):
        if self.qdrant.count(self.collection_name).count > 0:
            return

        docs = self.data["Techstack"].tolist()
        metadatas = [{"links": row["Links"]} for _, row in self.data.iterrows()]
        self.vectorstore.add_texts(texts=docs, metadatas=metadatas)

    def query_links(self, skills):
        if not skills:
            return []

        results = self.vectorstore.similarity_search(" ".join(skills), k=2)
        return [r.metadata for r in results]
