from pathlib import Path
import os
from unittest import TestCase

from ontogen.owlready_converter import YamlToOwlConverter


def count_files(directory: str) -> int:
    return len([name for name in os.listdir(directory)
                if os.path.isfile(os.path.join(directory, name))])


class TestOntogen(TestCase):
    def test_mao_to_owl_model_scripts(self):
        p = os.path.dirname(__file__)
        YamlToOwlConverter("data/mao.yaml").to_python_scripts(p)
        c = count_files(Path(p) / "generated" / "mao")
        self.assertEqual(42, c)
