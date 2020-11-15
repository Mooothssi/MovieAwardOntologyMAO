from typing import List, Optional

import yaml

from dirs import ROOT_DIR
from table_maker import Table

from yamd.pretty_label import get_pretty_label, get_language_from_code


def get_plain_literal(s: str) -> str:
    return s.split('^^')[0]


def get_markdown_list_item(level: int, s: str) -> str:
    """Returns a markdown list indented to the appropriate level.

    Args:
        level: The level to indent to
        s: The string which is the body of the list

    Examples:
        >>> get_markdown_list(0, 'Thing')
        '- Thing'
        >>> get_markdown_list(2, 'Pizza')
        '    - Pizza'
    """
    return ''.join([' ' * 2 * level, '- ', s])


def split_locstr(locstr: str) -> (str, str):
    try:
        value, type_ = locstr.split('^^')
        type_, language = type_.split('@')
        return value, language
    except ValueError:
        raise


def write_language_table(lst: List[str], property: str) -> str:
    """Returns a markdown table represenation of the value

    Args:
        lst: List of localised string (rdfs:Literal@someLanguage)

    Examples:
        >>> write_language_table(['Food^^rdfs:Literal@en'], 'label')
        '| Language | label |\\n|----------|-------|\\n| English  | Food  |\\n'
    """
    table = Table.create_table("Markdown")
    assert isinstance(property, str)
    table.add_header("Language", property)
    for item in lst:
        try:
            value, language = split_locstr(item)
        except ValueError:
            if item.endswith('^^xsd:string'):
                table.add_row('None', item.split('^^')[0])
            else:
                raise
        else:
            table.add_row(get_language_from_code(language), value)
    table.end_table()
    return str(table)


def write_classes(classes: dict) -> List[str]:
    lines = [
        '# Class',
    ]
    for class_, data in classes.items():
        lines.append(Class(class_, data).as_markdown())
    return lines


class Annotations:
    def __init__(self, data: dict):
        self.data = data

    def as_markdown(self) -> Optional[str]:
        if self.data is None:
            return
        lines = [
            '### Annotations',
        ]
        for property, value in self.data.items():
            if not isinstance(value, list):
                value = [value]
            locstrs = []
            for item in value:
                if '^^rdfs:Literal@' in item:
                    locstrs.append(item)
            if locstrs or property in ['rdfs:label']:
                lines.append(get_pretty_label(property))
                lines.append('')
                table = write_language_table(value, get_pretty_label(property))
                lines.append(table)
            else:
                lines.append(get_pretty_label(property))
                for item in value:
                    lines.append(get_markdown_list_item(1, get_plain_literal(item)))
                lines.append('')
        return '\n'.join(lines)


class Class:
    map = {
        'rdfs:subClassOf': 'Subclass Of',
        'owl:disjointWith': 'Disjoint with',
        'owl:equivalentClass': 'Equivalent class',
    }

    def __init__(self, name: str, data: dict):
        if isinstance(data, str):
            self.data = {}
        else:
            self.data = data
        self._name = name

    def as_markdown(self) -> str:
        lines = [
            f'## {self.name}',
            self.annotations,
            self.description,
            self.object_properties,
        ]
        return '\n'.join((line for line in lines if line))

    @property
    def name(self) -> str:
        return self._name.split(':')[1]

    @property
    def annotations(self) -> Optional[str]:
        try:
            return Annotations(self.data['annotations']).as_markdown()
        except KeyError:
            return None

    @property
    def description(self) -> Optional[str]:
        try:
            lines = []
            for uname, pname in self.map.items():
                if uname in self.data:
                    lines.append(f'{pname}:')
                    for item in self.data[uname]:
                        lines.append(get_markdown_list_item(1, item))
                    lines.append('')
            if lines:
                lines.insert(0, '### Description')
                return '\n'.join(lines)
        except KeyError:
            return None

    @property
    def object_properties(self) -> Optional[str]:
        try:
            lines = []
            for property in self.data['objectProperty']:
                lines.append(get_markdown_list_item(1, property))
            lines.append('')
            if lines:
                lines.insert(0, '### Object Properties')
                return '\n'.join(lines)
        except KeyError:
            return None

    # @property
    # def data_properties(self) -> str:
    #     try:
    #         lines = [
    #             '### Data Properties',
    #         ]
    #         for property in self.data['dataProperty']:
    #             lines.append(get_markdown_list_item(0, property))
    #         return '\n'.join(lines)
    #     except KeyError:
    #         return ''


def main():
    with open(ROOT_DIR / 'tests/test_cases/test_case1.yaml', 'r', encoding='utf-8') as yamlfile:
        data = yaml.load(yamlfile, yaml.FullLoader)
    print(data)

    lines: List[str] = [
        '# Ontology Description',
    ]
    lines += [Annotations(data['annotations']).as_markdown()]
    lines.append('')
    lines += write_classes(data['owl:Class'])

    with open(ROOT_DIR / 'yamd/test.md', 'w', encoding='utf-8') as mdfile:
        mdfile.write('\n'.join(lines))


if __name__ == '__main__':
    # import doctest
    #
    # doctest.testmod()
    main()
