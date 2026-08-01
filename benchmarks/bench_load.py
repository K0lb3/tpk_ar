import sys
from io import BytesIO
from pathlib import Path

import pyperf

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tpk_ar.file import TpkFile


DEFAULT_SAMPLE = ROOT / "tests" / "samples" / "type_tree" / "v2" / "uncompressed.tpk"


def load_tpk(payload: bytes) -> None:
    TpkFile.parse(BytesIO(payload)).GetDataBlob()


def main() -> None:
    runner = pyperf.Runner()
    payload = DEFAULT_SAMPLE.read_bytes()
    runner.bench_func("load_tpk_uncompressed", lambda payload=payload: load_tpk(payload))


if __name__ == "__main__":
    main()
