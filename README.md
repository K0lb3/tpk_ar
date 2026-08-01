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
