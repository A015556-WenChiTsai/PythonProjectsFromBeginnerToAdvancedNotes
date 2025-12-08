import requests

# Download a web page
response = requests.get("https://api.github.com")
print(response.status_code)  # Should print 200
print(80 * "*")


def multiply(*numbers):
    total = 1
    for number in numbers:
        total *= number
    return total


print(multiply(2, 3, 4, 5))
print("Hello")

name = "Alice"
name = "555"
age = 25
print(age)
is_student = True
print(is_student)
# 2age=30
# my-name = "Dave"
# my name = "Dave"
# class = "Python"
# name = Alice
"""
    註解是用來解釋為什麼而不是什麼
"""

1 + 1
1 * 9
total = 10 - 7
print(total)

string = "Hello, " + "world!"
print(string)
my_long_string = """
This is a long string
that spans multiple lines.
It preserves the line breaks and spaces.
"""
print(my_long_string)
first_name = "John"
last_name = "Doe"
full_name = first_name + " " + last_name
long_dash = "-" * 40
print(full_name)
print(long_dash)
print(len(long_dash))

is_logged_in = True
is_admin = False
has_permission = True
print(
    f"is_logged_in:{is_logged_in}, is_admin:{is_admin}, has_permission:{has_permission}"
)


is_ready = True

# From comparisons
age = 17
can_vote = age >= 18  # True

score = 75
passed = score > 60  # True
print(f"can_vote:{can_vote}, passed:{passed}")

age = 25

# Equality
print(age == 25)  # True - equals
print(age != 30)  # True - not equals

# Greater/Less than
print(age > 20)  # True - greater than
print(age < 30)  # True - less than
print(age >= 25)  # True - greater or equal
print(age <= 25)  # True - less or equal

age = 18

print(age == 18)  # True  - Equal to
print(age != 21)  # True  - Not equal to
print(age > 17)  # True  - Greater than
print(age < 20)  # True  - Less than
print(age >= 18)  # True  - Greater than or equal
print(age <= 18)  # True  - Less than or equal

age = 25
has_license = True

# AND - both must be true
can_drive = age >= 16 and has_license
print(can_drive)  # True

# OR - at least one must be true
day = "Saturday"
is_weekend = day == "Saturday" or day == "Sunday"
print(is_weekend)  # True

# NOT - reverses the value
is_adult = age >= 18
is_child = not is_adult
print(is_child)  # False

name = "Alice"
string = f"Hello, {name}!"
print(string)  # Output: Hello, Alice!
string = "Hello, {name}!"
print(string)

text = "Python Programming"

print(text.lower())  # "python programming"
print(text.upper())  # "PYTHON PROGRAMMING"
print(text.title())  # "Python Programming"

messy = "  hello world  "
print(messy.strip())  # "hello world" (removes whitespace)

price = "$19.99"
print(price.strip("$"))  # "19.99"


message = "I love Python programming with Python"

# Check if something exists
print("Python" in message)  # True
print(message.startswith("I"))  # True
print(message.endswith("Python"))  # True

# Find position
print(message.find("Python"))  # 7 (first occurrence)
print(message.count("Python"))  # 2 (number of times)

# Replace
new_message = message.replace("Python", "JavaScript")
print(new_message)  # "I love JavaScript programming with JavaScript"

score = 85

if score >= 90:
    print("A - Excellent!")
elif score >= 80:
    print("B - Good job!")
elif score >= 70:
    print("C - Keep it up!")
else:
    print("F - Need improvement")

for i in range(5):
    print(f"Iteration {i}")

for i in range(1, 7):
    print(f"Iteration {i}")

for i in range(0, 10, 2):
    print(f"Iteration {i}")

my_list = []

# List with items
fruits = ["apple", "banana", "orange"]
print(f"fruits: {fruits}")
numbers = [1, 2, 3, 4, 5]
print(f"numbers: {numbers}")
mixed = ["hello", 42, True, 3.14]  # Different types OK!
print(f"mixed: {mixed}")