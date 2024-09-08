from flask import Flask

app = Flask(__name__)

from db.init_db import CriarDB
from views import *

if __name__ == "__main__":
    CriarDB.novoDB()
    app.run(debug=True)

