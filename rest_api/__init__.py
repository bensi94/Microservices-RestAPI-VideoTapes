from flask import Flask
from sqlalchemy import create_engine

db = create_engine('postgresql+psycopg2://aslakur:1234@db/video_tapes')

app = Flask(__name__)

@app.route("/")
def index():
    print(db.execute("SELECT * FROM films"))
    return ("HELLO WORLD")
