import owlready2
from owlready2 import Imp, get_ontology


class Ontology:
    """
    TODO: A proxy for the real implementation in `owlready2`
    """

    def __init__(self, namespace_iri: str = ""):
        self._internal_onto: owlready2.Ontology = None
        self.namespace_iri = namespace_iri

    def create(self, namespace_iri: str = ""):
        """
            Newly creates an Ontology from an existing namespace
        """
        assert self.namespace_iri == "" or namespace_iri == "", "Namespace must be set before creation"
        self._internal_onto = get_ontology(self.namespace_iri if self.namespace_iri != "" else namespace_iri)

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
