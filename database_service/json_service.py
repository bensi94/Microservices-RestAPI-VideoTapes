# This class is made to read SC-T-302-HONN_2018_Friends.json and
# SC-T-302-HONN_2018_Videotapes into list of entity classes

import json
from entity_classes.user import User
from entity_classes.tape import Tape
from entity_classes.borrow import Borrow

class Json_service:

    user_list = []
    tape_list = []
    borrow_list = []

    def read_json(self):
        with open('files/SC-T-302-HONN_2018_Friends.json', 'r') as file:
            friends = json.load(file)
        
        with open('files/SC-T-302-HONN_2018_Videotapes.json', 'r') as file:
            tapes = json.load(file)

        # Because borrows don't have unique ids we have to greate one
        current_borrow_id = 1

        # Create users 
        for friend in friends:
            user_id = friend['id']
            first_name = friend['first_name']
            last_name = friend['last_name']
            email = friend['email']
            phone = friend['phone']
            address = friend['address']

            user = User(user_id, first_name, last_name, email, phone, address)
            self.user_list.append(user)

            # Only for friends that have borrowed tapes
            if 'tapes' in friend:
                for tape in friend['tapes']:
                    tape_id = tape['id']
                    borrow_date = tape['borrow_date']
                    return_date = tape['return_date']
                    borrow = Borrow(current_borrow_id, user_id, tape_id, borrow_date, return_date)
                    current_borrow_id += 1
                    self.borrow_list.append(borrow)
        
        # Create tapes
        for tape in tapes:
            tape_id = tape['id']
            title = tape['title']
            first_name = tape['director_first_name']
            last_name = tape['director_last_name']
            type = tape['type']
            release_date = tape['release_date']
            eidr = tape['eidr']
            tape = Tape(tape_id, title, first_name, last_name, type, release_date, eidr)
            self.tape_list.append(tape)
             
    def get_users(self):
        return self.user_list

    def get_tape_list(self):
        return self.tape_list
    
    def get_borrow_list(self):
        return self.borrow_list


