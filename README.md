# AI Chatbot for Israeli Labor Laws (דיני עבודה)

This project is a question-answering system that leverages Retrieval-Augmented Generation (RAG) to provide answers about labor laws and employee rights in Israel. The system uses a Large Language Model (LLM) grounded on a knowledge base built from data automatically scraped from the "Kol Zchut" (כל זכות) website.



## 🎯 Project Goal

The goal is to create a simple and accessible tool for employees and employers in Israel to ask questions in natural language (e.g., "כמה ימי חופשה מגיעים לי?") and receive accurate, context-aware answers based on reliable information.

## ✨ Key Features

-   **Automated Data Pipeline:** Python scripts to scrape and process all relevant articles from Kol Zchut.
-   **Efficient Retrieval:** Documents are chunked, converted to vector embeddings, and stored in a vector database for fast semantic search.
-   **Grounded Generation:** Uses a local, open-source LLM (via Ollama) to generate answers based *only* on the retrieved legal documents, reducing hallucinations.
-   **Accessible:** Designed to be run locally without relying on paid APIs.

## 🛠️ Tech Stack

-   **Language:** Python
-   **Core Logic:** RAG (Retrieval-Augmented Generation)
-   **Key Libraries:** LangChain, Requests, BeautifulSoup4
-   **LLM Serving:** Ollama (running models like Llama 3 or Mistral)
-   **Vector Database:** ChromaDB / FAISS (for local storage)
-   **Development Environment:** Google Colab, GitHub

## 🚀 Getting Started

### Prerequisites

1.  Python 3.8+
2.  [Ollama](https://ollama.com/) installed and running.
3.  Pull a model to use, e.g., `ollama pull llama3`

### Installation & Usage

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/israeli-law-rag.git](https://github.com/YOUR_USERNAME/israeli-law-rag.git)
    cd israeli-law-rag
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Build the Knowledge Base:**
    *(This will run the scraping and embedding scripts)*
    ```bash
    python build_database.py
    ```

4.  **Run the Q&A application:**
    ```bash
    python app.py
    ```
