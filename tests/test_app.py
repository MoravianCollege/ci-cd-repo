
from cicdrepo.app import app


def test_get_go():
    app.config['TESTING'] = True
    client = app.test_client()

    result = client.get('/go')
    assert b'Hello, World!' in result.data
