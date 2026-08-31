"""Document Processing Service.

Loads Markdown technical documentation files from disk and splits them into
chunks using recursive character text splitting for indexing into the vector store.
"""

from langchain_core.documents import Document
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.config import settings


class DocProcessor:
    """Handles loading and chunking of markdown documentation files."""

    def __init__(self) -> None:
        """Initialize the document processor with configuration parameters."""
        self.docs_dir = settings.docs_dir
        self.chunk_size = settings.chunk_size
        self.chunk_overlap = settings.chunk_overlap

    def loader_docs(self) -> list[Document]:
        """Load all Markdown (.md) documents recursively from the configured documents directory.

        Returns:
            list[Document]: A list of loaded LangChain Document objects with page content and metadata.
        """
        loader = DirectoryLoader(
            self.docs_dir,
            glob="**/*.md",
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"},
        )
        return loader.load()

    def process_docs(self) -> list[Document]:
        """Load documents and split them into overlapping character chunks.

        Returns:
            list[Document]: A list of chunked Document objects ready for embedding generation.
        """
        docs = self.loader_docs()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
        )
        return text_splitter.split_documents(docs)



