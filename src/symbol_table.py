"""จัดเก็บ Identifier และตรวจชื่อซ้ำโดยแยกตัวพิมพ์เล็ก/ใหญ่."""


class SymbolTable:
    # dict ตรวจสมาชิกเฉลี่ย O(1) และเก็บลำดับที่พบครั้งแรก
    def __init__(self):
        self._identifiers: dict[str, None] = {}

    def add(self, identifier: str) -> bool:
        """คืน True เมื่อเพิ่มชื่อใหม่ หรือ False เมื่อชื่อนั้นมีอยู่แล้ว."""
        if identifier in self._identifiers:
            return False
        self._identifiers[identifier] = None
        return True

    # เปิดให้ตรวจข้อมูลโดยไม่ต้องแก้ dict ภายในโดยตรง
    @property
    def identifiers(self) -> tuple[str, ...]:
        return tuple(self._identifiers)

    def __contains__(self, identifier: str) -> bool:
        return identifier in self._identifiers

    def __len__(self) -> int:
        return len(self._identifiers)
