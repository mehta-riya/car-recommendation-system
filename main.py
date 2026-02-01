import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Optional
import os

class CarRecommendationSystem:
    def __init__(self, csv_file_path: str):
        """
        Initializes the car recommendation system by loading data from a CSV file.
        Includes error handling for file not found or other loading issues.
        """
        try:
            # Check if the file exists before attempting to read
            if not os.path.exists(csv_file_path):
                raise FileNotFoundError(f"The file '{csv_file_path}' does not exist.")

            self.df = pd.read_csv(csv_file_path)
            
            # --- DEBUGGING LINE: Print the raw column names from your CSV ---
            print(f"Initial columns detected: {self.df.columns.tolist()}")

            self.prepare_data()
            
            if self.df.empty:
                print("The dataset is empty after cleaning. Please check your CSV file for data or formatting issues.")
            else:
                print(" Car Database Loaded Successfully!")
                print(f" Total Cars Available: {len(self.df)}")
        except FileNotFoundError as e:
            print(f" Error: {e}")
            print("Please make sure the CSV file is in the same folder as this script.")
            exit(1)
        except Exception as e:
            print(f"Error loading data: {e}")
            print("Please check the format and contents of your CSV file.")
            exit(1)

    def prepare_data(self):
        """
        Cleans and preprocesses the car data.
        - Renames columns for easier access.
        - Converts data types for numerical columns like Price.
        - Removes rows where the price value is missing or invalid.
        """
        # Rename columns to a more standard format
        self.df.columns = self.df.columns.str.lower().str.replace(' ', '_')
        
        # Convert 'price' to a numerical type, handling any non-numeric characters
        self.df['price'] = pd.to_numeric(
            self.df['price'].astype(str).str.replace('[$,]', '', regex=True),
            errors='coerce'
        )
        
        # Drop rows where 'price' conversion failed (are now NaN)
        self.df.dropna(subset=['price'], inplace=True)
        # Drop rows where 'seats' is missing, as it's a key preference
        self.df.dropna(subset=['seats'], inplace=True)
        # Convert 'seats' to an integer type
        self.df['seats'] = pd.to_numeric(self.df['seats'], errors='coerce')

        print(" Data cleaning and preprocessing complete!")

    def get_recommendations(
        self,
        budget: float,
        transmission_type: Optional[str] = None,
        body_type: Optional[str] = None,
        fuel_type: Optional[str] = None,
        num_seats: Optional[int] = None,
        brand: Optional[str] = None,
        num_results: int = 5
    ) -> pd.DataFrame:
        """
        Recommends cars based on user's preferences.
        
        Args:
            budget (float): The maximum budget for the car.
            transmission_type (str): 'Manual', 'Auto' or 'Manual / Auto'
            body_type (str): 'Hatchback', 'Sedan', 'SUV', 'MUV', etc.
            fuel_type (str): 'Petrol', 'Diesel', 'Hybrid'.
            num_seats (int): Number of seats in the car.
            brand (str): Specific brand name (e.g., 'Maruti Suzuki').
            num_results (int): The number of top recommendations to return.
        
        Returns:
            pd.DataFrame: A DataFrame containing the recommended cars, sorted by price.
        """
        # Start with all cars that fit the budget
        recommendations_df = self.df[self.df['price'] <= budget].copy()

        # Define the criteria for filtering. We'll use this list later for the match score.
        criteria = {
            'brand': brand,
            'transmission': transmission_type,
            'body': body_type,
            'fuel': fuel_type,
            'seats': num_seats
        }
        
        # Remove criteria with no preference (None)
        active_criteria = {key: value for key, value in criteria.items() if value is not None}

        # Filter the DataFrame based on user preferences
        for key, value in active_criteria.items():
            if key == 'seats':
                recommendations_df = recommendations_df[recommendations_df[key] == value]
            else:
                recommendations_df = recommendations_df[
                    recommendations_df[key].str.contains(str(value), case=False, na=False)
                ]

        if recommendations_df.empty:
            print(f" No cars found matching your criteria.")
            return pd.DataFrame()

        # Calculate a 'match_score' for each car based on the number of criteria met.
        def calculate_match_score(row):
            score = 0
            # We don't include budget in the score as it's a hard filter
            for key, value in active_criteria.items():
                if key == 'seats':
                    if row[key] == value:
                        score += 1
                else:
                    if str(value).lower() in str(row[key]).lower():
                        score += 1
            
            if len(active_criteria) > 0:
                return (score / len(active_criteria)) * 100
            else:
                return 0

        recommendations_df['match_score'] = recommendations_df.apply(calculate_match_score, axis=1)

        # Sort the results by price and then by match score
        sorted_recommendations = recommendations_df.sort_values(
            by=['price', 'match_score'], 
            ascending=[True, False]
        )
        
        return sorted_recommendations.head(num_results)

def display_menu_box(title, options):
    """
    Displays a list of options within a stylized box.
    """
    # Add "No preference" as the first option
    menu_options = ["No preference"] + [str(opt) for opt in options]
    
    # Calculate the box width based on the longest option
    max_length = max(len(f"{i}. {opt}") for i, opt in enumerate(menu_options))
    box_width = max(max_length + 6, len(title) + 6)
    
    # Print the top border
    print("-" * box_width)
    # Print the title, centered
    print(f"|{title.center(box_width - 2)}|")
    # Print the separator
    print("-" * box_width)

    # Print each option
    for i, opt in enumerate(menu_options):
        if i == 0:
            print(f"| 0. {opt.ljust(box_width - 6)}|")
        else:
            print(f"| {i}. {opt.ljust(box_width - 6)}|")

    # Print the bottom border
    print("-" * box_width)

def get_user_preferences(recommender: CarRecommendationSystem):
    """
    Gets car preferences from the user via a menu-driven interface.
    Returns a dictionary of selected options.
    """
    preferences = {}
    
    # Get Budget
    while True:
        try:
            budget = float(input(" Please enter your maximum budget (e.g., 1500000): "))
            preferences['budget'] = budget
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    
    # Get all unique values from the dataset for the menus
    unique_brands = sorted(recommender.df['brand'].unique())
    unique_transmissions = sorted(recommender.df['transmission'].unique())
    unique_bodies = sorted(recommender.df['body'].unique())
    unique_fuels = sorted(recommender.df['fuel'].unique())
    unique_seats = sorted(recommender.df['seats'].unique())
    
    # --- Brand Selection ---
    display_menu_box("Brand Selection", unique_brands)
    while True:
        try:
            choice = int(input("Enter the number for your preferred brand: "))
            if 0 <= choice <= len(unique_brands):
                preferences['brand'] = unique_brands[choice - 1] if choice != 0 else None
                break
            else:
                print("Invalid choice. Please enter a valid brand.")
        except (ValueError, IndexError):
            print("Invalid input. Please enter a valid brand.")

    # --- Transmission Selection ---
    display_menu_box("Transmission Type", unique_transmissions)
    while True:
        try:
            choice = int(input("Enter the number for your preferred transmission: "))
            if 0 <= choice <= len(unique_transmissions):
                preferences['transmission_type'] = unique_transmissions[choice - 1] if choice != 0 else None
                break
            else:
                print("Invalid choice. Please enter a valid transmission type.")
        except (ValueError, IndexError):
            print("Invalid input. Please enter a valid transmission type.")
    
    # --- Body Type Selection ---
    display_menu_box("Body Type", unique_bodies)
    while True:
        try:
            choice = int(input("Enter the number for your preferred body type: "))
            if 0 <= choice <= len(unique_bodies):
                preferences['body_type'] = unique_bodies[choice - 1] if choice != 0 else None
                break
            else:
                print("Invalid choice. Please enter a valid body type.")
        except (ValueError, IndexError):
            print("Invalid input. Please enter a valid body type.")

    # --- Fuel Type Selection ---
    display_menu_box("Fuel Type", unique_fuels)
    while True:
        try:
            choice = int(input("Enter the number for your preferred fuel type: "))
            if 0 <= choice <= len(unique_fuels):
                preferences['fuel_type'] = unique_fuels[choice - 1] if choice != 0 else None
                break
            else:
                print("Invalid choice. Please enter a valid fuel type.")
        except (ValueError, IndexError):
            print("Invalid input. Please enter a valid fuel type.")

    # --- Number of Seats Selection ---
    display_menu_box("Number of Seats", unique_seats)
    while True:
        try:
            choice = int(input("Enter the number for your preferred number of seats: "))
            if 0 <= choice <= len(unique_seats):
                preferences['num_seats'] = unique_seats[choice - 1] if choice != 0 else None
                break
            else:
                print("Invalid choice. Please enter a valid number.")
        except (ValueError, IndexError):
            print("Invalid input. Please enter a valid number.")
    
    return preferences

def recommendation_logic(recommender, user_preferences):
    """
    Performs the recommendation logic based on user preferences.
    """
    return recommender.get_recommendations(**user_preferences)

def show_results(recommended_cars):
    """
    Displays the final recommended cars to the user.
    """
    print(f"\n--- Top 5 Recommendations ---")
    if not recommended_cars.empty:
        # Display the new 'match_score' column
        print(recommended_cars[['brand', 'model', 'fuel', 'transmission', 'body', 'seats', 'price', 'match_score']])
    else:
        print("No recommendations to display.")

def compare_cars(recommender):
    """
    Allows the user to select and compare two car models.
    """
    print("\n--- Compare Two Car Models ---")
    
    # Get details for the first car
    car1_brand = input("Enter the brand of the first car: ")
    car1_model = input("Enter the model of the first car: ")
    
    # Get details for the second car
    car2_brand = input("Enter the brand of the second car: ")
    car2_model = input("Enter the model of the second car: ")
    
    # Filter for the selected cars
    car1_data = recommender.df[
        (recommender.df['brand'].str.lower() == car1_brand.lower()) &
        (recommender.df['model'].str.lower() == car1_model.lower())
    ]
    car2_data = recommender.df[
        (recommender.df['brand'].str.lower() == car2_brand.lower()) &
        (recommender.df['model'].str.lower() == car2_model.lower())
    ]
    
    # Check if both cars were found
    if not car1_data.empty and not car2_data.empty:
        print("\n--- Comparison Results ---")
        # Display the details side-by-side
        comparison_df = pd.concat([car1_data, car2_data], ignore_index=True)
        print(comparison_df.transpose())
    else:
        print("One or both cars were not found in the database. Please check the spelling.")

if __name__ == "__main__":
    # 1. Data load and clean
    recommender = CarRecommendationSystem('CARS_DATASET_WITHOUT.csv')
    
    if not recommender.df.empty:
        while True:
            # 2. Get user preferences
            user_preferences = get_user_preferences(recommender)

            # 3. Recommendation logic
            recommended_cars = recommendation_logic(recommender, user_preferences)

            # 4. Show results
            show_results(recommended_cars)

            # 5. Post-recommendation menu
            print("\nWhat would you like to do next?")
            print("1. Search again")
            print("2. Compare two car models")
            print("3. End the chat")
            
            while True:
                try:
                    choice = int(input("Enter your choice (1, 2, or 3): "))
                    if choice == 1:
                        break  # Breaks the inner loop to start a new search
                    elif choice == 2:
                        compare_cars(recommender)
                        break  # Breaks the inner loop to start a new search
                    elif choice == 3:
                        print("Thank you for using the Car Recommendation System. Goodbye!")
                        exit()
                    else:
                        print("Invalid choice. Please enter 1, 2, or 3.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
    else:
        print("\nCannot proceed with recommendations. Please check the dataset.")

