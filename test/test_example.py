"""testing everything in the python_example module"""

import python_example


def test_funcs() -> None:
    """test the functions in the example"""
    assert python_example.square(2) == 4
    assert python_example.is_one(1)
    assert python_example.isnt_one(2)
