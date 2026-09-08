class Parameter:
    """Key-value pair representing a simulation parameter."""

    def __init__(self, key: str, value: float) -> None:
        self.key = key
        self._value = value

    @classmethod
    def from_parameter(cls, p: "Parameter") -> "Parameter":
        return cls(p.key, p._value)

    def __str__(self) -> str:
        return f"key : {self.key} value : {self._value}"

    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, value: float) -> None:
        self._value = value

    def get_key(self) -> str:
        return self.key

    def set_key(self, key: str) -> None:
        self.key = key

    def get_value(self) -> float:
        return self._value

    def set_value(self, value: float) -> None:
        self._value = value
