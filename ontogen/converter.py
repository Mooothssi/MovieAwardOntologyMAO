from typing import Dict, List, Union, Tuple
import yaml
from semver import VersionInfo

from ontogen.base import DATATYPE_MAP
from ontogen.base.namespaces import OWL_EQUIVALENT_CLASS, OWL_RESTRICTION, OWL_INDIVIDUAL, RDF_TYPE, OWL_THING
from ontogen.primitives import (BASE_ENTITIES, COMMENT_ENTITY_NAME, LABEL_ENTITY_NAME, PROPERTY_ENTITIES,
                                Ontology, OwlEntity, OwlClass, OwlDataProperty,
                                OwlObjectProperty, absolutize_entity_name)
from ontogen.primitives.classes import OwlIndividual


def get_equivalent_datatype(entity_name: str) -> Union[type, str]:
    return DATATYPE_MAP.get(entity_name, entity_name)


class OntogenConverter:
    """
        A converter from YAML to an abstraction of OWL ontology
        Needs to be actualized by an instance of the class ``Ontology``.
    """
    SUPPORTED_VERSION = "1.1.0"

    def __init__(self):
        """Loads a file with the given name into a skeleton of an OWL ontology.
        """
        self.entities: Dict[str, OwlEntity] = {}
        self.ontology = Ontology()
        self.ontology.name_from_prefix()
        self.file_version = ""
        self.individuals: List[OwlIndividual] = []
        self._missing_entities = set()
        self._dct = {}

    @property
    def prefix(self) -> str:
        return self.ontology.base_prefix

    def _add_rules(self, base_dict: dict):
        b = base_dict.get("rules", {})
        for rule_name in b:
            self.ontology.add_rule(b[rule_name]["rule"], rule_name)

    def _deal_with_iris(self, base_dict: dict):
        self.ontology.base_iri = base_dict.get("iri", "")
        prefixes = base_dict.get("prefixes", {})
        try:
            [self.ontology.update_iri(prefix, prefixes[prefix]) for prefix in prefixes]
        except KeyError:
            raise AssertionError("Please define prefix for the base IRI of this Ontology")
        else:
            self.ontology.update_base_prefix()
            self.ontology.create()

    def _check_eligible_version(self, base_dict: dict):
        self.file_version = base_dict["version"].replace("v", "")
        if (VersionInfo.parse(self.file_version)
                .compare(VersionInfo.parse(OntogenConverter.SUPPORTED_VERSION)) > 0):
            raise AssertionError("Unsupported version of file")

    def read_yaml(self, spec_filename: str):
        """Internally reads a file with the given filename

        Args:
            spec_filename: The filename of a specs file in YAML
        """
        with open(spec_filename) as f:
            self._dct = yaml.load(f, Loader=yaml.Loader)
            root = self._dct
        self._check_eligible_version(root)
        self._deal_with_iris(root)
        temp_classes = []

        for base in BASE_ENTITIES:
            cls = base
            q = base.get_entity_name()
            if q not in root:
                continue
            classes = root[q]
            for class_entity_name in classes:
                if class_entity_name == OWL_THING:
                    continue
                e = absolutize_entity_name(class_entity_name, self.prefix)
                prefix, name = e.split(":")
                obj = cls(e)
                obj.prefix = prefix
                sub = classes[class_entity_name]
                if isinstance(sub, dict):
                    if base == OwlObjectProperty:
                        obj._characteristics = sub.get(RDF_TYPE, [])
                        obj.range = sub.get("rdfs:range", [])
                        inv = sub.get("owl:inverseOf", [])
                        if len(inv) == 1:
                            obj.inverse_prop = inv[0]
                    elif base == OwlDataProperty:
                        if "rdfs:range" in sub:
                            obj.range = [get_equivalent_datatype(datatype) for datatype in sub["rdfs:range"]]
                    annotations = sub.get("annotations", {})
                    obj.add_labels(annotations.get(LABEL_ENTITY_NAME, [None]))
                    obj.add_comments(annotations.get(COMMENT_ENTITY_NAME, [None]))
                if base == OwlClass:
                    obj._internal_dict = sub
                    obj.parent_class_names = sub.get("rdfs:subClassOf", [])
                    obj.disjoint_class_names = sub.get("owl:disjointWith", [])
                    obj.equivalent_class_expressions = self._get_equivalent_classes(sub)
                    for prop in PROPERTY_ENTITIES:
                        if prop not in sub:
                            continue
                        prop_class = sub[prop]
                        for prop_name in prop_class:
                            prop_qualifier = absolutize_entity_name(prop_name)
                            obj.defined_properties[prop_qualifier] = self.get_entity(prop_name)
                    temp_classes.append(obj)
                self.entities[class_entity_name] = obj
        self._add_individuals(root)
        if "annotations" in root:
            anno = root["annotations"]
            self.ontology.add_label(anno["rdfs:label"][0])
            self.ontology.add_annotation("license", anno["dcterms:license"][0])
            self.ontology.add_annotation("title", anno["dc:title"][0])
        self._load_class_descriptions(tuple(self.entities.values()))
        self.ontology.entities = self.entities

    def write_yaml(self, owl_filename: str, spec_filename: str):
        onto = Ontology.load_from_file(owl_filename)
        dct = {'version': self.SUPPORTED_VERSION, 'iri': onto.base_iri, 'prefixes': onto.iris,
               'annotations': onto.annotations}
        with open(spec_filename, "w") as f:
            self._dct = yaml.dump(dct, f)

    def _add_individuals(self, base_dict: dict):
        individuals = base_dict[OWL_INDIVIDUAL]
        for individual in individuals:
            ind = OwlIndividual(individual)
            for t in individuals[individual]:
                val = individuals[individual][t]
                for value in val:
                    if t == RDF_TYPE:
                        entity = self.get_entity(value)
                        ind.be_type_of(entity)
                    else:
                        ind.add_property_assertion(t, value)
            self.individuals.append(ind)

    @staticmethod
    def _get_equivalent_classes(sub_dict: dict) -> List:
        if OWL_EQUIVALENT_CLASS not in sub_dict:
            return []
        u = sub_dict[OWL_EQUIVALENT_CLASS]
        if isinstance(u, dict):
            return u.get(OWL_RESTRICTION, [])
        else:
            return u

    def _load_class_descriptions(self, classes: Tuple[OwlEntity, ...]):
        for cls in classes:
            if isinstance(cls, OwlClass) or isinstance(cls, OwlObjectProperty):
                [cls.add_superclass(self.get_entity(name, cls.prefix)) for name in cls.parent_class_names]
                if isinstance(cls, OwlClass):
                    [cls.add_disjoint_class(self.get_entity(name, cls.prefix)) for name in cls.disjoint_class_names]
                elif isinstance(cls, OwlObjectProperty):
                    cls.range = [self.get_entity(name, cls.prefix) for name in cls.range if isinstance(name, str)]
                    cls.inverse_prop = self.get_entity(cls.inverse_prop)

    def get_entity(self, entity_name: str, prefix: str = None) -> Union[OwlClass, OwlEntity, str]:
        if entity_name is None:
            return None
        if prefix is None:
            prefix = self.prefix
        modified_name = absolutize_entity_name(entity_name, prefix)
        if modified_name == "owl:Thing" or modified_name == f"{prefix}:Thing":
            return None
        try:
            if modified_name in self._missing_entities:
                self._missing_entities.remove(modified_name)
            return self.entities[modified_name]
        except KeyError:
            self._missing_entities.add(modified_name)
            return modified_name

    def check_missing_definitions(self):
        if len(self._missing_entities) > 0:
            missing = "\n".join([f"- {e}" for e in self._missing_entities])
            raise AssertionError(f"There are missing entities as follows. "
                                 f"Please check the consistency of the given specs!\n{missing}")

    def list_entities(self):
        """Print out list of entities to the console
        """
        for entity in self.entities:
            print(f"- {entity}: {self.entities[entity].__class__.__name__}")

    def export_to_ontology(self, onto: Ontology = None) -> Ontology:
        """Saves changes made into a given Ontology

        Args:
            onto: A given Ontology

        Returns:
            A resultant Ontology
        """
        self.check_missing_definitions()
        if onto is None:
            onto = self.ontology
            onto.name_from_prefix()
        onto.create()
        for entity in self.entities.values():
            entity.actualize(onto)
        self._add_rules(self._dct)
        onto.actualize()
        return onto
