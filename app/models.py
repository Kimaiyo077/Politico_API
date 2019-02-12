class PartyModel:
    '''an instance of the data structures that are required to to strore party data'''
    parties_db = []

    def create_party(data):

        name = data['name'].strip()
        hqAddress = data['hqAddress'].strip()
        logoUrl = data['logoUrl'].strip()
        id = len(PartyModel.parties_db) + 1

        if not name:
            return [400 ,'name cannot be empty']
        elif not hqAddress:
            return [400 ,'hqAddress cannot be empty']
        elif not logoUrl:
            return [400, 'logoUrl cannot be empty']
        
        for party in PartyModel.parties_db:
            if party['name'] == name:
                return [400, 'A party with that name already exists']
        
        #creates a new party filled with all required data.
        new_party = {
            'id' : id,
            'name' : name,
            'hqAddress' : hqAddress,
            'logoUrl' : logoUrl 
        }
    
        #adds new_party to parties_db
        PartyModel.parties_db.append(new_party)

        return [201, new_party]

    def get_all_parties():

        if len(PartyModel.parties_db) <= 0:
            return [404, 'No Parties to be shown']
        else:
            return [200, PartyModel.parties_db]

    def get_specific_party(party_id):

        for party in PartyModel.parties_db:
            if party['id'] == party_id:
                return [200, party]

        return [ 404, 'Party does not exist']
    
    def edit_a_party(party_id, data):
        name = data['name'].strip()

        if not name:
            return [404, 'name cannot be empty']


        for party in PartyModel.parties_db:
            if party['name'] == name:
                return [400, 'name already exists']

        for party in PartyModel.parties_db:
            if party['id'] == party_id:
                party['name'] = name
                return [200, party]

        return [404, 'party not found']

    def delete_specific_party(party_id):
        for party in PartyModel.parties_db:
            if party['id'] == party_id:
                index = party_id - 1
                PartyModel.parties_db.pop(index)
                return [200, 'Party has been succefully deleted']
        
        return [404, 'party not found']

        
class OfficeModel:
    '''an instance of the data structure that is required to strore office data'''
    offices_db = []
    office_types = ['Federal', 'Legislative', 'State', 'Local Government']

    def create_office(data):
        name = data['name'].strip()
        type = data ['type'].strip()
        id = len(OfficeModel.offices_db) + 1

        if not name:
            return [400 ,'name cannot be empty']
        elif not type:
            return [400, 'type cannot be empty']
        elif type not in OfficeModel.office_types:
            return [400, 'type must be either: Federal, Legislative, State or Local Government']
        
        for office in OfficeModel.offices_db:
            if office['name'] == name:
                return [400, 'An office with that name already exists']
        

        new_office = {
            'id': id,
            'name' : name,
            'type' : type
        }

        OfficeModel.offices_db.append(new_office)

        return [201, new_office]

    def get_all_offices():
        if len(OfficeModel.offices_db) <= 0:
            return [404, 'No Offices to be showed']
        else:
            return [200, OfficeModel.offices_db]

    def get_specific_office(office_id):

        for office in OfficeModel.offices_db:
            if office['id'] == office_id:
                return [200, office]

        return [ 404, 'office does not exist']

    def edit_specific_office(office_id, data):
        name = data['name'].strip()

        if not name:
            return [404, 'name cannot be empty']

        for office in OfficeModel.offices_db:
            if office['name'] == name:
                return [400, 'name already exists']

        for office in OfficeModel.offices_db:
            if office['id'] == office_id:
                office['name'] = name
                return [200, office]

        return [404, 'office not found']

    def delete_specific_office(office_id):
        for office in OfficeModel.offices_db:
            if office['id'] == office_id:
                index = office_id - 1
                OfficeModel.offices_db.pop(index)
                return [200, 'Office has been succefully deleted']
        
        return [404, 'office not found']
