# fruits = ["apple", "banana", "orange"]
# fruits[0] = "mango"
# print(fruits)  # ["mango", "banana", "orange"]

# # Add items
# fruits.append("grape")
# print(fruits)
# fruits.insert(1, "kiwi")    # Insert at position
# print(fruits)
# # Remove items
# fruits.remove("grape")     # Remove by value
# print(fruits)
# last = fruits.pop()        # Remove and return last
# print(last)
# del fruits[0]              # Remove by index
# print(fruits)


# numbers = [3, 1, 4, 1, 5, 9]

# # Information
# print(len(numbers))         # 6 (length)
# print(numbers.count(3))     # 2 (count occurrences)
# print(numbers.index(4))     # 2 (find position)

# # Sorting
# numbers.sort()              # Sort in place
# print(numbers)              # [1, 1, 3, 4, 5, 9]

# numbers.reverse()           # Reverse order
# print(numbers)              # [9, 5, 4, 3, 1, 1]

# # Copy
# new_list = numbers.copy()   # Create a copy
# print(new_list)     

# # fruits = ["apple", "banana", "orange"]


# # Check if item exists
# if "apple" in fruits:
#     print("Found apple!")

# fruits = []
# # Check if list is empty
# if fruits:
#     print("List has items")
# else:
#     print("List is empty")
    
# my_dict = {}
# print(my_dict)
# print(type(my_dict))  # <class 'dict'>
# # Dictionary with data
# person = {
#     "name": "Alice",
#     "age": 30,
#     "city": "New York"
# }

# print(person)
# # Different ways to create
# scores = dict(math=95, english=87, science=92)    
# print(scores)


# person = {"name": "Alice", "age": 30, "city": "New York"}
# # print(person)       # "Alice"
# # Get values by key
# # print(person["name"])       # "Alice"
# # print(person["age"])        # 30

# # Safer with get()
# print(person.get("job"))    # None (no error)
# print(person.get("job", "Unknown"))  # "Unknown" (default)

# person = {"name": "Alice", "age": 30}
# print(person)
# # Add or update
# person["email"] = "alice@email.com"  # Add new
# print(person)
# person["age"] = 31                   # Update existing
# print(person)
# # Remove items
# del person["email"]              # Remove by key
# print(person)
# age = person.pop("age")          # Remove and return
# print(age)
# person.clear()                   # Remove all items
# print(person)

# person = {"name": "Alice", "age": 30, "city": "New York"}
# print(person)
# # Get all keys, values, or items
# print(person.keys())    # dict_keys(['name', 'age', 'city'])
# print(person.values())  # dict_values(['Alice', 30, 'New York'])
# print(person.items())   # dict_items([('name', 'Alice'), ...])

# # Check if key exists
# if "name" in person:
#     print("Name found!")

# # Update multiple values
# person.update({"age": 31, "job": "Engineer"})
# print(person)


# # Dictionary of dictionaries
# students = {
#     "alice": {"age": 20, "grade": "A"},
#     "bob": {"age": 21, "grade": "B"},
#     "charlie": {"age": 19, "grade": "A"}
# }
# print(students)  # "A"
# # Access nested data
# print(students["alice"]["grade"])  # "A"


# # Empty tuple
# empty = ()
# print(empty)
# # Tuple with items
# point = (3, 5)
# print(point)
# colors = ("red", "green", "blue")
# print(colors)
# # Single item tuple needs comma!
# single = (42,)  # Note the comma
# print(single)
# not_tuple = (42)  # This is just 42 in parentheses
# print(not_tuple)
# # Without parentheses (implicit)
# coordinates = 10, 20
# print(coordinates)

# point = (3, 5)
# print(point)      # 3
# colors = ("red", "green", "blue")
# print(colors)      # 3
# # Get items
# print(point[-1])      # 3
# print(colors[-1])    # "blue"

# # Slicing works too
# print(colors[0:2])   # ("red", "green")

# point = (3, 5)
# print(point)
# x, y = point  # x = 3, y = 5
# print(f"x:{x}, y:{y}")
# # Multiple assignment
# a, b, c = 1, 2, 3  # Same as (1, 2, 3)
# print(f"a:{a}, b:{b}, c:{c}")
# # Swap variables elegantly
# x, y = y, x  # Swaps values!
# print(f"x:{x}, y:{y}")


# empty_set = set()  # NOT {} - that's a dict!
# print(empty_set)
# # Set with values - both ways work
# numbers = {1, 2, 3, 4, 5}
# print(numbers)
# fruits = set(["apple", "banana", "orange"])
# print(fruits)
# # From a list (removes duplicates)
# scores = [85, 90, 85, 92, 90]
# print(scores)
# unique_scores = set(scores)  # {85, 90, 92}
# print(unique_scores)

# colors = {"red", "blue"}
# print(colors)
# # Add items
# colors.add("green")
# print(colors)  # {'red', 'blue', 'green'}

# # Remove items
# colors.remove("blue")    # Error if not found
# print(colors)
# colors.discard("blue")    # Error if not found
# print(colors)
# colors.discard("yellow") # No error if not found
# print(colors)

# # Check membership
# if "red" in colors:
#     print("Red is available")
    
    
# # This function only prints
# def add_print(a, b):
#     print(a + b)

# # This function returns a value
# def add_return(a, b):
#     return a + b

# # Now you can use the result
# result = add_return(5, 3)
# print(f"The result is {result}")  # The result is 8    

# def double(number):
#     return number * 2

# # Store in variable
# result = double(5)

# # Use in expressions
# total = double(5) + double(3)  # 10 + 6 = 16

# # Pass to other functions
# print(double(10))  # 20

# # Use in conditions
# if double(7) > 10:
#     print("Big number!")
    
# import random

# # Use module functions
# number = random.randint(1, 10)
# print(f"Random number: {number}")
# choice = random.choice(["apple", "banana", "orange"])
# print(f"Random choice: {choice}")

# # Date and time
# import datetime
# today = datetime.date.today()
# print(today)  # 2024-01-15

# import os
# current_dir = os.getcwd()
# print(current_dir)

# # JSON data
# import json
# data = {"name": "Alice", "age": 30}
# json_string = json.dumps(data)
# print(json_string)  # {"name": "Alice", "age": 30}
# parsed_data = json.loads(json_string)
# print(parsed_data)  # {'name': 'Alice', 'age': 30}

# # Import entire module
# import math
# result = math.sqrt(16)
# print(f"result:{result}")  # 4.0
# # Import specific functions
# from math import sqrt, pi
# result = sqrt(16)
# print(f"result:{result}")  # 4.0
# circle_area = pi * radius ** 2
# print(f"circle_area:{circle_area}")  # 4.0
# # Import with alias
# import pandas as pd
# df = pd.DataFrame(data)

# # Import everything (avoid this!)
# from math import *


# import requests

# # We need coordinates to get weather data
# latitude = 48.85   # Paris latitude
# longitude = 2.35   # Paris longitude

# # Build the API URL with our parameters
# url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m"

# # Make the request
# response = requests.get(url)
# print(f"response:{response}")
# print(f"response.status_code:{response.status_code}")
# data = response.json()
# print(f"type(response.json()):{type(response.json())}")
# print(f"data:{data}")
# print(f"type(data):{type(data)}")
# print(f"data.keys():{data.keys()}")
# print(f"data.values():{data.values()}")


import requests

def get_weather(latitude, longitude):
    response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m")
    data = response.json()
    return data['current']['temperature_2m']

# Get temperature for different cities
paris_temp = get_weather(48.85, 2.35)
london_temp = get_weather(51.50, -0.12)
tokyo_temp = get_weather(35.68, 139.69)

print(f"Paris: {paris_temp}°C")
print(f"London: {london_temp}°C")
print(f"Tokyo: {tokyo_temp}°C")

import requests
from datetime import datetime, timedelta

# Calculate dates
today = datetime.now()
week_ago = today - timedelta(days=7)

# Format dates for API (YYYY-MM-DD)
start_date = week_ago.strftime("%Y-%m-%d")
end_date = today.strftime("%Y-%m-%d")

# Get Paris weather for past week
url = f"https://api.open-meteo.com/v1/forecast?latitude=48.85&longitude=2.35&start_date={start_date}&end_date={end_date}&daily=temperature_2m_max,temperature_2m_min"

response = requests.get(url)
data = response.json()
print(data)

import pandas as pd

# Extract the daily data
daily_data = data['daily']

# Create a DataFrame
df = pd.DataFrame({
    'date': daily_data['time'],
    'max_temp': daily_data['temperature_2m_max'],
    'min_temp': daily_data['temperature_2m_min']
})

# Convert date strings to datetime
df['date'] = pd.to_datetime(df['date'])

print(df)

import matplotlib.pyplot as plt

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(df['date'], df['max_temp'], marker='o', label='Max Temp')
plt.plot(df['date'], df['min_temp'], marker='o', label='Min Temp')

# Add labels and title
plt.xlabel('Date')
plt.ylabel('Temperature (°C)')
plt.title('Paris Weather - Past 7 Days')
plt.legend()

# Rotate x-axis labels for readability
plt.xticks(rotation=45)
plt.tight_layout()

# Save the plot
plt.savefig('weather_chart.png')
plt.show()

import os

# Create data folder if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')

# Save to CSV
df.to_csv('data/paris_weather.csv', index=False)
print("Data saved to data/paris_weather.csv")