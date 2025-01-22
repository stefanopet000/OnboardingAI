from transformers import pipeline
from fuzzywuzzy import fuzz
from parseScenario import parse_ruby_file
import json
import os
import sys
import logging



class FAQAssistant:
    def __init__(self, ruby_file, json_file):
        # Setup logging
        self.logger = logging.getLogger(__name__)
        
        try:
            if not os.path.exists(ruby_file):
                raise FileNotFoundError(f"Scenarios file not found: {ruby_file}")
            if not os.path.exists(json_file):
                print:(f"Error: The file '{json_file}' was not found. Parsing {ruby_file} now...")
                parse_ruby_file(ruby_file, json_file)
            try:
                with open(json_file, "r") as file:
                    self.scenario = json.load(file)
            except json.JSONDecodeError:
                print(f"Error: The file '{json_file}' is not a valid JSON file.")
                sys.exit(1)
        except Exception as e:
            self.logger.error(f"Initialization error: {str(e)}")
            raise

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
        try:
            best_match, highest_score = self.find_best_match(question)
            
            if best_match and highest_score > 70:
                # Add context and format the answer more naturally
                context = f"Based on the scenario about {best_match['scenario'].lower()}: "
                steps = (
                    f"When {best_match['given']}, {best_match['when']}, "
                    f"you {best_match['then']}."
                )
                return context + steps
            
            elif highest_score > 0:
                return " I found a match but I am not enough confident to provide an answer, try formulate the question differently."
            else:
                return "Sorry, I couldn't find an answer to your question. Please try again."
        except Exception as e:
            self.logger.error(f"Error in get_answer: {str(e)}")
            return "Sorry, I encountered an error. Please try again later."