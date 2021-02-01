import random
import pandas as pd
import re
from faker import Faker


class DataGenerator():
    '''
    The purpose of this class is to fake some name and address data in order to improve support.
    '''
    def __init__(self, max_nb_chars=80, n=1000, seed=369):
        random.seed(seed)
        # Set the seed value of the shared `random.Random` object
        # across all internal generators that will ever be created
        Faker.seed(seed)

        self.n = n
        self.max_nb_chars = max_nb_chars
        self.fake = Faker()
        # Creates and seeds a unique `random.Random` object for
        # each internal generator of this `Faker` instance
        self.fake.seed_instance(0)
        # Creates and seeds a unique `random.Random` object for
        # the en_US internal generator of this `Faker` instance
        self.fake.seed_locale('en_US', 0)

        self.fake_names = []
        self.fake_addresses = []
        self.fake_lines = []

    def insert_entity_span(self, text, entity):
        words = text.split()
        random_position = random.randint(0,len(words)-1)
        prefix = " ".join(words[:random_position])
        posix = " ".join(words[random_position:])
        new_text = prefix + f" {entity} " + posix
        return new_text.strip()

    def generate_fake_data(self):
        self.fake_names = []
        self.fake_addresses = []
        self.fake_lines = []
        for i in range(0,self.n):
            self.fake_names.append(self.fake.name())
            self.fake_addresses.append(self.fake.address().replace("\n"," "))

        # add some special part addresses to train data in the following formats:
        # Apt. 123

        additional_addresses = ["Apt. " + f"{random.randint(10,9999)}" for _ in range(0, self.n // 20 )] + \
            ["Apt ." + f"{random.randint(10,3999)}" for _ in range(0, self.n // 20 )] + \
            ["Apt . " + f"{random.randint(10,3999)}" for _ in range(0, self.n // 20 )] + \
            ["Apt " + f"{random.randint(10,3999)}"  for _ in range(0, self.n // 20 )]
        for i in range(0,self.n*2):
            self.fake_lines.append(self.fake.text(max_nb_chars=self.max_nb_chars))
        self.fake_addresses.extend(additional_addresses)

        generated_data = []
        for i in range(0,self.n):
            candidate_name = self.fake_names[random.randint(0,len(self.fake_names) -1)]
            candidate_line = self.fake_lines[random.randint(0,len(self.fake_lines) -1)]
            generated_data.append(
                {
                    "Text": self.insert_entity_span(candidate_line, candidate_name),
                    "Labels": "Name",
                    "PII": candidate_name
                }
            )

            candidate_address = self.fake_addresses[random.randint(0,len(self.fake_addresses)-1)]
            candidate_line = self.fake_lines[random.randint(0,self.n*2-1)]

            generated_data.append(
                {
                    "Text": self.insert_entity_span(candidate_line, candidate_address),
                    "Labels": "Address",
                    "PII": candidate_address
                }
            )

        return pd.DataFrame(generated_data)

