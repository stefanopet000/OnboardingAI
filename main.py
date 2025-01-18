from transformers import pipeline
from fuzzywuzzy import fuzz
import json
import os
import sys


class FAQAssistant:
    def __init__(self, file_path):
        self.faqs = self.load_faqs(file_path)

    def load_faqs(self, file_path):
        """Load FAQs from a JSON file."""
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
            return[]
        
    def find_best_match(self, question):
        """Find the best matching question in the FAQ data."""
        best_match = None
        highest_score = 0

        for faq in self.faqs:
            score = fuzz.ratio(question.lower(), faq['question'].lower())
            if score > highest_score:
                highest_score = score
                best_match = faq
        return best_match, highest_score
    
    def get_answer(self, question):
        best_match, highest_score = self.find_best_match(question)

        if best_match and highest_score > 70:
            return best_match["answer"]
        elif highest_score > 0:
            return " I found a match but I am not enough confident to provide an answer, try formulate the question differently."
        else:
            return "Sorry, I couldn't find an answer to your question. Please try again."

    
"""
        

# load the FAQ data
def load_faqs(file_path="data/faqs.json"):
    if not os.path.exists(file_path):
        print("Could not find the FAQ data file. Please make sure the file exists.")
        sys.exit(1)
    else:
        print("FAQ data loaded successfully")
    with open(file_path, "r") as f:
        faq_data = json.load(f)
    return faq_data

def find_best_match(question, faqs):
    # similarity check to get the closest question
    best_match = None
    highest_score = 0

    for faq in faqs:
        # Calculate similarities between user question and faq question
        score=fuzz.ratio(question.lower(), faq['question'].lower())
        if score > highest_score:
            highest_score = score
            best_match = faq
    return best_match, highest_score
    
def create_pipeline():
    print("loading model... this may take a few minutes")
    return pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

# Get an answer from the pipeline
def get_answer(question, context, qa_pipeline):
    result = qa_pipeline(question=question, context=context)
    return result["answer"]

# Main function
def main():
    # Load the FAQ data
    faqs = load_faqs()

    # Prepare context (e.g., combining all FAQ answers)
    context = " ".join([f"{q['question']} {q['answer']}" for q in faqs])

    # Initialize the pipeline
    qa_pipeline = create_pipeline()

    print("\nHi, I am your Luscii FAQ assistant, how can I help you? If you don't need me type 'exit' to quit.\n")


    while True:
        question = input(" Ask me anything: ").strip()
        if question.lower() == "exit":
            print("Feel free to ask me anything anytime. Goodbye dear Lusciian!")
            break
        
        best_match, highest_score = find_best_match(question, faqs)
        if highest_score > 80:
            print(f"Did you mean: {best_match['question']}?")
            user_input = input("Yes or No: ")
            if user_input.lower() in ["no", "n"]:
                print("Mmh, ok, in that case I'm sorry but I didn't understand the question, can you try again?")
                continue
            else:
                print("Great! Let me get the answer for you.")
                context = f"{best_match['question']} {best_match['answer']}"
                answer = qa_pipeline(question=question, context=context)['answer']
                print(f"answer: {answer}\n")
        else:    
            print("I'm sorry, I don't understand the question, can you try again?")
            continue


if __name__ == "__main__":
    main()


"""