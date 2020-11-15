from typing import List

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


def write_annotations(annotations: dict) -> List[str]:
    """Returns a list of lines to write for the "Ontology Description" part

    Args:
        data: YAML specs for the ontology
    """
    lines = [
        '### Annotations',
    ]
    for property, value in annotations.items():
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
                lines.append(get_markdown_list_item(0, get_plain_literal(item)))
    return lines


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


def main():
    with open(ROOT_DIR / 'tests/test_cases/test_case1.yaml', 'r', encoding='utf-8') as yamlfile:
        data = yaml.load(yamlfile, yaml.FullLoader)
    print(data)

    lines: List[str] = [
        '# Ontology Description',
    ]
    lines += write_annotations(data['annotations'])

    with open(ROOT_DIR / 'yamd/test.md', 'w', encoding='utf-8') as mdfile:
        mdfile.write('\n'.join(lines))


if __name__ == '__main__':
    # import doctest
    #
    # doctest.testmod()
    main()
