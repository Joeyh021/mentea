"""testing everything in this file"""

import python_example


def test_funcs():
    assert python_example.square(2) == 4
    assert python_example.is_one(1)
    assert python_example.isnt_one(2)
