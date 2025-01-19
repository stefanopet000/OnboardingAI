import re
import json

def parse_ruby_file(file_path):
    scenarios = []
    with open(file_path, "r") as file:
        scenario = {}
        for line in file:
            if line.startswith("Scenario:"):
                if scenario:  # Save the previous scenario if it exists
                    scenarios.append(scenario)
                scenario = {"scenario": line.replace("Scenario:", "").strip()}
            elif line.startswith("Given"):
                scenario["given"] = line.replace("Given", "").strip()
            elif line.startswith("When"):
                scenario["when"] = line.replace("When", "").strip()
            elif line.startswith("Then"):
                scenario["then"] = line.replace("Then", "").strip()
        if scenario:  # Append the last scenario
            scenarios.append(scenario)
    return scenarios

# Save parsed scenarios to JSON
scenarios = parse_ruby_file("scenarios.rb")
with open("scenarios.json", "w") as json_file:
    json.dump(scenarios, json_file, indent=4)