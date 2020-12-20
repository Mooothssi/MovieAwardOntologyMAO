from contextlib import contextmanager
import pickle

import spacy
import typing

from dirs import ROOT_DIR
from utils.misc import depreciated

nlp = spacy.load("en_core_web_sm")


class M:
    file = 'mapping/{}.pickle'
    resources = {}

    @classmethod
    def write_resource(cls, name: str, value: object):
        cls.resources[name] = value
        cls.dump_resource(name)

    @classmethod
    def load_resource(cls, name: str) -> typing.List[str]:
        with open(ROOT_DIR / cls.file.format(name), 'rb') as file:
            cls.resources[name] = pickle.load(file)
            return cls.resources[name]

    @classmethod
    def dump_resource(cls, name: str):
        with open(ROOT_DIR / cls.file.format(name), 'wb') as file:
            pickle.dump(cls.resources[name], file)


@depreciated("Use get_resources() instead")
@contextmanager
def get_person_names():
    # Code to acquire resource, e.g.:
    person_names = M.load_resource('person_names')
    try:
        yield person_names
    finally:
        # Code to release resource, e.g.:
        M.dump_resource('person_names')


@contextmanager
def get_resources(*names):
    # Code to acquire resource, e.g.:
    resources = [M.load_resource(name) for name in names]
    try:
        yield resources
    finally:
        # Code to release resource, e.g.:
        for name in names:
            M.dump_resource(name)


def categorize(s: str) -> typing.Tuple[str, str]:
    doc = nlp(s)
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            person = ent.text
            return 'PERSON', s
        elif ent.label_ == 'ORG':
            organization = ent.text
            return 'ORG', s
        print(ent.text, ent.start_char, ent.end_char, ent.label_)

    with get_resources('person_names', 'org_names') as (person_names, org_names):
        if s in person_names:
            return 'PERSON', s
        if s in org_names:
            return 'ORG', s

        res = input(f"Is '{s}' a person or an organization? (1/2) or replace ('r'): ")
        if res == '1':
            person_names.append(s)
            return 'PERSON', s
        if res == '2':
            org_names.append(s)
            return 'ORG', s
        if res == 'r':
            repl = input("Replace with: ")
            return categorize(repl)


def get_not_person_name(s1: str, s2: str) -> str:
    """ Returns one of the two inputs that are not people names. """
    if s1 is None or s2 is None:
        raise TypeError(f"s1 and s2 must be str, not {s1} {s2}")
    person = None
    doc = nlp(s1)
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            person = ent.text
        print(ent.text, ent.start_char, ent.end_char, ent.label_)
    if person is not None:
        return s2

    doc = nlp(s2)
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            person = ent.text
        print(ent.text, ent.start_char, ent.end_char, ent.label_)
    if person is not None:
        return s1

    with get_person_names() as person_names:
        if s1 in person_names:
            if s2 not in person_names:
                return s2
            else:
                raise ValueError(f"Both '{s1}' and '{s2}' are names")
        elif s2 in person_names:
            return s1
        else:
            res = input(f"Choose between '{s1}' or '{s2}' as the person (1/2): ")
            if res == '1':
                person_names.append(s1)
                return s2
            if res == '2':
                person_names.append(s2)
                return s1
        # raise ValueError(f"IDK who is a person! between {s1} and {s2}")
