import re
from re import Match
from typing import Dict, List, Tuple
import types
from owlready2 import *

innermost_pattern = r'((?:\()([^\(\)]+) (and|or) ([^\(\)]+)(?:\)))'
normal_pattern = r'(.+) (and|or) (.+)'
# (op, nested)
NOT_PATTERN: Tuple[str, List[int]] = (r'(not)(?:\(([^\(\)]+)\)| (.+))', [3, 2])
AND_OR_PAREN_PATTERN = (r'\((.+)\) (and|or) \((.+)\)', [1, 3], 2)
LOGICAL_PAREN_PATTERN = (r'((?:\()([^\(\)]+) (and|or) ([^\(\)]+)(?:\)))', [2, 4], 3)
NO_PAREN = r'(([a-z]+:)?[<A-Z>]+[a-z]*) (and|or|some) (([a-z]+:)?[<A-Z>]+[a-z]*)'
TRIPLE_PATTERN = (r'(?:((?:[a-z]+:)?[<A-Z0-9>#]+[a-z]*)|'
                  r'(\((?:[a-z]+:)?[<A-Z0-9>#]+[a-z]*\))) '
                  r'(and|or|some) '
                  r'(?:((?:[a-z]+:)?[<A-Z0-9>#]+[a-z]*)|'
                  r'(\((?:[a-z]+:)?[<A-Z0-9>#]+[a-z]*\)))', [5, 4], 3, [2, 1])
# not is a double (not Pet) and can be parenthesized {not (Pet)}

PATTERNS = (NOT_PATTERN, TRIPLE_PATTERN)


class TokenInfo:
    start_index: int
    end_index: int
    operator: str
    sub_tokens: List["TokenInfo"]

    def __init__(self):
        self.operator = ""
        self.sub_tokens = ["", ""]
        self.raw_str: Tuple[TokenInfo, TokenInfo] = ("", "")
        self.is_class = False

    @property
    def count(self):
        return self.end_index - self.start_index

    def get_repr(self):
        return f"<TK#{id(self)}>"

    @property
    def construct(self) -> ClassConstruct or type:
        if self.is_class:
            new_str = self.raw_str[0]
            if ":" in self.raw_str[0]:
                new_str = self.raw_str[0].split(":")[1]
            return type(str(new_str), (Thing,),
                        {"namespace": get_ontology("http://www.semanticweb.org/movie-ontology/ontologies/2020/9/mao#")})
        elif self.operator == "and":
            first, second = self.raw_str
            return first.construct & second.construct
        elif self.operator == "or":
            first, second = self.raw_str
            return first.construct | second.construct
        elif self.operator == "not":
            return Not(self.raw_str[0].construct)

    def __repr__(self):
        if self.operator == "not":
            return f"%{self.operator}({self.raw_str[0]})"
        else:
            return f"%({self.raw_str[0]}) {self.operator} ()"


class ClassExpToConstruct:
    def __init__(self):
        self.reg_tokens: Dict[str, TokenInfo] = {}

    def match_registered(self, str_match: str) -> TokenInfo:
        str_match = str_match.replace("(", "").replace(")", "")
        if str_match in self.reg_tokens:
            return self.reg_tokens[str_match]
        else:
            tk = TokenInfo()
            r = self._cls_to_residue(str_match)
            tk.raw_str = (str_match,)
            tk.is_class = True
            return tk

    def get_triple_match(self, recv_string: str):
        result = recv_string
        m = Match
        while m is not None:
            m = re.search(TRIPLE_PATTERN[0], result)
            if m is None:
                break
            tk = TokenInfo()
            q = m.groups()
            p = tuple(set(TRIPLE_PATTERN[1] + TRIPLE_PATTERN[3]))
            tk.raw_str = [self.match_registered(n)
                          for n in [m.group(e)
                                    for e in p]
                          if n is not None]
            tk.start_index, tk.end_index = m.span()
            tk.operator = m.group(TRIPLE_PATTERN[2])
            result = result[:tk.start_index] + tk.get_repr() + result[tk.end_index:]
            self.reg_tokens[tk.get_repr()] = tk
        return result

    def get_match(self, re_pattern: Tuple, recv_string: str) -> str:
        m = re.search(re_pattern[0], recv_string)
        if m is None:
            return recv_string
        tk = TokenInfo()
        tk.raw_str = [self.match_registered(n)
                      for n in [m.group(e) for e in re_pattern[1]]
                      if n is not None]
        tk.start_index, tk.end_index = m.span()
        if len(re_pattern) == 3:
            tk.operator = m.group(re_pattern[2])
        else:
            tk.operator = "not"
        res = recv_string[:tk.start_index] + tk.get_repr() + recv_string[tk.end_index:]
        self.reg_tokens[tk.get_repr()] = tk
        return res

    def _cls_to_residue(self, expression: str):
        residue = self.get_match(NOT_PATTERN, expression)
        residue = self.get_triple_match(residue)
        return residue

    def class_expression_to_construct(self, expression: str):
        """
        to `owlready` Class Construct
        :param expression:
        :return:
        """
        self._cls_to_residue(expression)
        construct_list = [j.construct for j in self.reg_tokens.values()]
        self.reg_tokens.clear()
        return construct_list[-1]


if __name__ == '__main__':
    c = ClassExpToConstruct()
    print(c.class_expression_to_construct("(mao:Dog and mao:Croc) or mao:Cat or (mao:Person and mao:Film)"))
