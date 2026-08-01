import argparse
import cProfile
import sys
from io import BytesIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tpk_ar.file import TpkFile


DEFAULT_SAMPLE = ROOT / "tests" / "samples" / "type_tree" / "v2" / "uncompressed.tpk"


def load_tpk(payload: bytes) -> None:
    TpkFile.parse(BytesIO(payload)).GetDataBlob()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Profile loading a TPK file for snakeviz")
    parser.add_argument("--sample", type=Path, default=DEFAULT_SAMPLE, help="Path to the TPK sample")
    parser.add_argument("--output", type=Path, help="Path to the cProfile output file")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    payload = args.sample.read_bytes()

    output = args.output
    if output is None:
        output = Path("profiles") / f"{args.sample.stem}.prof"
    output.parent.mkdir(parents=True, exist_ok=True)

    profiler = cProfile.Profile()
    profiler.enable()
    load_tpk(payload)
    profiler.disable()
    profiler.dump_stats(str(output))
    print(f"Wrote profile to {output}")


if __name__ == "__main__":
    main()
