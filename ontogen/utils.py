import re


class BinaryTree:
    def __init__(self):
        self.left = ""
        self.op = "and"
        self.right = ""
        self.previous = None

    @property
    def is_empty(self):
        return self.left == "" or self.right == ""

    def __str__(self):
        return f"{self.left} {self.op} {self.right} -> {self.previous}"


innermost_pattern = r'((?:\()([^\(\)]+) (and|or) ([^\(\)]+)(?:\)))'
normal_pattern = r'(.+) (and|or) (.+)'


def class_expression_to_construct(expression: str, bintree: BinaryTree = None) -> BinaryTree:
    """
    to `owlready` Class Construct
    :param expression:
    :return:

    #>>> class_expression_to_construct("Drug and not(hasForActivePrinciple some ActivePrinciple)")
    [Drug & Not(has_for_active_principle.some(ActivePrinciple))]
    """
    try:
        m, idx = next(u for u in [(re.search(p[0], expression), p[1]) for p in [
            (innermost_pattern, (2, 3, 4)),
            (normal_pattern, (1, 2, 3)),
        ]] if u[0] is not None)
    except StopIteration:
        return bintree
    new_bintree = BinaryTree()
    new_bintree.previous = bintree
    new_bintree.left = m.group(idx[0])
    new_bintree.op = m.group(idx[1])
    new_bintree.right = m.group(idx[2])

    subexpression = re.sub(innermost_pattern, "<rp>", expression)
    if subexpression != expression:
        return class_expression_to_construct(subexpression, new_bintree)
    else:
        return bintree
    #
    # if left == "<rp>":
    #     bintree.left = existing_bintree
    # else:
    #     leftmost = class_expression_to_construct(left, inner)
    #     if leftmost.is_empty:
    #         bintree.left = m.group(idx[0])
    #     else:
    #         bintree.left = leftmost
    # if right == "<rp>":
    #     bintree.right = existing_bintree
    # else:
    #     bintree.right = right
    # bintree.op = m.group(idx[1])

    return new_bintree


print(class_expression_to_construct("Dog and (not Cat and Cat) and (hasPet some (Dog and ((((Dog and ((Dog and F and Cat) and Cat)) and Cat) and Cat) and Cat)))"))
