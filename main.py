from transformers import pipeline
from fuzzywuzzy import fuzz
from parseScenario import parse_ruby_file
import json
import os
import sys



class FAQAssistant:
    def __init__(self, ruby_file, json_file):
        if not os.path.exists(ruby_file):
            print(f"Error: I could not find any scenarios. Please first create a ruby file with the scenarios")
            sys.exit(1)
        if not os.path.exists(json_file):
            print:(f"Error: The file '{json_file}' was not found. Parsing {ruby_file} now...")
            parse_ruby_file(ruby_file, json_file)
        try:
            with open(json_file, "r") as file:
                self.scenario = json.load(file)
        except json.JSONDecodeError:
            print(f"Error: The file '{json_file}' is not a valid JSON file.")
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