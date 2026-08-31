"""Context Retrieval Service.

Manages vector embeddings generation using FastEmbed (`BAAI/bge-small-en-v1.5`)
and persistent storage/similarity search with ChromaDB.
"""

import os
from typing import List
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_community.embeddings import FastEmbedEmbeddings

from app.core.config import settings
from app.services.doc_processor import DocProcessor


class ContextRetriever:
    """Manages document vectorization, ChromaDB persistence, and semantic search retrieval."""

    def __init__(self) -> None:
        """Initialize the context retriever with FastEmbed and Chroma vector store."""
        self.doc_processor = DocProcessor()
        self.embedding = FastEmbedEmbeddings(
            model_name="BAAI/bge-small-en-v1.5"
        )
        self.vec_store = self.get_or_create_vector_store()

    def get_or_create_vector_store(self) -> Chroma:
        """Load an existing Chroma vector store if present on disk; otherwise index documents from scratch.

        Returns:
            Chroma: Initialized Chroma vector store instance.
        """
        if os.path.exists(settings.chroma_persist_dir):
            return Chroma(
                persist_directory=settings.chroma_persist_dir,
                embedding_function=self.embedding,
            )
        else:
            return self.index_documents()

    def index_documents(self) -> Chroma:
        """Process documents from disk, compute dense embeddings, and persist in ChromaDB.

        Returns:
            Chroma: Vector store populated with indexed document chunks.
        """
        processed_docs = self.doc_processor.process_docs()
        vec_store = Chroma.from_documents(
            documents=processed_docs,
            embedding=self.embedding,
            persist_directory=settings.chroma_persist_dir,
        )
        print(f"[vector store] Indexed {len(processed_docs)} chunks at {settings.chroma_persist_dir}")
        return vec_store

    def retrieve(self, query: str, k: int = 3) -> List[Document]:
        """Perform semantic similarity search on the indexed technical documentation.

        Args:
            query (str): The search query to find matching documents for.
            k (int): Number of top relevant document chunks to retrieve (default: 3).

        Returns:
            List[Document]: List of most relevant Document chunks.
        """
        return self.vec_store.similarity_search(query, k=k)


# Singleton instance of ContextRetriever for reuse across requests
retriever = ContextRetriever()

