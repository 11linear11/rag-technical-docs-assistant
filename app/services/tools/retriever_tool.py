# pyrefly: ignore [missing-import]
from app.services.retriever import retriever
from langchain_core.tools import tool


@tool
def retriever_tool(query: str, k: int = 3):
    """Search and retrieve technical documentation from the vector store.

    Args:
        query: The reformulated, concise technical search query representing the user's core intent (e.g., 'FastAPI custom exception handler', 'Pydantic BaseSettings env configuration'). Do NOT pass raw conversational input directly.
        k: Number of relevant documentation chunks to retrieve (default: 3).
    """
    docs = retriever.retrieve(query, k=k)
    if not docs:
        return "No documents found"
    context = ""
    for doc in docs:
        doc.metadata["source"] = doc.metadata["source"].split("data/documents/")[-1]
        context += f"**Document:** {doc.metadata['source']}\n\n"
        context += f"{doc.page_content}\n\n"
    return context



