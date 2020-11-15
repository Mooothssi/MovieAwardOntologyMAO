from ontogen.owlready_converter import YamlToOwlConverter

import os


if __name__ == "__main__":
    YamlToOwlConverter("./mao_bck.yaml").to_python_scripts(os.path.dirname(__file__))
