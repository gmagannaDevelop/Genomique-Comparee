"""

"""

import unittest
import numpy as np
from pathlib import Path

# Our module to be tested
from gencomp.parsing import parse_strains_from_filename

DATA_DIR: str = "ready_blast_outputs"
RNG_SEED: int = 1234
DATA_FILE_EXTENSION: str = ".bl"


class TestParsing(unittest.TestCase):
    """ """

    def setUp(self):
        print("Setting up parsing test")
        self.base_path = Path(".")
        self.data_path = self.base_path.joinpath(DATA_DIR)
        if not self.data_path.exists():
            raise FileNotFoundError(
                f"DATA_PATH : {self.data_path.absolute().as_posix()}"
            )
        self.blast_files = list(self.data_path.glob("*.bl"))
        self._extension = DATA_FILE_EXTENSION

    def tearDown(self):
        pass

    def get_n_random_files(self, n: int):
        """Choose n random file amongst self.blast_files"""
        return list(np.random.choice(self.blast_files, n))

    def test_parse_strains_from_filename(self):
        """ """
        files = [
            Path(
                "ready_blast_outputs/Escherichia_coli_str_k_12_substr_mg1655-vs-Escherichia_coli_str_k_12_substr_w3110.bl"
            ),
            Path(
                "ready_blast_outputs/Escherichia_coli_str_k_12_substr_w3110-vs-Shigella_flexneri_2a_str_2457t.bl"
            ),
            Path(
                "ready_blast_outputs/Shigella_flexneri_2a_str_2457t-vs-Escherichia_fergusonii_atcc_35469.bl"
            ),
            Path(
                "ready_blast_outputs/Shigella_dysenteriae_sd197-vs-Shigella_flexneri_5_str_8401.bl"
            ),
        ]
        for file in files:
            self.assertEqual(len(parse_strains_from_filename(file)), 2)
