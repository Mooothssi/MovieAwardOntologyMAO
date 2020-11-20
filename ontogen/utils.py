from re import Match, match, search
from typing import Dict, Tuple

from owlready2 import ClassConstruct, ConstrainedDatatype, Not, ObjectProperty, OneOf, Thing

from ontogen.base import Ontology
from ontogen.base.vars import GENERATED_TYPES
from ontogen.internal import CONSTRAINT_DATATYPE_OPERATOR_MAP

__all__ = ('ClassExpToConstruct',)

QUANTIFIER_RESTRICTION_KEYWORDS = ("some", "only")
PROPERTY_RESTRICTION_KEYWORDS = QUANTIFIER_RESTRICTION_KEYWORDS + ("value",)
TRIPLE_LOGICAL_OPERATION_KEYWORDS = ("and", "or")
CARDINALITY_RESTRICTION_KEYWORDS = ("min", "max", "exactly")

TRIPLE_KEYWORDS = (PROPERTY_RESTRICTION_KEYWORDS +
                   TRIPLE_LOGICAL_OPERATION_KEYWORDS +
                   CARDINALITY_RESTRICTION_KEYWORDS)

# (op, nested)
NOT_PATTERN = (r'(not)(?:\(([:a-zA-Z0-9<># ]*)\)| '
               r'((?:[a-z]+:)?[<a-zA-Z0-9>#]+[A-Za-z]*))', (3, 2))
TRIPLE_PATTERN = (r'(?:((?:[a-z]+:)?[<a-zA-Z0-9>#]+[A-Za-z]*)|'
                  r'(\((?:[a-z]+:)?[<a-zA-Z0-9>#]+[A-Za-z]*\))) '
                  rf'({"|".join(TRIPLE_KEYWORDS)}) (?:([0-9]+) )?'
                  r'(?:((?:[a-z]+:)?[<a-zA-Z0-9>#]+[A-Za-z0-9]*(?:\[.+\])?)|'
                  # r'(?:((?:[a-z]+:)?[<a-zA-Z0-9>#]+[A-Za-z0-9\[\]\'<>=]*)|'
                  r'(\((?:[a-z]+:)?[<a-zA-Z0-9>#]+[A-Za-z]*\)))', (2, 1, 6, 5, 4), 3)

PATTERNS = (NOT_PATTERN, TRIPLE_PATTERN)

RESERVED = {"True": True, "False": False, "integer": int}

XSD_LITERAL_DATATYPE_MAP = {
    'integer': int,
    'boolean': bool,
    'string': str,
    'float': float,
    'decimal': float
}


def get_imp_literal_type(literal_entity_name: str):
    if ":" in literal_entity_name:
        literal_entity_name = literal_entity_name.split(":")[1]
    return XSD_LITERAL_DATATYPE_MAP.get(literal_entity_name, literal_entity_name)


def check_constraint_data_types(expression: str) -> ConstrainedDatatype or str:
    """
    Creates a respective ConstrainedDatatype for a given expression

    Args:
        expression: A literal expression

    Returns: The respective ConstrainedDatatype

    >>> check_constraint_data_types("integer[>=40]")
    ConstrainedDatatype(int, min_inclusive = 40)
    """
    constraint_pattern = r'([A-z]+)(?:\[(?:([A-z]+|[<>=]{0,2})) ?(.+)\])?$'
    m = match(constraint_pattern, expression)
    if m is None:
        return expression
    literal, operator, val = get_imp_literal_type(m.group(1)), m.group(2), m.group(3)
    kwargs = {}
    k = CONSTRAINT_DATATYPE_OPERATOR_MAP.get(operator, operator)
    kwargs[k] = literal(val)
    return ConstrainedDatatype(literal, **kwargs)


def get_class_from_literal(onto: Ontology, literal: str, base_cls=Thing):
    if literal in GENERATED_TYPES:
        return GENERATED_TYPES[literal]
    if literal is None:
        return Thing
    new_type = type(str(literal), (base_cls,), {"namespace": onto.implementation})
    GENERATED_TYPES[literal] = new_type
    return new_type


def get_individual_from_literal(onto: Ontology, name: str, cls_literal: str = None, base_cls=Thing):
    short_entity_name = name # f"{onto.base_prefix}:{name}"
    assert short_entity_name in GENERATED_TYPES, f"Individual {short_entity_name} has yet to be created"
    individual = GENERATED_TYPES[short_entity_name]
    return individual
    # cls = get_class_from_literal(onto, cls_literal, base_cls)
    # if cls is Thing:
    #     individual = cls(name, onto.implementation)
    # else:
    #     individual = cls()
    # individual.name = name


class TokenInfo:
    """
        Contains the information of a Token
    """
    def __init__(self, onto: Ontology):
        self.keyword = None
        self.sub_tokens: Tuple[TokenInfo or str, ...] = tuple()
        self.is_class = False
        self.onto = onto
        self.start_index = 0
        self.end_index = 0

    @property
    def count(self):
        return self.end_index - self.start_index

    def get_repr(self):
        return f"<TK#{id(self)}>"

    @property
    def construct(self) -> ClassConstruct or type or bool or int:
        try:
            if self.is_class:
                self.keyword = None
                new_str = self.sub_tokens[0]
                if '[' in new_str:
                    return check_constraint_data_types(new_str)
                if new_str.isdigit():
                    return int(new_str)
                if new_str in GENERATED_TYPES:
                    return GENERATED_TYPES[new_str]
                if new_str in RESERVED:
                    return RESERVED[new_str]
                if ":" in self.sub_tokens[0]:
                    new_str = self.sub_tokens[0].split(":")[1]
                base_cls = Thing
                if self.keyword in QUANTIFIER_RESTRICTION_KEYWORDS:
                    base_cls = ObjectProperty
                return get_class_from_literal(self.onto, new_str, base_cls)
            elif self.keyword in CARDINALITY_RESTRICTION_KEYWORDS:
                first, second, third = self.sub_tokens
                return getattr(first.construct, self.keyword)(third.construct, second.construct)
            elif self.keyword in TRIPLE_KEYWORDS:
                first, second = self.sub_tokens
                if self.keyword in "value":
                    return get_individual_from_literal(self.onto, second.sub_tokens[0])
                elif self.keyword in QUANTIFIER_RESTRICTION_KEYWORDS:
                    return getattr(first.construct, self.keyword)(second.construct)
                elif self.keyword == "and":
                    return first.construct & second.construct
                elif self.keyword == "or":
                    return first.construct | second.construct
            elif self.keyword == "not":
                return Not(self.sub_tokens[0].construct)
        except AttributeError:
            raise SyntaxError("Unable to construct from Class Expression syntax!")

    def __repr__(self):
        if self.keyword == "not":
            return f"^{self.keyword}({self.sub_tokens[0]})"
        elif self.is_class:
            return self.sub_tokens[0]
        else:
            return f"^({self.sub_tokens[0]}) {self.keyword} " \
                   f"({self.sub_tokens[1] if len(self.sub_tokens) > 1 else ''})"


class ClassExpToConstruct:
    """
    A class to convert a Class Expression of `Protege` to a Class Construct of `owlready2`
    """
    def __init__(self, onto: Ontology):
        self.reg_tokens: Dict[str, TokenInfo] = {}
        self.ontology = onto
        self.existing_constructs = []

    def match_registered(self, str_match: str) -> TokenInfo:
        str_match = str_match.replace("(", "").replace(")", "")
        if str_match in self.reg_tokens:
            return self.reg_tokens[str_match]
        else:
            tk = TokenInfo(self.ontology)
            result = self._cls_to_residue(str_match)
            if result == str_match:
                tk.sub_tokens = (result,)
                tk.is_class = True
            else:
                return self.match_registered(result)
            return tk

    def get_match(self, re_pattern: Tuple, recv_string: str):
        result = recv_string
        m = Match
        while m is not None:
            m = search(re_pattern[0], result)
            if m is None:
                break
            tk = TokenInfo(self.ontology)
            tk.sub_tokens = [self.match_registered(n)
                             for n in [m.group(e) for e in re_pattern[1]]
                             if n is not None]
            tk.start_index, tk.end_index = m.span()
            if len(re_pattern) == 3:
                tk.keyword = m.group(re_pattern[2])
            else:
                tk.keyword = "not"
            result = result[:tk.start_index] + tk.get_repr() + result[tk.end_index:]
            self.reg_tokens[tk.get_repr()] = tk
        return result

    def _match_one_of(self, exp):
        m = search(r'^{(.+)}$', exp)
        if m is None:
            return exp
        y = OneOf([get_individual_from_literal(self.ontology, y.strip()) for y in m.group(1).split(",")])
        self.existing_constructs.append(y)
        return

    def _cls_to_residue(self, expression: str):
        residue = expression
        residue = self._match_one_of(residue)
        if residue is None:
            return residue
        for p in PATTERNS:
            residue = self.get_match(p, residue)
        return residue

    def to_construct(self, expression: str) -> ClassConstruct:
        """
        Converts a Class Expression of `Protege` to a Class Construct of `owlready2`
        Args:
            expression: An expression in Class Expression Syntax of Protege

        Returns:
            A ClassConstruct counterpart of the given expression
        """
        self._cls_to_residue(expression)
        construct_list = [j.construct for j in self.reg_tokens.values()]
        construct_list.extend(self.existing_constructs)
        self.reg_tokens.clear()
        self.existing_constructs.clear()
        return construct_list[-1]


if __name__ == '__main__':
    o = Ontology("http://www.semanticweb.org/movie-ontology/ontologies/2020/9/mao#")
    c = ClassExpToConstruct(o)
    print(c.to_construct("(mao:Dog and not(mao:Croc or not(mao:Cat))) or mao:Cat or (mao:Person and mao:Film)"))
