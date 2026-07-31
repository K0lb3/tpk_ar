import lzma
import struct
from typing import Union

import brotli
import lz4.block

ByteString = Union[bytes, bytearray, memoryview]
GZIP_MAGIC: bytes = b"\x1f\x8b"
BROTLI_MAGIC: bytes = b"brotli"


# LZMA
def decompress_lzma(data: ByteString, read_decompressed_size: bool = False) -> bytes:
    props, dict_size = struct.unpack("<BI", data[:5])
    lc = props % 9
    remainder = props // 9
    pb = remainder // 5
    lp = remainder % 5
    dec = lzma.LZMADecompressor(
        format=lzma.FORMAT_RAW,
        filters=[
            {
                "id": lzma.FILTER_LZMA1,
                "dict_size": dict_size,
                "lc": lc,
                "lp": lp,
                "pb": pb,
            }
        ],
    )
    data_offset = 13 if read_decompressed_size else 5
    return dec.decompress(data[data_offset:])


# LZ4
def decompress_lz4(data: ByteString, uncompressed_size: int) -> bytes:  # LZ4M/LZ4HC
    return lz4.block.decompress(data, uncompressed_size)


# Brotli
def decompress_brotli(data: ByteString) -> bytes:
    return brotli.decompress(data)


__all__ = (
    "decompress_brotli",
    "decompress_lz4",
    "decompress_lzma",
)
