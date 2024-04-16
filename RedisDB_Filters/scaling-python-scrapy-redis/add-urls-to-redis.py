import redis
from redis import from_url
from dotenv import load_dotenv
import os


load_dotenv()
# Create a redis client
redisClient = redis.from_url(os.getenv('REDIS_CLOUD_KEY'))


def combine_elements(x, y):
    combinations = {}

    for element_y in y:
        for key_x, value_x in x.items():
            combination_name = key_x + ',' + element_y[0]
            combination_value = value_x + element_y[1]
            combinations[combination_name] = combination_value

    return combinations


# Example usage
x = {
    "zachodniopomorskie": "32"
}

y = [
("Szczecin", "61"),
    ("Koszalin", "62"),
    ("Stargard Szczeciński", "63"),
    ("Kołobrzeg", "64"),
    ("białogardzki", "01"),
    ("choszczeński", "02"),
    ("drawski", "03"),
    ("goleniowski", "04"),
    ("gryficki", "05"),
    ("gryfiński", "06"),
    ("kamieński", "07"),
    ("kołobrzeski", "08"),
    ("koszaliński", "09"),
    ("łobeski", "10"),
    ("myśliborski", "11"),
    ("policki", "12"),
    ("pyrzycki", "13"),
    ("sławieński", "14"),
    ("stargardzki", "15"),
    ("szczecinecki", "16"),
    ("świdwiński", "17"),
    ("wałecki", "18")
]

output = combine_elements(x, y)

# Print the output dictionary
links_pref = "https://fundusze.ngo.pl/aktualne?page=1&terc="
for combination, value in output.items():
    link = links_pref + value
    # Push URLs to Redis Queue
    redisClient.lpush('filters_queue:start_urls', link)

dict = {}
for combination, value in output.items():
    dict[value] = combination
print(len(dict))
print(dict)
