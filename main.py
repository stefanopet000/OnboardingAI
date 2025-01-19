from transformers import pipeline
from fuzzywuzzy import fuzz
import json
import os
import sys


class FAQAssistant:
    def __init__(self, scenario_file):
        try:
            with open(scenario_file, "r") as file:
                self.scenario = json.load(file)
        except FileNotFoundError:
            print(f"Error: The file '{scenario_file}' was not found.")
            sys.exit(1)

    def find_best_match(self, question):
        """Find the best matching question in the FAQ data."""
        best_match = None
        highest_score = 0
        
        for scenario in self.scenario:
            score = fuzz.ratio(question.lower(), scenario['scenario'].lower())
            if score > highest_score:
                highest_score = score
                best_match = scenario
        return best_match, highest_score
    
    def get_answer(self, question):
        best_match, highest_score = self.find_best_match(question)

        if best_match and highest_score > 70:
            return (
                f"When {best_match['given']}, {best_match['when']}, "
                f"you {best_match['then']}."
            ) 
            
        elif highest_score > 0:
            return " I found a match but I am not enough confident to provide an answer, try formulate the question differently."
        else:
            return "Sorry, I couldn't find an answer to your question. Please try again."