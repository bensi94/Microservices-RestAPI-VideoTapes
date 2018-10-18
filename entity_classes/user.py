class User:
    def __init__(self, id, first_name, 
                last_name, email, phone, address):
        self.id = int(id)
        self.name = first_name + ' ' + last_name
        self.email = email
        self.phone = phone
        self.address = address
