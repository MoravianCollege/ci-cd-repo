
from flask import Flask
from cicdrepo.main import go
app = Flask(__name__)


@app.route('/go')
def get_go():
    return str(go())
