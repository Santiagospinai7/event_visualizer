import sys
import os

# Add the root directory of the project to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.time_utils import convert_time_to_region

data = [
    {"region": "NAW", "original": "2025-07-01T06:00:00Z", "converted_expected": "2025-06-30 23:00:00", "diff": "UTC-7 (Summer)"},
    {"region": "EU", "original": "2025-06-01T12:00:00Z", "converted_expected": "2025-06-01 14:00:00", "diff": "UTC+2 (Summer)"},
    {"region": "OCE", "original": "2025-01-15T06:00:00Z", "converted_expected": "2025-01-15 17:00:00", "diff": "UTC+11 (Summer)"},
    {"region": "BR", "original": "2025-01-15T06:00:00Z", "converted_expected": "2025-01-15 03:00:00", "diff": "UTC-3 "},
    
    {"region": "NAW", "original": "2025-12-01T06:00:00Z", "converted_expected": "2025-11-30 22:00:00", "diff": "UTC-8 (winter)"},
    {"region": "EU", "original": "2025-12-01T12:00:00Z", "converted_expected": "2025-12-01 13:00:00", "diff": "UTC+1 (winter)"},
    {"region": "OCE", "original": "2025-07-01T06:00:00Z", "converted_expected": "2025-07-01 16:00:00", "diff": "UTC+10 (winter)"},
    
    {"region": "ASIA", "original": "2025-03-01T06:00:00Z", "converted_expected": "2025-03-01 15:00:00", "diff": "UTC+9"},
    {"region": "ME", "original": "2025-03-01T06:00:00Z", "converted_expected": "2025-03-01 10:00:00", "diff": "UTC+4"},
    
    {"region": "NAW", "original": "2025-04-15T06:00:00Z", "converted_expected": "2025-04-14 23:00:00", "diff": "UTC-7 (Summer)"},
    {"region": "EU", "original": "2025-03-29T23:00:00Z", "converted_expected": "2025-03-30 01:00:00", "diff": "UTC+2 (Summer)"},
    {"region": "BR", "original": "2025-05-15T12:00:00Z", "converted_expected": "2025-05-15 09:00:00", "diff": "UTC-3"},
    {"region": "ASIA", "original": "2025-06-10T02:00:00Z", "converted_expected": "2025-06-10 11:00:00", "diff": "UTC+9"},
    {"region": "OCE", "original": "2025-02-01T23:00:00Z", "converted_expected": "2025-02-02 10:00:00", "diff": "UTC+11"},
    {"region": "ME", "original": "2025-07-20T06:00:00Z", "converted_expected": "2025-07-20 10:00:00", "diff": "UTC+4"},
    {"region": "NAC", "original": "2025-09-15T00:00:00Z", "converted_expected": "2025-09-14 20:00:00", "diff": "UTC-4 (Summer)"},
    {"region": "EU", "original": "2025-01-15T06:00:00Z", "converted_expected": "2025-01-15 07:00:00", "diff": "UTC+1"},
    {"region": "ASIA", "original": "2025-10-01T18:00:00Z", "converted_expected": "2025-10-02 03:00:00", "diff": "UTC+9"},
    {"region": "OCE", "original": "2025-08-15T06:00:00Z", "converted_expected": "2025-08-15 16:00:00", "diff": "UTC+10"},
    {"region": "NAW", "original": "2025-11-01T06:00:00Z", "converted_expected": "2025-10-31 23:00:00", "diff": "UTC-7 (Summer)"},
    {"region": "ME", "original": "2025-12-15T06:00:00Z", "converted_expected": "2025-12-15 10:00:00", "diff": "UTC+4"},
]

for entry in data:
    entry["converted"] = convert_time_to_region(entry["original"], entry["region"])

def print_results(data):
    print("Resultados de la Conversión:\n" + "=" * 50)
    correct = 0
    incorrect = 0

    for entry in data:
        result = "Correct" if entry['converted'] == entry['converted_expected'] else "Incorrect"
        if result == "Correct":
            correct += 1
        else:
            incorrect += 1

        print(f"Region: {entry['region']} ({entry['diff']})")
        print(f"Original: {entry['original']}")
        print(f"Converted: {entry['converted']}")
        print(f"Expected: {entry['converted_expected']}")
        print(f"Result: {result}")
        print("-" * 50)

    print("\nResumen:")
    print(f"Casos Correctos: {correct}")
    print(f"Casos Incorrectos: {incorrect}")
    print("=" * 50)

if __name__ == "__main__":
    print_results(data)