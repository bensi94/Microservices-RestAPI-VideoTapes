class User:
    def __init__(self, id=None, first_name=None, 
                last_name=None, email=None, phone=None, address=None, input_tuple=None):
        
        if input_tuple is None:
            self.id = int(id)
            self.name = first_name + ' ' + last_name
            self.email = email
            self.phone = phone
            self.address = address
        else:
            self.id = int(input_tuple[0])
            self.name = input_tuple[1]
            self.email = input_tuple[2]
            self.phone = input_tuple[3]
            self.address = input_tuple[4]

    def return_as_dict(self):
        user = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
        }
        return user