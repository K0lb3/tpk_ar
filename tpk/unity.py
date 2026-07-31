from dataclasses import dataclass
from struct import Struct
from typing import Any, BinaryIO, ClassVar, Dict, List, Optional, Tuple

from tpk_helper.unityversion import UnityVersion

from .enums import TpkUnityClassFlags
from .utils import INT32, UINT16, get_item_for_version, read_version


@dataclass
class TpkUnityClass:
    __slots__ = ("Name", "Base", "Flags", "EditorRootNode", "ReleaseRootNode")
    ParserStruct: ClassVar[Struct] = Struct("<HHb")
    Name: int
    Base: int
    Flags: TpkUnityClassFlags
    EditorRootNode: Optional[int]
    ReleaseRootNode: Optional[int]

    @classmethod
    def parse(cls, stream: BinaryIO) -> "TpkUnityClass":
        Name, Base, Flags = TpkUnityClass.ParserStruct.unpack(stream.read(TpkUnityClass.ParserStruct.size))
        flags = TpkUnityClassFlags(Flags)
        editorRootNode = releaseRootNode = None
        if flags & TpkUnityClassFlags.HasEditorRootNode:
            (editorRootNode,) = UINT16.unpack(stream.read(UINT16.size))
        if flags & TpkUnityClassFlags.HasReleaseRootNode:
            (releaseRootNode,) = UINT16.unpack(stream.read(UINT16.size))

        return cls(Name=Name, Base=Base, Flags=flags, EditorRootNode=editorRootNode, ReleaseRootNode=releaseRootNode)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "Name": self.Name,
            "Base": self.Base,
            "Flags": self.Flags,
            "EditorRootNode": self.EditorRootNode,
            "ReleaseRootNode": self.ReleaseRootNode,
        }

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TpkUnityClass):
            return False
        return self.to_dict() == other.to_dict()

    def __hash__(self) -> int:
        return hash(
            (
                self.Name,
                self.Base,
                self.Flags,
                self.EditorRootNode,
                self.ReleaseRootNode,
            )
        )


class TpkClassInformation(List[Tuple[UnityVersion, Optional[TpkUnityClass]]]):
    ID: int

    def __init__(self, entries: List[Tuple[UnityVersion, Optional[TpkUnityClass]]], ID: int):
        super().__init__(entries)
        self.ID = ID

    @classmethod
    def parse(cls, stream: BinaryIO) -> "TpkClassInformation":
        (ID,) = INT32.unpack(stream.read(INT32.size))
        (count,) = INT32.unpack(stream.read(INT32.size))
        entries = [
            (read_version(stream), TpkUnityClass.parse(stream) if stream.read(1)[0] else None) for _ in range(count)
        ]
        instance = cls(entries, ID)
        return instance

    def getVersionedClass(self, version: UnityVersion) -> Optional[TpkUnityClass]:
        return get_item_for_version(version, self)


@dataclass
class TpkUnityNode:
    __slots__ = (
        "TypeName",
        "Name",
        "ByteSize",
        "Version",
        "TypeFlags",
        "MetaFlag",
        "SubNodes",
    )
    ParserStruct: ClassVar[Struct] = Struct("<HHihbIH")
    TypeName: int
    Name: int
    ByteSize: int
    Version: int
    TypeFlags: int
    MetaFlag: int
    SubNodes: List[int]

    @classmethod
    def parse(cls, stream: BinaryIO) -> "TpkUnityNode":
        (
            TypeName,
            Name,
            ByteSize,
            Version,
            TypeFlags,
            MetaFlag,
            count,
        ) = cls.ParserStruct.unpack(stream.read(cls.ParserStruct.size))

        SubNodeStruct = Struct(f"<{count}H")
        SubNodes = list(SubNodeStruct.unpack(stream.read(SubNodeStruct.size)))

        return cls(
            TypeName=TypeName,
            Name=Name,
            ByteSize=ByteSize,
            Version=Version,
            TypeFlags=TypeFlags,
            MetaFlag=MetaFlag,
            SubNodes=SubNodes,
        )

    def __hash__(self) -> int:
        # TODO
        return hash(self.__dict__)


class TpkUnityNodeBuffer(List[TpkUnityNode]):
    @classmethod
    def parse(cls, stream: BinaryIO) -> "TpkUnityNodeBuffer":
        (count,) = INT32.unpack(stream.read(INT32.size))
        return cls(TpkUnityNode.parse(stream) for _ in range(count))


__all__ = ["TpkUnityClass", "TpkClassInformation", "TpkUnityNode", "TpkUnityNodeBuffer"]
