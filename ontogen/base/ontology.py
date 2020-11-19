import owlready2
from owlready2 import Imp, get_ontology
from typing import Dict, Optional

from .namespaces import lookup_iri
from .annotatable import OwlAnnotatable


def get_ontology_from_prefix(prefix: str, ld: dict):
    return get_ontology(lookup_iri(prefix, ld))


FREE_DOMAIN = "http://www.semanticweb.org"


class Ontology(OwlAnnotatable):
    """
    TODO: A proxy for the real implementation in `owlready2`
    """
    license: str
    seeAlso: str
    contributor: str
    comment: str

    def __init__(self, base_iri: str = "", base_prefix: str = ""):
        self._internal_onto: owlready2.Ontology or None = None
        self.base_iri = base_iri
        self.base_prefix = base_prefix
        self.iris: Dict[str, str] = {}
        self.annotations = {}

    def name_from_prefix(self, developer: str = "nomad"):
        import datetime
        now = datetime.datetime.now()
        self.base_iri = f"{FREE_DOMAIN}/{developer}/ontologies/{now.year}/{now.month}/{self.base_prefix}#"

    def _get_onto_from_prefix(self, prefix: str) -> owlready2.Ontology:
        return get_ontology_from_prefix(prefix, self.iris)

    def lookup_iri(self, prefix: str):
        """
        Get a fully qualified IRI from a given prefix
        Args:
            prefix:

        Returns:

        """
        return lookup_iri(prefix, self.iris)

    def lookup_prefix(self, iri: str):
        """
         Get a fully qualified prefix from a given IRI
        Args:
            iri:

        Returns:

        """
        return lookup_iri(iri, self.prefixes)

    def update_base_prefix(self):
        self.base_prefix = self.lookup_prefix(self.base_iri)

    @property
    def prefixes(self):
        return {v: k for k, v in self.iris.items()}

    def create(self, namespace_iri: str = ""):
        """
            Newly creates an Ontology from an existing namespace
        """
        assert self.base_iri == "" or namespace_iri == "", "Namespace must be set before creation"
        self.base_iri = self.base_iri if self.base_iri != "" else namespace_iri
        self._internal_onto = get_ontology(self.base_iri)
        self.base_prefix = self.implementation.name
        self.update_iri()

    def update_iri(self, prefix: Optional[str] = None, iri: Optional[str] = None):
        if prefix is None:
            prefix = self.base_prefix
        if iri is None:
            iri = self.base_iri
        self.iris[prefix] = iri

    @classmethod
    def load_from_file(cls, filename: str) -> "Ontology":
        """
        Loads an Ontology from an existing file

        Args:
            filename: The name of a given file

        Returns: An Ontology object

        """
        inst = cls()
        inst._internal_onto = get_ontology(f"file:////{filename}")
        inst._internal_onto.load()
        inst.base_iri, inst.base_prefix = inst.implementation.base_iri, inst.implementation.name
        inst.update_iri()
        return inst

    def save_to_file(self, filename: str, file_format: str="rdfxml"):
        """
        Saves an Ontology with a given filename

        Args:
            filename: The name of a given file
            file_format: The file format of given filename. Only `rdfxml` is supported by `owlready2`
        """
        self.implementation.save(file=filename, format=file_format)

    def add_rule(self, swrl_rule: str, rule_name: str = None, comment: str = None):
        """
        Adds a SWRL rule to the Ontology

        Args:
            swrl_rule: A rule definition in SWRL
            rule_name: The name of the given rule in `rdfs:label`
            comment: An `rdfs:comment` on the given rule
        """
        rule = Imp(namespace=self.implementation)
        if rule_name is not None:
            rule.label = rule_name
        if comment is not None:
            rule.comment = comment
        rule.set_as_rule(swrl_rule.replace(f"{self.base_name}:", "").replace("^ ", ", "))

    @property
    def implementation(self) -> owlready2.Ontology:
        if self._internal_onto is None:
            self.create()  # lazy creation
        return self._internal_onto

    @property
    def base_name(self):
        return self.implementation.name

    def add_label(self, label: str or int):
        self.add_annotation("rdfs:label", label)

    def add_license(self, label: str or int):
        self.add_annotation("dcterms:licence", label)

    def add_annotation(self, annotation: str, value):
        if annotation not in self.annotations:
            self.annotations[annotation] = []
        self.annotations[annotation].append(value)

    def actualize(self):
        self.properties_values = self.annotations
        self.actualize_annotations(self)
        for a in self.annotations:
            name = a
            if ":" in a:
                name = a.split(":")[1]
            for t in self.annotations[a]:
                getattr(self.implementation.metadata, name).append(t)
