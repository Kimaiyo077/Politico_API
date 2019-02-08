class PartyModel:
    '''an instance of the data structures that are required to to strore party data'''
    parties_db = []

    def __init__(self, name, hqAddress, logoUrl):
        self.name = name
        self.hqAddress = hqAddress
        self.logoUrl = logoUrl
        self.id = len(parties_db) + 1

class OfficeModel:
    '''an instance of the data structure that is required to strore office data'''
    offices_db = []

    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.id = len(offices_db) + 1
