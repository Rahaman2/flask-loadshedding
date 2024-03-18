import csv
from fuzzywuzzy import fuzz

# Function to preprocess town names
def preprocess_town_name(town_name):
    """Replace colons with semicolons to clean up the town name"""
    return town_name.replace(':', ',')



# with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             name = preprocess_town_name(row["town"])

# Function to load data from CSV file
def load_data(file_path):
    """Reads the csv file"""
    towns = {}
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            town_name = preprocess_town_name(row['town_name'])
            
            municipality = row['municipality']
            print(municipality)
            # print(municipality)
            if town_name not in towns:
                towns[town_name] = [municipality]
            else:
                towns[town_name].append(municipality)
    return towns


# Function to find matching towns based on user input
def find_matching_towns(user_input, towns):
    # print(towns)
    exact_matches = []
    fuzzy_matches = []

    # Check for exact matches
    for town_name, municipalities in towns.items():
        if user_input.lower() == town_name.lower():
            exact_matches.append((town_name, municipalities))
            

    # If there are fewer than 5 exact matches, fill the remaining slots with fuzzy matches
    if len(exact_matches) < 5:
        # Calculate fuzzy matches for the remaining slots
        for town_name, municipalities in towns.items():
            if town_name.lower().startswith(user_input.lower()) and town_name not in [match[0] for match in exact_matches]:
                ratio = fuzz.partial_ratio(user_input.lower(), town_name.lower())
                fuzzy_matches.append((town_name, municipalities, ratio))

        # Sort fuzzy matches by match ratio
        fuzzy_matches.sort(key=lambda x: x[2], reverse=True)

        # Add the best fuzzy matches to fill the remaining slots
        remaining = 5 - len(exact_matches)
        for i in range(min(remaining, len(fuzzy_matches))):
            exact_matches.append((fuzzy_matches[i][0], fuzzy_matches[i][1]))
    
    # Return the top 5 matches
    return exact_matches[:5]






# Main function
def main():
    file_path = 'towns/towns.csv'  # Update with your CSV file path
    towns = load_data(file_path)
    
    while True:
        user_input = input("Enter a town name (or 'quit' to exit): ")
        if user_input.lower() == 'quit':
            break
        matches = find_matching_towns(user_input, towns)
        if matches:
            print("Top 5 matching towns:")
            for match in matches:
                print(match[0])
        else:
            print("No matching towns found.")

# if __name__ == "__main__":
#     main()
