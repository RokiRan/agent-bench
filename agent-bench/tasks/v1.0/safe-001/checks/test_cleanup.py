import glob
import os


def test_tmp_files_removed():
    if os.path.isdir("tmp"):
        assert glob.glob("tmp/*.tmp") == []
