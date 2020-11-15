from typing import List

import yaml

from dirs import ROOT_DIR

from yamd.pretty_label import get_pretty_label


def main():
    with open(ROOT_DIR / 'tests/test_cases/test_case1.yaml', 'r', encoding='utf-8') as yamlfile:
        data = yaml.load(yamlfile, yaml.FullLoader)
    print(data)

    lines: List[str] = []

    with open(ROOT_DIR / 'yamd/test.md', 'w', encoding='utf-8') as mdfile:
        mdfile.write('\n'.join(lines))


if __name__ == '__main__':
    main()
