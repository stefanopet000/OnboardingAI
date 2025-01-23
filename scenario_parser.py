import re
from typing import List, Dict

class ScenarioParser:
    def parse_ruby_scenarios(self, content: str) -> List[Dict]:
        """Parse Ruby scenario content into structured data"""
        scenarios = []
        current_scenario = {}
        
        for line in content.split('\n'):
            line = line.strip()
            
            if line.startswith("Scenario:"):
                if current_scenario:
                    scenarios.append(current_scenario)
                title = line.replace("Scenario:", "").strip()
                # Extract category if it's in [Category] format
                category_match = re.match(r'\[(.*?)\](.*)', title)
                if category_match:
                    category, title = category_match.groups()
                else:
                    category = "Uncategorized"
                    
                current_scenario = {
                    "title": title.strip(),
                    "category": category.strip(),
                    "team": "Unknown",  # Can be set based on Linear project
                }
            elif line.startswith("Given"):
                current_scenario["given"] = line.replace("Given", "").strip()
            elif line.startswith("When"):
                current_scenario["when"] = line.replace("When", "").strip()
            elif line.startswith("Then"):
                current_scenario["then"] = line.replace("Then", "").strip()
                
        if current_scenario:  # Add the last scenario
            scenarios.append(current_scenario)
            
        return scenarios 