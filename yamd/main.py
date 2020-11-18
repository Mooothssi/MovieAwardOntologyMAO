from pathlib import Path
from typing import List, Optional, Dict, Union, Tuple, Type

import yaml

from dirs import ROOT_DIR
from table_maker import Table
from yamd.markdown import get_md_list
from yamd.parser import parse_lenient_list_of_strings, parse_lenient_list_of_list_of_string
from yamd.owl import get_pretty_label, get_language_from_code, split_locstr, get_plain_literal, is_locstr


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
        return '\n'.join(lines)


class Entity:
    def __init__(self, name: str, data: dict):
        if isinstance(data, str):
            # Allow using '' as placeholder when no data
            assert data == ''
            self.data = {}
        else:
            self.data = data
        self._name = name

    @property
    def _description_map(self) -> Dict[str, str]:
        raise NotImplementedError

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


def write_classes(classes: dict) -> List[str]:
    lines = [
        '# Class',
    ]
    for class_, data in classes.items():
        lines.append(Class(class_, data).as_markdown())
    return lines


def convert_v1(data: dict) -> List[str]:
    """Returns the lines of md documentation to write from specs data."""
    lines = []
    if 'annotations' in data:
        lines += [f'# Ontology Description',
                  Annotations(data['annotations']).as_markdown(),
                  '']

    sections: List[Tuple[str, str, Type[Entity]]] = [
        ('Classes', 'owl:Class', Class),
        ('Object Properties', 'owl:ObjectProperty', ObjectProperty),
        ('Data Properties', 'owl:DataProperty', DataProperty),
        ('Annotation Properties', 'owl:AnnotationProperty', AnnotationProperty),
        # ('Rules', 'owl:Rule?', Rule?),
    ]
    for section, dict_section, cls in sections:
        if dict_section not in data:
            continue
        lines += [f'# {section}']
        lines += [cls(p, d).as_markdown() for p, d in data[dict_section].items()]
        lines += ['']
    return lines


def convert_owl_yaml_to_md(owlyaml_file: Union[str, Path],
                           md_file: Union[str, Path]) -> None:
    """Converts a owl yaml specs file to md documentation."""
    with open(owlyaml_file, 'r', encoding='utf-8') as yamlfile:
        data = yaml.load(yamlfile, yaml.FullLoader)

    if 'specs' not in data:
        # first version
        lines = convert_v1(data)
    else:
        raise NotImplementedError

    with open(md_file, 'w', encoding='utf-8') as mdfile:
        mdfile.write('\n'.join(lines))


if __name__ == '__main__':
    import doctest

    doctest.testmod()
    convert_owl_yaml_to_md(ROOT_DIR / 'tests/test_cases/test_case1.yaml', ROOT_DIR / 'yamd/test.md')
