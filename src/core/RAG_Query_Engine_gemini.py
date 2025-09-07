from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from src.config import GEMINI_API_KEY  # Import the API key

# --- Constants ---
DB_PATH = "vectorstores/db_chroma"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL_NAME = "gemini-2.5-flash-preview-05-20"  # Updated model name


def get_rag_chain():
    """
    Builds and returns a RAG (Retrieval-Augmented Generation) chain.
    The chain retrieves relevant documents from a vector store and uses the
    Gemini API to generate an answer based on the retrieved context.
    """
    # 1. Load the vector store and create a retriever
    embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    vectorstore = Chroma(persist_directory=DB_PATH, embedding_function=embedding_model)
    retriever = vectorstore.as_retriever(search_kwargs={'k': 3})  # Retrieve top 3 chunks

    # 2. Define the prompt template
    template = """
    ענה על השאלה אך ורק בהתבסס על ההקשר הבא:

    {context}

    שאלה: {question}
    """
    prompt = PromptTemplate.from_template(template)

    # 3. Initialize the Gemini LLM
    # This now uses the ChatGoogleGenerativeAI class with your API key
    llm = ChatGoogleGenerativeAI(model=LLM_MODEL_NAME, google_api_key=GEMINI_API_KEY)

    # 4. Build the RAG chain using LangChain Expression Language (LCEL)
    rag_chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
    )

    return rag_chain


def ask_question(question: str):
    """
    Initializes the RAG chain and asks a specific question.
    """
    print("--- Setting up RAG chain... ---")
    rag_chain = get_rag_chain()

    print(f"\n--- Asking question: {question} ---")
    answer = rag_chain.invoke(question)

    print("\n--- Answer: ---")
    print(answer)
