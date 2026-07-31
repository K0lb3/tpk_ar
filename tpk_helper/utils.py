from io import BytesIO
from typing import Literal
from urllib.request import urlopen
from zipfile import ZipFile

from .tpk import TpkFile

TPK_URL = "https://nightly.link/AssetRipper/Tpk/workflows/{type}_tpk/{version}/{compression}_file.zip"


def download_tpk(
    type: Literal["type_tree", "engine_asset"] = "type_tree",
    compression: Literal["brotli", "lz4", "lzma", "uncompressed"] = "brotli",
    version: str = "master",
    verify: bool = True,
) -> bytes:
    url = TPK_URL.format(type=type, version=version, compression=compression)
    res = urlopen(url)
    if res.status != 200:
        raise Exception(f"Failed to download TPK file: {res.status} {res.reason}")
    zip_data = res.read()

    with ZipFile(BytesIO(zip_data)) as zip_file:
        tpk_data = zip_file.read(f"{compression}.tpk")

    if verify:
        with BytesIO(tpk_data) as f:
            TpkFile(f).GetDataBlob()
    return tpk_data
