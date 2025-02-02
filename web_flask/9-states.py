#!/usr/bin/python3
"""
Script that starts a Flask web application:
Your web application must be listening on 0.0.0.0, port 5000
You must use storage for fetching data from the storage engine
 (FileStorage or DBStorage) => from models import storage and storage.all(...)
To load all cities of a State:
If your storage engine is DBStorage, you must use cities relationship
Otherwise, use the public getter method cities
After each request you must remove the current SQLAlchemy Session:
Declare a method to handle @app.teardown_appcontext
Call in this method storage.close()
Routes:
/states: display a HTML page: (inside the tag BODY)
H1 tag: “States”
UL tag: with the list of all State objects present in DBStorage
    sorted by name (A->Z) tip
LI tag: description of one State: <state.id>: <B><state.name></B>
/states/<id>: display a HTML page: (inside the tag BODY)
If a State object is found with this id:
H1 tag: “State: ”
H3 tag: “Cities:”
UL tag: with the list of City objects linked to the State sorted by name (A->Z)
LI tag: description of one City: <city.id>: <B><city.name></B>
Otherwise:
H1 tag: “Not found!”
You must use the option strict_slashes=False in your route definition
Import this 7-dump to have some data
IMPORTANT
Make sure you have a running and valid setup_mysql_dev.sql
    in your AirBnB_clone_v2 repository (Task)
Make sure all tables are created when you run
    echo "quit" | HBNB_MYSQL_USER=hbnb_dev HBNB_MYSQL_PWD=hbnb_dev_pwd
    HBNB_MYSQL_HOST=localhost
    HBNB_MYSQL_DB=hbnb_dev_db HBNB_TYPE_STORAGE=db
    ./console.py
"""


from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def close(self):
    """Closes connection with db"""
    storage.close()


@app.route("/states", strict_slashes=False)
@app.route("/states/<id>", strict_slashes=False)
def state_w_id(id=None):
    """Returns a list of state objects. If id exists, returns
    a specific state"""
    states = storage.all(State)
    state = None
    if id:
        if "State." + id in states.keys():
            state = states["State." + id]
    return render_template("9-states.html", **(locals()))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
