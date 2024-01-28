"""
A simple test script for hello_world.py.
"""
from src import hello_world


def test_hello_world_output():
    """
    Tests the output of hello_world2() function.
    """
    assert hello_world.hello_world2() == 'Hello World'
