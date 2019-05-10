
from cicdrepo import main


def test_go():
    assert main.go() == 'Hello World!'
