import random


def spin_wheel() -> str:

    chances = {"<:shining:1144089713934864444>": 0.05, "<:glowing:1144089680934080512>": 0.12, "<:common:1144089649174814730>": 0.83}
    
    # Generate a random number between 0 and 1
    random_number = random.random()
    
    # Initialize a variable to keep track of the cumulative probability
    cumulative_probability = 0
    
    # Iterate through the chances and select a value based on the probabilities
    for value, probability in chances.items():
        cumulative_probability += probability
        if(random_number < cumulative_probability):
            return value

    return ""