import os
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# --- Constants ---
# This is where your downloaded text files are.
DATA_PATH = "data/raw"
# This is where the vector database will be saved.
DB_PATH = "vectorstores/db_chroma"

def main(limit=None):
    """
    Main function to build the vector store.
    1. Loads documents from the data path.
    2. Chunks the documents into smaller pieces.
    3. Creates embeddings for the chunks.
    4. Saves the embeddings to a Chroma vector store.
    """
    # 1. Load the documents
    print("--- Loading documents... ---")
    loader = DirectoryLoader(DATA_PATH, glob="*.txt")
    documents = loader.load()
    print(f"Loaded {len(documents)} documents.")

    if limit and limit > 0:
        print(f"--- Limiting processing to the first {limit} documents. ---")
        documents = documents[:limit]

    # 2. Chunk the documents
    print("--- Chunking documents... ---")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)
    print(f"Split documents into {len(texts)} chunks.")

    # 3. Create embeddings
    print("--- Creating embeddings... (This may take a few minutes) ---")
    # We use a powerful multilingual model that works well for Hebrew
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # 4. Create and save the vector store
    print("--- Creating and persisting vector store... ---")
    # This single command creates the embeddings and saves them to disk.
    db = Chroma.from_documents(
        texts, 
        embedding_model, 
        persist_directory=DB_PATH
    )
    
    print("\n--- Vector store created successfully! ---")
    print(f"Database saved at: {DB_PATH}")

# The __main__ block is commented out because in a Colab notebook,
# we will call the main() function directly from a code cell.
# This makes the script more interactive and easier to use for experiments.

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Build a Chroma vector store from raw text documents.")
#     parser.add_argument(
#         "-l", "--limit", 
#         type=int, 
#         default=None, 
#         help="Limit the number of documents to process (e.g., for testing)."
#     )
#     args = parser.parse_args()
    
#     main(limit=args.limit)

# --- HOW TO RUN IN A COLAB CELL ---
# To build the vector store for all documents, you would run this in a cell:
# main()
#
# To build for a limited number of documents (e.g., 10), you would run:
# main(limit=10)

