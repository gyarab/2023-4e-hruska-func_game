#file na testing supr python skriptů ----- bajajajo
import random

def generate_random_numbers():
    return random.sample(range(1, 4), 3)

def invert_list(numbers):
    inverted_numbers = [5 - num for num in numbers]
    return inverted_numbers

random_numbers = generate_random_numbers()
print("Random numbers from 1 to 4:", random_numbers)
inverted_numbers = invert_list(random_numbers)
print("Inverted numbers from 4 to 1:", inverted_numbers)