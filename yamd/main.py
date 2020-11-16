from abc import ABCMeta, abstractmethod
from typing import List, Optional, Iterable, Union, Dict

import yaml

from dirs import ROOT_DIR
from table_maker import Table
from yamd.pretty_label import get_pretty_label, get_language_from_code


def get_plain_literal(datatype_value: str) -> str:
    return datatype_value.split('^^')[0]


def get_md_list(level: int, lst: Iterable[Union[str, Iterable[str]]]) -> str:
    """Returns a markdown list indented to the appropriate level.

    Args:
        level: The base level to indent to.
        lst: The list of (list of) str to convert to markdown.

    Examples:
        >>> get_md_list(5, [])
        ''
        >>> get_md_list(0, ['Thing'])
        '- Thing'
        >>> get_md_list(2, ['Pizza','Basil'])
        '    - Pizza\\n    - Basil'
        >>> get_md_list(0, ['Ant', ['Ant man', 'Ant woman']])
        '- Ant\\n  - Ant man\\n  - Ant woman'

    Notes:
        Base list item must be `str` in order to support
        multiple types of iterables. Either the list item
        type is defined or the iterable type is defined.
        I chose the former.
    """
    if isinstance(lst, str):
        return ''.join(('  ' * level, '- ', lst))
    if isinstance(lst, Iterable):
        return '\n'.join(get_md_list(level + 1, item) for item in lst)
    raise TypeError(f"item must be a str or an iterable of str, not {lst.__class__.__name__}")


def split_locstr(locstr: str) -> (str, str):
    try:
        value, type_ = locstr.split('^^')
        type_, language = type_.split('@')
        return value, language
    except ValueError:
        raise


def write_language_table(lst: List[str], header: str) -> str:
    """Returns a markdown table represenation of the value

    Args:
        lst: List of localised string (rdfs:Literal@someRegion)
        header: The other header besides language.

    Examples:
        >>> write_language_table(['Food^^rdfs:Literal@en'], 'label')
        '| Language | label |\\n|----------|-------|\\n| English  | Food  |\\n'
    """
    table = Table.create_table("Markdown")
    assert isinstance(header, str)
    table.add_header("Language", header)
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


def is_locstr(s: str) -> bool:
    """Returns True if `s` is a localized string."""
    return '^^rdfs:Literal@' in s


ALWAYS_USE_TABLE = ['rdfs:label']


class Annotations:
    def __init__(self, data: dict):
        self.data = data

    def as_markdown(self) -> Optional[str]:
        if self.data is None:
            return
        lines = [
            '### Annotations',
        ]
        for prop, values in self.data.items():
            clean_values = parse_lenient_list_of_strings(values)
            lines.append(get_pretty_label(prop))
            if any(is_locstr(item) for item in clean_values) or prop in ALWAYS_USE_TABLE:
                lines.append('')
                table = write_language_table(clean_values, get_pretty_label(prop))
                lines.append(table)
            else:
                lines.append(get_md_list(0, map(get_plain_literal, clean_values)))
                lines.append('')
        return '\n'.join(lines)


class Entity(metaclass=ABCMeta):
    def __init__(self, name: str, data: dict):
        if isinstance(data, str):
            # Allow using '' as placeholder when no data
            assert data == ''
            self.data = {}
        else:
            self.data = data
        self._name = name

    @property
    @abstractmethod
    def _description_map(self) -> Dict[str, str]:
        raise NotImplementedError

    @abstractmethod
    def as_markdown(self) -> str:
        raise NotImplementedError

    @property
    def name(self) -> str:
        return self._name.split(':')[-1]

    @property
    def annotations(self) -> Optional[str]:
        try:
            return Annotations(self.data['annotations']).as_markdown()
        except KeyError:
            return None


class Class(Entity):
    @property
    def _description_map(self) -> Dict[str, str]:
        return {
            'rdfs:subClassOf': 'Subclass of',
            'owl:disjointWith': 'Disjoint with',
            'owl:equivalentClass': 'Equivalent tp',
        }

    def as_markdown(self) -> str:
        lines = [
            f'## {self.name}',
            self.annotations,
            self.description,
            self.object_properties,
            self.data_properties,
        ]
        return '\n'.join((line for line in lines if line))

    @property
    def description(self) -> Optional[str]:
        lines = []
        for uname, pname in self._description_map.items():
            if uname in self.data:
                if uname == 'owl:equivalentClass':
                    data = self.data[uname]['owl:Restriction']
                else:
                    data = self.data[uname]
                cleaned_data = parse_lenient_list_of_strings(data)
                if cleaned_data:
                    lines += [f'{pname}:',
                              get_md_list(0, cleaned_data),
                              '']
        if lines:
            lines.insert(0, '### Description')
            return '\n'.join(lines)

    @property
    def object_properties(self) -> Optional[str]:
        if 'objectProperty' in self.data:
            cleaned_data = parse_lenient_list_of_list_of_string(self.data['objectProperty'])
            if cleaned_data:
                lines = ['### Object Properties',
                         get_md_list(0, cleaned_data),
                         '']
                return '\n'.join(lines)
        return

    @property
    def data_properties(self) -> Optional[str]:
        if 'dataProperty' in self.data:
            cleaned_data = parse_lenient_list_of_list_of_string(self.data['dataProperty'])
            if cleaned_data:
                lines = ['### Data Properties',
                         get_md_list(0, cleaned_data),
                         '']
                return '\n'.join(lines)
        return


def parse_lenient_list_of_strings(obj) -> List[str]:
    if isinstance(obj, str):
        if obj:
            # assume using not using list for one string
            return [obj]
        # empty string, assume using '' as placeholder
        assert obj == ''
        return []
    if isinstance(obj, list):
        if all(isinstance(item, str) for item in obj):
            return obj
    raise ValueError(f"Object is not a list of strings: '{obj}'")


def is_recursive_list_of_strings(obj) -> bool:
    if isinstance(obj, str):
        return True
    if isinstance(obj, list):
        return all(is_recursive_list_of_strings(item) for item in obj)
    return False


def parse_lenient_list_of_list_of_string(obj) -> List[str]:
    if isinstance(obj, str):
        if obj:
            # assume using not using list for one string
            return [obj]
        # empty string, assume using '' as placeholder
        assert obj == ''
        return []
    if isinstance(obj, list):
        if is_recursive_list_of_strings(obj):
            return obj
    raise ValueError(f"Object is not a list of (list of) strings: '{obj}'")


def parse_lenient_list_of_objects(obj) -> List[dict]:
    if isinstance(obj, str):
        if obj == '':
            # empty string, assume using '' as placeholder
            return []
    if isinstance(obj, dict):
        # assume using not using list for one object
        return [obj]
    if isinstance(obj, list):
        if all(isinstance(item, dict) for item in obj):
            return obj
    raise ValueError(f"Object is not a list of dicts: '{obj}'")


class Property(Entity):
    @property
    def _description_map(self) -> Dict[str, str]:
        return {
            'rdfs:domain': 'Domain',
            'rdfs:range': 'Range',
            'rdfs:subPropertyOf': 'Sub-properties',
        }

    def as_markdown(self) -> str:
        lines = [
            f'## {self.name}',
            self.annotations,
            self.description,
        ]
        return '\n'.join((line for line in lines if line))

    @property
    def description(self) -> Optional[str]:
        lines = []
        for uname, pname in self._description_map.items():
            if uname in self.data:
                lines += [
                    f'{pname}:',
                    get_md_list(0, self.data[uname]),
                    ''
                ]
        if lines:
            lines.insert(0, '### Description')
            return '\n'.join(lines)


class ObjectProperty(Property):
    pass


class DataProperty(Property):
    pass


class AnnotationProperty(Property):
    @property
    def _description_map(self) -> Dict[str, str]:
        return {
            'rdfs:domain': 'Domain',
            'rdfs:range': 'Range',
            # 'rdf:superProperty': 'Superproperties',
        }


def main():
    with open(ROOT_DIR / 'tests/test_cases/test_case2.yaml', 'r', encoding='utf-8') as yamlfile:
        data = yaml.load(yamlfile, yaml.FullLoader)
    # print(data)

    lines: List[str] = [
        '# Ontology Description',
    ]
    try:
        lines += [Annotations(data['annotations']).as_markdown()]
    except KeyError:
        pass
    lines.append('')
    lines += write_classes(data['owl:Class'])

    try:
        for p, d in data['owl:ObjectProperty'].items():
            lines += [ObjectProperty(p, d).as_markdown()]
        lines.append('')
    except KeyError:
        pass

    try:
        for p, d in data['owl:DataProperty'].items():
            lines += [DataProperty(p, d).as_markdown()]
        lines.append('')
    except KeyError:
        pass

    try:
        for p, d in data['owl:AnnotationProperty'].items():
            lines += [AnnotationProperty(p, d).as_markdown()]
    except KeyError:
        pass

    with open(ROOT_DIR / 'yamd/test.md', 'w', encoding='utf-8') as mdfile:
        mdfile.write('\n'.join(lines))


if __name__ == '__main__':
    # import doctest
    #
    # doctest.testmod()
    main()
