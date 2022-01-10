"""the module root - imported when importing python_test"""


def square(x: int) -> int:
    """square a number"""
    return x**2


def is_one(x: str | int) -> bool:
    """check if a value is one"""
    return x in ("1", 1)


def isnt_one(x: str | int) -> bool:
    """kinda self explanatory"""
    return not is_one(x)


def start() -> None:
    """entry point"""
    print("running package!")
