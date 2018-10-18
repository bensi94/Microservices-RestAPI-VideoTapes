from datetime import datetime

class Borrow:
    def __init__(self, id, user_id, tape_id, borrow_date, return_date):
        self.id = int(id)
        self.user_id = int(user_id)
        self.tape_id = int(tape_id)
        self.borrow_date = datetime.strptime(borrow_date, '%Y-%m-%d')

        if return_date == None:
            self.return_date = None
        else:
            self.return_date = datetime.strptime(return_date, '%Y-%m-%d')
