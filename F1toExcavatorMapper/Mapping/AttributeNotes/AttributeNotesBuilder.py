import os

import pandas as pd

from F1toExcavatorMapper.Utils.Singleton import Singleton


@Singleton
class AttributeNotesBuilder:
    taken_prefixes = []

    def __init__(self):
        self.current_incrementer = 0

    def map(self, data, source_type):
        self.current_incrementer = 0
        data.loc[:, 'note_id'] = pd.Series("", index=data.index)

        #generate unused prefix
        random_prefix = pd.np.random.randint(low=1000, high=99999999)
        while self.is_id_collision(random_prefix, len(data.index)):
            random_prefix = pd.np.random.randint(low=1000, high=99999999)
        self.taken_prefixes.append(random_prefix)
        data['note_id'] = data['note_id'].apply(self.get_sequential_id, args=(random_prefix,))
        return data

    def get_sequential_id(self, value, current_prefix):
        note_id = current_prefix + self.current_incrementer
        self.current_incrementer += 1
        return note_id

    def is_id_collision(self, starting_value, length):
        for existing_prefix in self.taken_prefixes:
            if starting_value <= existing_prefix <= starting_value+length:
                return True
        return False
