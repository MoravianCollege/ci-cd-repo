
from cicdrepo import main


def test_go():
    assert main.go() == 42
