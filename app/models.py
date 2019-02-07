class PartyModel:
    parties_db = []

    def __init__(self, name, hqAddress, logoUrl):
        self.name = name
        self.hqAddress = hqAddress
        self.logoUrl = logoUrl
        self.id = len(parties_db) + 1

class OfficeModel:
    offices_db = []

    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.id = len(offices_db) + 1
