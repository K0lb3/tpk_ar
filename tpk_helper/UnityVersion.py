from enum import IntEnum
from typing import Optional

try:
    from UnityPy.helpers.UnityVersion import UnityVersion, UnityVersionType
except ImportError:

    class UnityVersionType(IntEnum):
        a = 0  # Alpha
        b = 1  # Beta
        c = 2  # China
        f = 3  # Final
        p = 4  # Patch
        x = 5  # Experimental
        u = 255  # Unknown

    class UnityVersion(int):
        # https://github.com/AssetRipper/VersionUtilities/blob/master/VersionUtilities/UnityVersion.cs
        _type_str: Optional[str]
        _postfix: Optional[str]

        @property
        def major(self):
            return (self >> 48) & 0xFFFF

        @property
        def minor(self):
            return (self >> 32) & 0xFFFF

        @property
        def build(self):
            return (self >> 16) & 0xFFFF

        @property
        def type(self):
            return UnityVersionType((self >> 8) & 0xFF)

        @property
        def type_str(self):
            return getattr(self, "_type_str", self.type.name)

        @property
        def postfix(self):
            return getattr(self, "_postfix", "")

        @property
        def type_number(self):
            return self & 0xFF

        def __str__(self) -> str:
            if self.major <= 5:
                return f"{self.major}.{self.minor}.{self.build}"
            else:
                return f"{self.major}.{self.minor}{self.type_str}{self.type_number}{self.postfix}"

        def __repr__(self) -> str:
            return f"UnityVersion {self.__str__()}"


__all__ = ["UnityVersion", "UnityVersionType"]
