from tpk_helper.utils import download_tpk

download_tpk(
    type="type_tree",
    compression="brotli",
    version="master",
    verify=True,
)


def main():
    download_tpk()
