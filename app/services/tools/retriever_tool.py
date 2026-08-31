"""Retriever Tool for LangChain and LangGraph Agent.

Exposes the `retriever_tool` decorated with `@tool` so the LLM agent can autonomously
query the vector database to fetch relevant technical documentation chunks.
"""

from langchain_core.tools import tool
from app.services.retriever import retriever


@tool
def retriever_tool(query: str, k: int = 3) -> str:
    """Search and retrieve technical documentation from the vector store.

    Args:
        query: The reformulated, concise technical search query representing the user's core intent
               (e.g., 'FastAPI custom exception handler', 'Pydantic BaseSettings env configuration').
               Do NOT pass raw conversational input directly.
        k: Number of relevant documentation chunks to retrieve (default: 3).

    Returns:
        str: Formatted context string containing the document sources and chunk text,
             or 'No documents found' if no matching content was retrieved.
    """
    docs = retriever.retrieve(query, k=k)
    if not docs:
        return "No documents found"

    context = ""
    for doc in docs:
        # Simplify document source path to relative file name for cleaner citations
        source = doc.metadata.get("source", "Unknown")
        if "data/documents/" in source:
            source = source.split("data/documents/")[-1]
        doc.metadata["source"] = source

        context += f"**Document:** {source}\n\n"
        context += f"{doc.page_content}\n\n"

    return context




