# from typing import List, Dict, Any, Optional
# import os
# from langchain_community.vectorstores import FAISS
# from langchain_community.embeddings import OpenAIEmbeddings
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.document_loaders import DirectoryLoader, TextLoader
# from pydantic import BaseModel, Field


# class RAGQuery(BaseModel):
#     query: str = Field(..., description="The query to search for in the knowledge base")
#     top_k: int = Field(3, description="Number of documents to retrieve")


# class RAGResponse(BaseModel):
#     documents: List[str] = Field(..., description="Retrieved documents relevant to the query")
#     metadata: List[Dict[str, Any]] = Field(..., description="Metadata for each retrieved document")


# class RAGTool:
#     """Tool for retrieving relevant information from a knowledge base using RAG (Retrieval-Augmented Generation)."""

#     name = "rag_tool"
#     description = "Use this tool to search for information in a knowledge base when you need to retrieve specific documents."
#     args_schema = RAGQuery
#     return_schema = RAGResponse

#     def __init__(self, knowledge_dir: str = None):
#         self.knowledge_dir = knowledge_dir or os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "knowledge")
#         self.vector_store = None
#         self.initialize()

#     def initialize(self):
#         """Initialize the vector store with documents from the knowledge directory."""
#         # Check if the knowledge directory exists
#         if not os.path.exists(self.knowledge_dir):
#             os.makedirs(self.knowledge_dir, exist_ok=True)
#             with open(os.path.join(self.knowledge_dir, "sample.txt"), "w") as f:
#                 f.write("This is a sample document for the knowledge base.\n\n"
#                         "It contains information about how to use the RAG tool.\n\n"
#                         "You can add more documents to the knowledge directory to expand the knowledge base.")

#         # Load documents
#         try:
#             loader = DirectoryLoader(
#                 self.knowledge_dir,
#                 glob="**/*.txt",
#                 loader_cls=TextLoader
#             )
#             documents = loader.load()
            
#             # Split documents into chunks
#             text_splitter = RecursiveCharacterTextSplitter(
#                 chunk_size=1000,
#                 chunk_overlap=200
#             )
#             chunks = text_splitter.split_documents(documents)
            
#             # Create vector store
#             embeddings = OpenAIEmbeddings()
#             self.vector_store = FAISS.from_documents(chunks, embeddings)
#             print(f"Initialized RAG tool with {len(chunks)} document chunks")
#         except Exception as e:
#             print(f"Error initializing RAG tool: {e}")
#             # Create a minimal vector store with an empty document if loading fails
#             self.vector_store = None

#     def __call__(self, query: RAGQuery) -> RAGResponse:
#         """Search for documents relevant to the query."""
#         if not self.vector_store:
#             return RAGResponse(
#                 documents=["No documents available in the knowledge base."],
#                 metadata=[{"source": "system", "error": "Vector store not initialized"}]
#             )

#         # Retrieve relevant documents
#         results = self.vector_store.similarity_search_with_score(
#             query.query,
#             k=query.top_k
#         )

#         # Format the response
#         documents = []
#         metadata = []
        
#         for doc, score in results:
#             documents.append(doc.page_content)
#             meta = doc.metadata.copy()
#             meta["relevance_score"] = float(score)
#             metadata.append(meta)

#         return RAGResponse(documents=documents, metadata=metadata)

#     def get_schema(self) -> Dict[str, Any]:
#         """Get the schema for this tool."""
#         return {
#             "name": self.name,
#             "description": self.description,
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "query": {
#                         "type": "string",
#                         "description": "The query to search for in the knowledge base"
#                     },
#                     "top_k": {
#                         "type": "integer",
#                         "description": "Number of documents to retrieve",
#                         "default": 3
#                     }
#                 },
#                 "required": ["query"]
#             }
#         }