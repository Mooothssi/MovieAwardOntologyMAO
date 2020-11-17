from re import search, Match
from typing import Dict, List, Tuple

from owlready2 import ClassConstruct, Not, Thing
# ConstrainedDatatype
from ontogen.base import GENERATED_TYPES, Ontology

innermost_pattern = r'((?:\()([^\(\)]+) (and|or) ([^\(\)]+)(?:\)))'
normal_pattern = r'(.+) (and|or) (.+)'
# (op, nested)
NOT_PATTERN: Tuple[str, List[int]] = (r'(not)(?:\(([^\(\)]+)\)| (.+))', [3, 2])
NEW_NOT_PATTERN = (r'(not)(?:\(([:a-zA-Z0-9<># ]*)\)| '
                   r'((?:[a-z]+:)?[<a-zA-Z0-9>#]+[A-Za-z]*))', (3, 2))
AND_OR_PAREN_PATTERN = (r'\((.+)\) (and|or) \((.+)\)', (1, 3), 2)
TRIPLE_PATTERN = (r'(?:((?:[a-z]+:)?[<a-zA-Z0-9>#]+[A-Za-z]*)|'
                  r'(\((?:[a-z]+:)?[<a-zA-Z0-9>#]+[A-Za-z]*\))) '
                  r'(and|or|some|value) '
                  r'(?:((?:[a-z]+:)?[<a-zA-Z0-9>#]+[A-Za-z]*)|'
                  r'(\((?:[a-z]+:)?[<a-zA-Z0-9>#]+[A-Za-z]*\)))', (2, 1, 5, 4), 3)
# not is a double (not Pet) and can be parenthesized {not (Pet)}

PATTERNS = (NEW_NOT_PATTERN, TRIPLE_PATTERN)

RESERVED = {"True": True, "False": False, "integer": int}


class TokenInfo:
    start_index: int
    end_index: int
    operator: str
    sub_tokens: List["TokenInfo"]

    def __init__(self, onto: Ontology):
        self.operator = ""
        self.sub_tokens = ["", ""]
        self.raw_str: Tuple[TokenInfo, TokenInfo] = ("", "")
        self.is_class = False
        self.onto = onto.implementation

    @property
    def count(self):
        return self.end_index - self.start_index

    def get_repr(self):
        return f"<TK#{id(self)}>"

    @property
    def construct(self) -> ClassConstruct or type or bool:
        if self.is_class:
            new_str = self.raw_str[0]
            if new_str in GENERATED_TYPES:
                return GENERATED_TYPES[new_str]
            if new_str in RESERVED:
                return RESERVED[new_str]
            if ":" in self.raw_str[0]:
                new_str = self.raw_str[0].split(":")[1]
            return type(str(new_str), (Thing,),
                        {"namespace": self.onto})
        elif self.operator == "and":
            first, second = self.raw_str
            return first.construct & second.construct
        elif self.operator == "or":
            first, second = self.raw_str
            return first.construct | second.construct
        elif self.operator == "some":
            first, second = self.raw_str
            return first.construct.some(second.construct)
        elif self.operator == "value":
            first, second = self.raw_str
            return first.construct.value(second.construct)
        elif self.operator == "not":
            return Not(self.raw_str[0].construct)

    def __repr__(self):
        if self.operator == "not":
            return f"%{self.operator}({self.raw_str[0]})"
        elif self.is_class:
            return self.raw_str[0]
        else:
            return f"%({self.raw_str[0]}) {self.operator} " \
                   f"({self.raw_str[1] if len(self.raw_str) > 1 else ''})"


class ClassExpToConstruct:
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
                tk.raw_str = (result,)
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
            tk.raw_str = [self.match_registered(n)
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
