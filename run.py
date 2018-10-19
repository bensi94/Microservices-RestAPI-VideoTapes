from rest_api import app
from database.database_service import Database_service

db_service = Database_service()
db_service.init_database()


app.run(host='0.0.0.0', port=80, debug=True)
