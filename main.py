# # from src.core.ask_question import ask_question
# from src.core.RAG_Query_Engine_gemini import ask_question
#
# # Ask your first question!
# # ask_question("מהם זכויות המובטלים?")
# ask_question("על איזה שאלות אתה יודע לענות?")

import argparse
from src.core.RAG_Query_Engine_gemini import ask_question

if __name__ == "__main__":
    # Set up a command-line argument parser to accept a question
    parser = argparse.ArgumentParser(description="Ask a question to the Israeli Labor Law RAG chatbot.")
    parser.add_argument("question", type=str, help="The question you want to ask.")

    args = parser.parse_args()

    # Call the main function from our core logic
    ask_question(args.question)