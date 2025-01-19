import json

def parse_ruby_file(file_path, output_path):
    """Parse a Ruby file and save the structured data to a JSON file."""
    scenarios = []
    with open(file_path, "r") as file:
        scenario = {}
        for line in file:
            line = line.strip()
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

    # Write scenarios to JSON
    with open(output_path, "w") as json_file:
        json.dump(scenarios, json_file, indent=4)
    print(f"Scenarios successfully parsed and saved to {output_path}")

# Example Usage
if __name__ == "__main__":
    input_file = "data/scenarios.rb"  # Path to Ruby file
    output_file = "data/scenarios.json"  # Path to JSON file
    parse_ruby_file(input_file, output_file)