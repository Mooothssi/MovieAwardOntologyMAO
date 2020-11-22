from pathlib import Path
from typing import List, Optional, Dict, Union, Tuple, Type, IO, Hashable, Set

import yaml

from dirs import ROOT_DIR
from table_maker import Table
from utils.temp_io_utils import open_and_write_file
from yamd.markdown import get_md_list
from yamd.owl import get_pretty_label, get_language_from_code, split_locstr, get_plain_literal, is_locstr
from yamd.parser import parse_lenient_list_of_strings, parse_lenient_list_of_list_of_string, trim_dict

LOLOS = Union[str, List['LOLOS']]


class Node:
    _instances = {}

    def __new__(cls, *args, **kwargs):
        key = args[0]
        if key not in cls._instances:
            cls._instances[key] = super().__new__(cls)
        return cls._instances[key]

    def __init__(self, key: Hashable):
        if not hasattr(self, 'key'):
            # So that attributes don't get rewritten
            self.key = key
            self._parents: Set['Node'] = set()
            self._children: Set['Node'] = set()

    @classmethod
    def get_instance(cls, key: Hashable) -> 'Node':
        try:
            return cls._instances[key]
        except KeyError:
            raise KeyError(f"Key '{key}' is not a node.")

    def _add_parent(self, parent) -> None:
        if not isinstance(parent, Node):
            raise TypeError(f"parent must be a Node, not a '{parent.__class__.__name__}'")
        if parent is self:
            raise ValueError(f"parent must be a separate entity")
        self._parents.add(parent)
        parent._children.add(self)

    def add_parents(self, *parents: 'Node') -> None:
        if len(parents) == 0:
            raise ValueError("No nodes are given!")
        for parent in parents:
            self._add_parent(parent)

    def add_parent_from_keys(self, *keys: Hashable) -> None:
        if len(keys) == 0:
            raise ValueError("No keys are given!")
        for key in keys:
            self._add_parent(self.get_instance(key))

    def __str__(self):
        return f"{self.key}"

    def _get_key(self) -> Hashable:
        return self.key

    def show_graph(self, level: int = 0) -> str:
        lines = [f"{'  ' * level}- {self.key}"]
        lines += [child.show_graph(level + 1) for child in sorted(self._children, key=Node._get_key)]
        return '\n'.join(lines)

    @property
    def parents(self) -> Set['Node']:
        return self._parents.copy()

    @property
    def children(self) -> Set['Node']:
        return self._children.copy()

    @classmethod
    def from_list_of_parents(cls, child: str, parents: Union[str, List[str]]) -> None:
        if isinstance(parents, str):
            Node(child)._add_parent(Node(parents))
            return
        if isinstance(parents, list):
            for parent in parents:
                cls.from_list_of_parents(child, parent)
            return
        raise AssertionError(f"STH WRONG child={child} parents={parents}")


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
    def __init__(self, name: str, data: dict, *, auto_include_thing: bool = True):
        if isinstance(data, str):
            # Allow using '' as placeholder when no data
            assert data == ''
            self.data = {}
        else:
            self.data = data
        self._name = name
        self.maybe_include_thing(auto_include_thing)

    def maybe_include_thing(self, auto_include_thing: bool) -> None:
        if auto_include_thing:
            try:
                Node(self.name).add_parents(Node(self._top_type))
            except ValueError as e:
                if e.args[0] == 'parent must be a separate entity':
                    # Might have 'Thing' etc. defined
                    pass
                else:
                    print(e.args)
                    raise

    @property
    def _description_map(self) -> Dict[str, str]:
        raise NotImplementedError

    @property
    def _top_type(self) -> str:
        raise NotImplementedError

    def as_markdown(self) -> str:
        raise NotImplementedError

    @property
    def name(self) -> str:
        prefix, *rest = self._name.split(':')
        return ':'.join(rest)

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
            'owl:equivalentClass': 'Equivalent to',
        }

    @property
    def _top_type(self) -> str:
        return 'Thing'

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
    def description(self, version=2) -> Optional[str]:
        if version == 1:
            return self._description_v1()
        elif version >= 2:
            return self._description_v2()

    def _description_v1(self) -> Optional[str]:
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
                    if uname == 'rdfs:subClassOf':
                        Node.from_list_of_parents(self.name, cleaned_data)
        if lines:
            lines.insert(0, '### Description')
            return '\n'.join(lines)

    def _description_v2(self) -> Optional[str]:
        lines = []
        for uname, pname in self._description_map.items():
            if uname in self.data:
                data = self.data[uname]
                cleaned_data = parse_lenient_list_of_strings(data)
                if cleaned_data:
                    lines += [f'{pname}:',
                              get_md_list(0, cleaned_data),
                              '']
                    if uname == 'rdfs:subClassOf':
                        Node.from_list_of_parents(self.name, cleaned_data)
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


class IRIPrefix(Entity):
    def __init__(self, data_iri: dict, data_prefix: dict):
        self.data_iri = data_iri
        self.data_prefix = data_prefix

    def as_markdown(self) -> str:
        lines = [
            '# IRI',
            self.data_iri,
            '',
            '# Prefixes',
        ]
        print(self.data_prefix.items())
        for prop, value in self.data_prefix.items():
            heading_prop = f'## {prop}'
            lines.append('\n'.join([heading_prop, value, '']))
        return '\n'.join(lines)


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
                cleaned_data = parse_lenient_list_of_strings(self.data[uname])
                lines += [
                    f'{pname}:',
                    get_md_list(0, cleaned_data),
                    ''
                ]
                if uname == 'rdfs:subPropertyOf':
                    Node.from_list_of_parents(self.name, cleaned_data)
        if lines:
            lines.insert(0, '### Description')
            return '\n'.join(lines)


class ObjectProperty(Property):
    @property
    def _top_type(self) -> str:
        return 'TopObjectProperty'


class DataProperty(Property):
    @property
    def _top_type(self) -> str:
        return 'TopDataProperty'


class AnnotationProperty(Property):
    @property
    def _description_map(self) -> Dict[str, str]:
        return {
            'rdfs:domain': 'Domain',
            'rdfs:range': 'Range',
            # 'rdf:superProperty': 'Superproperties',
        }

    @property
    def _top_type(self) -> str:
        return 'DummyTopAnnotationProperty'

    def maybe_include_thing(self, auto_include_thing: bool) -> None:
        """Definitely include the dummy TopAnnotationProperty"""
        try:
            Node(self.name).add_parents(Node(self._top_type))
        except ValueError as e:
            if e.args[0] == 'parent must be a separate entity':
                # Might have 'Thing' etc. defined
                pass
            else:
                print(e.args)
                raise


def write_classes(classes: dict) -> List[str]:
    lines = [
        '# Class',
    ]
    for class_, data in classes.items():
        lines.append(Class(class_, data).as_markdown())
    return lines


def convert_v1(data: dict, *, auto_include_thing: bool = True) -> List[str]:
    """Returns the lines of md documentation to write from specs data."""
    text_sections = []
    if 'annotations' in data:
        lines = [f'# Ontology Description',
                 Annotations(data['annotations']).as_markdown(),
                 '']
        text_sections.append('\n'.join(lines))

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
        lines = [f'# {section}']
        lines += [cls(p, d, auto_include_thing=auto_include_thing).as_markdown() for p, d in data[dict_section].items()]
        lines += ['']
        text_sections.append('\n'.join(lines))
    liens = []
    t = Node('Thing').show_graph()
    if t:
        lines = ['# Class Hierarchy',
                 t,
                 '']
    if Node('TopObjectProperty').children or Node('TopDataProperty').children or Node('DummyTopAnnotationProperty').children:
        lines += ['# Property Hierarchy']
    if Node('TopObjectProperty').children:
        lines += ['### Object Property',
                  Node('TopObjectProperty').show_graph(),
                  '']
    if Node('TopDataProperty').children:
        lines += ['### Data Property',
                  Node('TopDataProperty').show_graph(),
                  '']
    if Node('DummyTopAnnotationProperty').children:
        lines += ['### Annotation Property']
        lines += [annotation.show_graph() for annotation in Node('DummyTopAnnotationProperty').children]
        lines += ['']
    text_sections.insert(1, '\n'.join(lines))
    return text_sections


def convert_v2(data: dict, *, auto_include_thing: bool = True) -> List[str]:
    """Returns the lines of md documentation to write from specs data."""
    text_sections = [
        f"version {data['version']}\n",
    ]
    if 'prefixes' in data:
        lines = [IRIPrefix(data['iri'], data['prefixes']).as_markdown(),
                 '']
        text_sections.append('\n'.join(lines))

    if 'annotations' in data:
        lines = [f'# Ontology Description',
                 Annotations(data['annotations']).as_markdown(),
                 '']
        text_sections.append('\n'.join(lines))

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
        lines = [f'# {section}']
        lines += [cls(p, d, auto_include_thing=auto_include_thing).as_markdown() for p, d in data[dict_section].items()]
        lines += ['']
        text_sections.append('\n'.join(lines))
    liens = []
    t = Node('Thing').show_graph()
    if t:
        lines = ['# Class Hierarchy',
                 t,
                 '']
    if Node('TopObjectProperty').children or Node('TopDataProperty').children or Node('DummyTopAnnotationProperty').children:
        lines += ['# Property Hierarchy']
    if Node('TopObjectProperty').children:
        lines += ['### Object Property',
                  Node('TopObjectProperty').show_graph(),
                  '']
    if Node('TopDataProperty').children:
        lines += ['### Data Property',
                  Node('TopDataProperty').show_graph(),
                  '']
    if Node('DummyTopAnnotationProperty').children:
        lines += ['### Annotation Property']
        lines += [annotation.show_graph() for annotation in Node('DummyTopAnnotationProperty').children]
        lines += ['']
    text_sections.insert(2, '\n'.join(lines))
    return text_sections


def convert_owl_yaml_to_md(owlyaml_file: Union[str, Path],
                           md_file: Union[IO, str, Path]) -> None:
    """Converts a owl yaml specs file to md documentation."""
    with open(owlyaml_file, 'r', encoding='utf-8') as yamlfile:
        data = yaml.load(yamlfile, yaml.FullLoader)
        data = trim_dict(data)
    #     print(str(data))
    # print(data['version'])

    if 'version' not in data:
        # first version
        lines = convert_v1(data)
    elif data['version'] == 'v1.0.0':
        lines = convert_v1(data, auto_include_thing=False)
    elif data['version'] == 'v2.1.0':
        lines = convert_v2(data, auto_include_thing=True)
    else:
        raise NotImplementedError

    open_and_write_file(md_file, '\n'.join(lines))


if __name__ == '__main__':
    import doctest

    doctest.testmod()
    convert_owl_yaml_to_md(ROOT_DIR / 'tests/specs/v2.1.0/test_case1.yaml', ROOT_DIR / 'yamd/test.md')
