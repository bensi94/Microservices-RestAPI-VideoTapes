from sqlalchemy import create_engine

engine = create_engine('postgresql+psycopg2://scott:tiger@localhost/mydatabase')

