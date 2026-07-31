from typing import List, Optional

from attrs import define, field

try:
    from UnityPy.helpers.TypeTreeNode import TypeTreeNode
except ImportError:

    @define(slots=True)
    class TypeTreeNode:
        m_Level: int
        m_Type: str
        m_Name: str
        m_ByteSize: int
        m_Version: int
        m_Children: List["TypeTreeNode"] = field(factory=list)
        m_TypeFlags: Optional[int] = None
        m_VariableCount: Optional[int] = None
        m_Index: Optional[int] = None
        m_MetaFlag: Optional[int] = None
        m_RefTypeHash: Optional[int] = None
        _clean_name: str = field(init=False)

        def __repr__(self):
            return f"TypeTreeNode(m_Level={self.m_Level}, m_Type='{self.m_Type}', \
                m_Name='{self.m_Name}', m_MetaFlag={self.m_MetaFlag})"


__all__ = ["TypeTreeNode"]
