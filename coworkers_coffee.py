import json
from datetime import datetime

# Loading coworkers from input file.  If no input file is provided (ex day 0), default list is loaded.
def load_coworkers(input_json):
    try:
        with open(input_json) as input_file:
            return json.load(input_file)
    except FileNotFoundError:
        print(f"File not found or no file provided, using default settings.")
        return [
            {"name": "Bob", "fav_coffee" : "cappuccino", "cost" : 4.00, "expected" : 0.0, "paid" : 0.00, "fairness" : 0.00},
            {"name": "Jeremy", "fav_coffee" : "black coffee", "cost" : 2.00,"expected" : 0.0,  "paid" : 0.00, "fairness" : 0.00},
            {"name": "Alice", "fav_coffee" : "cold brew", "cost" : 5.00, "expected" : 0.0, "paid" : 0.00, "fairness" : 0.00},
            {"name": "Carol", "fav_coffee" : "affogato", "cost" : 6.00, "expected" : 0.0, "paid" : 0.00, "fairness" : 0.00},
            {"name": "Dave", "fav_coffee" : "mocha", "cost" : 3.00, "expected" : 0.0, "paid" : 0.00, "fairness" : 0.00},
            {"name": "Eddie", "fav_coffee" : "americano", "cost" : 3.00, "expected" : 0.0, "paid" : 0.00, "fairness" : 0.00},
            {"name": "Francine", "fav_coffee" : "cold brew", "cost" : 1.00, "expected" : 0.0, "paid" : 0.00, "fairness" : 0.00}
        ]

def calculate_expected_payments(coworkers):
    # Calculate the average cost of a coffee
    average_cost = sum(coworker["cost"] for coworker in coworkers) / len(coworkers)
    # Calculate how many times the coworkers have gone for coffee
    total_rounds = (sum(coworker["paid"] for coworker in coworkers) / (average_cost * len(coworkers))) + 1
    
    for coworker in coworkers:
        '''
        Calculate each coworker's expected total contribution
        Expected contribution is just how much their coffee is * how many times they've gone to get coffee
        How much would they be spending if they just payed for themselves?
        '''
        expected_payment = total_rounds * coworker["cost"]
        coworker["expected"] = expected_payment
        # Adjust the fairness score based on the difference.  Fairness is determined by how much coworker has payed minus how much they would pay for themselves.
        coworker["fairness"] = coworker["paid"] - expected_payment

# Next payer is determined by who has the lowest fairness score.
def find_next_payer(coworkers):
    calculate_expected_payments(coworkers)
    # Sort coworkers by their fairness score
    sorted_coworkers = sorted(coworkers, key=lambda x: x.get("fairness", 0))
    return sorted_coworkers[0]["name"]


def update_payment(coworkers, payer_name):
    total_cost = sum(coworker["cost"] for coworker in coworkers)
    for coworker in coworkers:
        if coworker["name"] == payer_name:
            coworker["paid"] += total_cost
            break

# Saving to output file to use on next day
def save_coworkers(coworkers, outfile_name):
    with open(outfile_name, "w") as output_file:
        json.dump(coworkers, output_file, indent=4)

def main():
    preference = input("Do you want to use the previous coffee order file? [y/n] ")
    if preference.lower() == "y":
        input_json = input("Please enter the previous coffee order file (MM_DD_YYYY.json): ")
    else:
        input_json = "default.json"
    
    coworkers = load_coworkers(input_json)

    change_preference = input("Do you want to change the favorite coffee and cost fields for any coworkers? [y/n] ")
    if change_preference.lower() == "y":
        coworker_name = input("Enter the name of the coworker you want to update: ")
        for coworker in coworkers:
            if coworker["name"] == coworker_name:
                coworker["fav_coffee"] = input(f"Enter the new favorite coffee for {coworker['name']}: ")
                coworker["cost"] = float(input(f"Enter the new cost for {coworker['name']}'s coffee: "))
                break

    payer_name = find_next_payer(coworkers)
    print(f"{payer_name} should pay for the coffee this time.")
    update_payment(coworkers, payer_name)

    now = datetime.now()
    date_time = now.strftime("%m_%d_%Y")
    outfile_name = f"{date_time}.json"
    
    save_coworkers(coworkers, outfile_name)
    print(f"Coworkers' payment information has been saved to {outfile_name}.")

if __name__ == "__main__":
    main()
