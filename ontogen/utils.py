from re import search, Match
from typing import Dict, Tuple

from owlready2 import ClassConstruct, Not, ObjectProperty, Thing

from ontogen.base import GENERATED_TYPES, Ontology

innermost_pattern = r'((?:\()([^\(\)]+) (and|or) ([^\(\)]+)(?:\)))'

QUANTIFIER_RESTRICTION_KEYWORDS = ("some", "only")
TRIPLE_LOGICAL_OPERATION_KEYWORDS = ("and", "or")

TRIPLE_KEYWORDS = (QUANTIFIER_RESTRICTION_KEYWORDS +
                   TRIPLE_LOGICAL_OPERATION_KEYWORDS +
                   ("value",))

# (op, nested)
NOT_PATTERN = (r'(not)(?:\(([:a-zA-Z0-9<># ]*)\)| '
               r'((?:[a-z]+:)?[<a-zA-Z0-9>#]+[A-Za-z]*))', (3, 2))
TRIPLE_PATTERN = (r'(?:((?:[a-z]+:)?[<a-zA-Z0-9>#]+[A-Za-z]*)|'
                  r'(\((?:[a-z]+:)?[<a-zA-Z0-9>#]+[A-Za-z]*\))) '
                  rf'({"|".join(TRIPLE_KEYWORDS)}) '
                  r'(?:((?:[a-z]+:)?[<a-zA-Z0-9>#]+[A-Za-z]*)|'
                  r'(\((?:[a-z]+:)?[<a-zA-Z0-9>#]+[A-Za-z]*\)))', (2, 1, 5, 4), 3)

PATTERNS = (NOT_PATTERN, TRIPLE_PATTERN)

RESERVED = {"True": True, "False": False, "integer": int}


class TokenInfo:
    """
        Contains the information of a Token
    """
    def __init__(self, onto: Ontology):
        self.operator = ""
        self.sub_tokens: Tuple[TokenInfo or str, ...] = tuple()
        self.is_class = False
        self.onto = onto.implementation
        self.start_index = 0
        self.end_index = 0

    @property
    def count(self):
        return self.end_index - self.start_index

    def get_repr(self):
        return f"<TK#{id(self)}>"

    @property
    def construct(self) -> ClassConstruct or type or bool:
        try:
            if self.is_class:
                new_str = self.sub_tokens[0]
                if new_str in GENERATED_TYPES:
                    return GENERATED_TYPES[new_str]
                if new_str in RESERVED:
                    return RESERVED[new_str]
                if ":" in self.sub_tokens[0]:
                    new_str = self.sub_tokens[0].split(":")[1]
                base_cls = Thing
                if self.operator in QUANTIFIER_RESTRICTION_KEYWORDS:
                    base_cls = ObjectProperty
                new_type = type(str(new_str), (base_cls,), {"namespace": self.onto})
                GENERATED_TYPES[new_str] = new_type
                return new_type
            elif self.operator == "and":
                first, second = self.sub_tokens
                return first.construct & second.construct
            elif self.operator == "or":
                first, second = self.sub_tokens
                return first.construct | second.construct
            elif self.operator == "some":
                first, second = self.sub_tokens
                return first.construct.some(second.construct)
            elif self.operator == "value":
                first, second = self.sub_tokens
                return first.construct.value(second.construct)
            elif self.operator == "not":
                return Not(self.sub_tokens[0].construct)
        except AttributeError:
            raise SyntaxError("Unable to construct from Class Expression syntax!")

    def __repr__(self):
        if self.operator == "not":
            return f"%{self.operator}({self.sub_tokens[0]})"
        elif self.is_class:
            return self.sub_tokens[0]
        else:
            return f"%({self.sub_tokens[0]}) {self.operator} " \
                   f"({self.sub_tokens[1] if len(self.sub_tokens) > 1 else ''})"


# TODO: ConstrainedDatatype
class ClassExpToConstruct:
    """
    A class to convert a Class Expression of `Protege` to a Class Construct of `owlready2`
    """
    def __init__(self, onto: Ontology):
        self.reg_tokens: Dict[str, TokenInfo] = {}
        self.ontology = onto

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
                             for n in [m.group(e)
                                    for e in re_pattern[1]]
                             if n is not None]
            tk.start_index, tk.end_index = m.span()
            if len(re_pattern) == 3:
                tk.operator = m.group(re_pattern[2])
            else:
                tk.operator = "not"
            result = result[:tk.start_index] + tk.get_repr() + result[tk.end_index:]
            self.reg_tokens[tk.get_repr()] = tk
        return result

    def _cls_to_residue(self, expression: str):
        residue = expression
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
        self.reg_tokens.clear()
        return construct_list[-1]


if __name__ == '__main__':
    c = ClassExpToConstruct(Ontology("http://www.semanticweb.org/movie-ontology/ontologies/2020/9/mao#"))
    c.to_construct("(mao:Dog and not(mao:Croc or not(mao:Cat))) or mao:Cat or (mao:Person and mao:Film)")
