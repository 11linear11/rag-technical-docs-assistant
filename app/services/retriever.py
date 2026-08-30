from app.core.config import settings
from app.services.doc_processor import DocProcessor
# pyrefly: ignore [missing-import]
from langchain_chroma import Chroma
# pyrefly: ignore [missing-import]
from langchain_community.embeddings import FastEmbedEmbeddings
import os

class ContextRetriever:
    def __init__(self):
        self.doc_processor = DocProcessor()
        self.embedding = FastEmbedEmbeddings(
            model_name="BAAI/bge-small-en-v1.5"
        )
        self.vec_store = self.get_or_create_vector_store()
    
    def get_or_create_vector_store(self):
        if os.path.exists(settings.chroma_persist_dir):
            return Chroma(
                persist_directory=settings.chroma_persist_dir,
                embedding_function=self.embedding
            )
        else:
            return self.index_documents()

            
    def index_documents(self):

        vec_store = Chroma.from_documents(
            documents=self.doc_processor.process_docs(),
            embedding=self.embedding,
            persist_directory=settings.chroma_persist_dir
        )
        print(f"[vector store] Indexed documents at {settings.chroma_persist_dir}")
        return vec_store
    def retrieve(self,query:str,k=3):
        return self.vec_store.similarity_search(query, k=k)

retriever = ContextRetriever()
