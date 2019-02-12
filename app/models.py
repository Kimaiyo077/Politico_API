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
