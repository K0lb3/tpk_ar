# Tpk

A Python port of [AssetRipper/Tpk](https://github.com/AssetRipper/Tpk), primarily for use in UnityPy.

This is maintained as a separate project to ensure forward compatibility for older UnityPy versions against potential breaking changes in the original code.

Rather than acting as an exact mirror of the upstream project, this port focuses solely on providing a Tpk format parser with a stable, backward-compatible API.

## Options

The `brotli` and `lz4` dependencies are optional. To handle compressed Tpk files, install the package with the required extras:

```bash
pip install "tpk[brotli]"
pip install "tpk[lz4]"
pip install "tpk[full]"  # Installs both
```

## Development

### TODO

- [x] Parser
- [ ] Dumper (for saving extracted type tree information of games)
- [ ] Native Extension (C++, for performance)

### Benchmarking

To measure the cost of loading a TPK file and inspect the same code path in snakeviz, install the dev extras:

```bash
uv sync --extra dev
```

Run the timing benchmark against the bundled uncompressed sample:

```bash
uv run python benchmarks/bench_load.py
```

Generate a profile for the same load path, then open it in snakeviz:

```bash
uv run python benchmarks/profile_load.py
uv run snakeviz profiles/uncompressed.prof
```
