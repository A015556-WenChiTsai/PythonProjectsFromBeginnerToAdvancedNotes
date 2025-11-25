import random
OPERATORS = ["+", "-", "*"]
MIN_OPERAND = 3
MAX_OPERAND = 12
TOTAL_PROBLEMS = 10
left = random.randint(MIN_OPERAND, MAX_OPERAND)
right = random.randint(MIN_OPERAND, MAX_OPERAND)
operator = random.choice(OPERATORS)
expr = str(left) + " " + operator + " " + str(right)
print(f"Generated problem: {expr}")
print(f"Answer: {eval(expr)}")