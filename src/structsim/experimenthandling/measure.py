class Measure:
    """Key-value pair for extracted simulation result measures."""

    def __init__(self, key: str, value: str) -> None:
        self._key = key
        self._value = value

    def __str__(self) -> str:
        return f"Key : {self._key} Value : {self._value}"

    def get_value(self) -> str:
        return self._value

    def set_value(self, value: str) -> None:
        self._value = value

    def get_key(self) -> str:
        return self._key

    def set_key(self, key: str) -> None:
        self._key = key
