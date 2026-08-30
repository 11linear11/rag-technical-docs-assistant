# pyrefly: ignore [missing-import]
from app.services.retriever import retriever
from langchain_core.tools import tool


@tool
def retriever_tool(query: str, k: int = 3):
    """Tool to retrieve documents from the vector store"""
    docs = retriever.retrieve(query, k=k)
    if not docs:
        return "No documents found"
    context = ""
    for doc in docs:
        doc.metadata["source"] = doc.metadata["source"].split("data/documents/")[-1]
        context += f"**Document:** {doc.metadata['source']}\n\n"
        context += f"{doc.page_content}\n\n"
    return context


if __name__ == "__main__":
    result = retriever_tool.invoke({"query": "How to handle exceptions?", "k": 2})
    print(result)