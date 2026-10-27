class SymbolTable:
    def __init__(self):
        self._identifiers: dict[str, None] = {}

    def add(self, identifier: str) -> bool:
        if identifier in self._identifiers:
            return False
        self._identifiers[identifier] = None
        return True

    @property
    def identifiers(self) -> tuple[str, ...]:
        return tuple(self._identifiers)

    def __contains__(self, identifier: str) -> bool:
        return identifier in self._identifiers

    def __len__(self) -> int:
        return len(self._identifiers)
