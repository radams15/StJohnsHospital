import json
from EncryptedJsonFile import EncryptedJsonFile



class PatientDataDao(EncryptedJsonFile):
    def __init__(self, file, key):
        super().__init__(file, key, encrypted=False)
