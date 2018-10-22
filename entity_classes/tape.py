from datetime import datetime

class Tape:
    def __init__(self, id=None, title=None, director_first_name=None,
                 director_last_name=None, type=None, release_date=None, eidr=None, input_tuple=None, director=None):
        
        if input_tuple is None:
            if id is not None:
                self.id = int(id)
            self.title = title
            if director is None:
                self.director = director_first_name + ' ' + director_last_name
            else:
                self.director = director
            self.type = type
            self.release_date = datetime.strptime(release_date, '%Y-%m-%d')
            self.eidr = eidr
        else:
            self.id = int(input_tuple[0])
            self.title = input_tuple[1]
            self.director = input_tuple[2]
            self.type = input_tuple[3]
            self.release_date = input_tuple[4]
            self.eidr = input_tuple[5]
    

    def return_as_dict(self):
        tape = {
            "id": self.id,
            "title": self.title,
            "director": self.director,
            "type": self.type,
            "release_date": self.release_date,
            "eidr": self.eidr
        }
        return tape
