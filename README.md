# Car Recommendation System

## Overview
The Car Recommendation System is a Python-based command-line application designed to recommend cars based on user-defined preferences. The system analyzes a structured car dataset and filters results using criteria such as budget, brand, transmission type, body type, fuel type, and seating capacity.

In addition to recommendations, the system also supports side-by-side comparison of two car models, helping users make informed decisions.

---

## Key Features
- Budget-based car filtering
- Menu-driven user input for easy interaction
- Recommendations based on multiple user preferences
- Match score calculation to indicate relevance of recommendations
- Data cleaning and preprocessing for reliable results
- Comparison of two car models
- Robust error handling for invalid inputs and missing data

---

## Technologies Used
- Python 3
- Pandas
- NumPy
- CSV dataset

---

## Project Structure
CAR-RECOMMENDATION-SYSTEM-main/
│
├── main.py
├── CARS_DATASET_WITHOUT.csv
├── requirements.txt
└── README.md


---

## System Workflow
1. The car dataset is loaded from a CSV file and cleaned to ensure consistency.
2. The user is prompted to enter a maximum budget.
3. The user selects preferences through a menu-based interface.
4. Cars are filtered based on budget and selected criteria.
5. A match score is calculated for each car based on how many preferences it satisfies.
6. The top matching cars are displayed, sorted by price and relevance.
7. The user may repeat the search, compare two cars, or exit the application.

---

## How to Run the Project

### Prerequisites
- Python 3.x installed

### Steps
1. Clone the repository:
https://github.com/mehta-riya/car-recommendation-system.git

2. Navigate to the project directory:
cd CAR-RECOMMENDATION-SYSTEM-main

3. Install the required dependencies:
pip install -r requirements.txt

4. Run the application:
python main.py


---

## User Input Parameters
- Budget (mandatory)
- Brand (optional)
- Transmission type (optional)
- Body type (optional)
- Fuel type (optional)
- Number of seats (optional)

All optional preferences can be skipped by selecting “No preference” from the menu.

---

## Output
The system displays a table containing:
- Brand
- Model
- Fuel type
- Transmission
- Body type
- Seating capacity
- Price
- Match score (percentage)

---

## Error Handling
- Handles missing or incorrectly named CSV files
- Validates numerical inputs and menu selections
- Displays informative messages when no recommendations match the criteria

---

## Future Enhancements
- Integration of machine learning–based recommendation logic
- Web-based interface using Streamlit or Flask
- Additional ranking factors such as mileage and safety ratings
- Personalized recommendations based on user preferences and usage patterns

---

## Authors
-RIYA MEHTA 
-HIMESH MEHTA 
-OM GHAG 
-POOJAN MODI
-AYAZ MEMOM


