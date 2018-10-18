from datetime import datetime

class Tape:
    def __init__(self, id, title, director_first_name, 
                director_last_name, type, release_date, eidr):
        self.id = int(id)
        self.title = title
        self.director = director_first_name + ' ' + director_last_name
        self.type = type
        self.release_date = datetime.strptime(release_date, '%Y-%m-%d')
        self.eidr = eidr

