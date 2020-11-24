from typing import Any, Dict, List, Union, Tuple, Type
import yaml
from owlready2 import AnnotationPropertyClass, ClassValueList, DataPropertyClass, ObjectPropertyClass, Thing, IndividualValueList
from semver import VersionInfo

from ontogen.base import DATATYPE_MAP
from ontogen.base.namespaces import OWL_EQUIVALENT_CLASS, OWL_RESTRICTION, OWL_INDIVIDUAL, RDF_TYPE, OWL_THING, \
    OWL_CLASS, OWL_ANNOTATION_PROPERTY, OWL_OBJECT_PROPERTY, OWL_DATA_PROPERTY
from ontogen.primitives import (BASE_ENTITIES, COMMENT_ENTITY_NAME, LABEL_ENTITY_NAME, PROPERTY_ENTITIES,
                                Ontology, OwlEntity, OwlClass, OwlDataProperty,
                                OwlObjectProperty)
from ontogen.utils.basics import absolutize_entity_name
from ontogen.primitives.classes import OwlIndividual
from ontogen.utils.basics import assign_optional_dct


def get_equivalent_datatype(entity_name: str) -> Union[type, str]:
    return DATATYPE_MAP.get(entity_name, entity_name)


class OntogenConverter:
    """
        A converter from YAML to an abstraction of OWL ontology
        Needs to be actualized by an instance of the class ``Ontology``.
    """
    SUPPORTED_VERSION = "2.1.0"

    def __init__(self):
        """Loads a file with the given name into a skeleton of an OWL ontology.
        """
        self.entities: Dict[str, Union[OwlEntity, OwlIndividual]] = {}
        self.ontology = Ontology()
        self.ontology.generate_base_iri_from_prefix()
        self.file_version = ""
        self._individuals: List[OwlIndividual] = []
        self._missing_entities = set()
        self._dct = {}

    @property
    def prefix(self) -> str:
        return self.ontology.base_prefix

    def _add_rules(self, base_dict: dict):
        b = base_dict.get("rules", {})
        for rule_name in b:
            self.ontology.add_rule(b[rule_name]["rule"][0], rule_name)

    def _deal_with_iris(self, base_dict: dict):
        self.ontology.base_iri = base_dict.get("iri", "")
        prefixes = base_dict.get("prefixes", {})
        try:
            [self.ontology.define_prefix(prefix, prefixes[prefix]) for prefix in prefixes]
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

    def load_from_spec(self, spec_filename: str):
        """Creates an abstract Ontology from a specs file with the given filename

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
            q = base.get_owl_type_entity_name()
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
                    obj.parent_class_names = sub.get("rdfs:subClassOf", [])
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
                self.entities[absolutize_entity_name(class_entity_name)] = obj
        self._add_individuals(root)
        if "annotations" in root:
            anno = root["annotations"]
            self.ontology.add_label(anno["rdfs:label"][0])
            self.ontology.add_annotation("license", anno["dcterms:license"][0])
            self.ontology.add_annotation("title", anno["dc:title"][0])
        self._load_class_descriptions(tuple(self.entities.values()))
        self.ontology.entities = self.entities

    def write_yaml(self, owl_filename: str, spec_filename: str):
        self.ontology = Ontology.load_from_file(owl_filename)
        onto = self.ontology
        with onto.implementation:
            g = onto.rdflib_graph
            namespaces = dict(g.namespaces())
            for k in namespaces:
                self.ontology.define_prefix(k, str(namespaces[k]))
        internals = self._from_internals_to_dict()
        dct = {'version': self.SUPPORTED_VERSION,
               'iri': onto.base_iri,
               'prefixes': onto.iris,
               'annotations': onto.annotations}
        dct.update(internals)
        with open(spec_filename, "w") as f:
            self._dct = yaml.dump(dct, f)

    def _add_individuals(self, base_dict: dict):
        individuals = base_dict.get(OWL_INDIVIDUAL, {})
        for individual in individuals:
            ind = OwlIndividual(individual)
            for t in individuals[individual]:
                values = individuals[individual][t]
                if t == RDF_TYPE:
                    for value in values:
                        entity = self.get_entity(value)
                        ind.be_type_of(entity)
                elif t == "relations":
                    for key in values:
                        ind.add_property_assertion(key, values[key])
            self.individuals[individual] = ind

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
            onto.generate_base_iri_from_prefix()
        onto.create()
        for entity in self.entities.values():
            entity.actualize(onto)
        self._add_rules(self._dct)
        onto.actualize()
        return onto

    @property
    def individuals(self):
        return self._get_with_type(OwlIndividual)

    @property
    def classes(self):
        return self._get_with_type(OwlClass)

    @property
    def object_properties(self):
        return self._get_with_type(OwlObjectProperty)

    @property
    def data_properties(self):
        return self._get_with_type(OwlDataProperty)

    def _get_with_type(self, t: Type[Union[OwlEntity, OwlIndividual]]):
        return {x: self.entities[x] for x in self.entities if isinstance(self.entities[x], t)}

    def _from_internals_to_dict(self) -> dict:
        onto = self.ontology
        classes: List[Thing] = list(onto.implementation.classes())
        props: List[Thing] = list(onto.implementation.properties())
        individuals: List[Thing] = list(onto.implementation.individuals())
        all_three = classes + props + individuals
        for cls in classes:
            p = onto.lookup_prefix(cls.namespace.base_iri)
            e = absolutize_entity_name(cls.name, p)
            c = OwlClass(e)
            for p in Thing.get_properties(cls):
                if isinstance(p, AnnotationPropertyClass):
                    c.retrieve_builtin_prop(p.name, cls, self.ontology.lookup_prefix(p.namespace.base_iri))
            c.parent_class_names = [absolutize_entity_name(s.name) for s in cls.is_a]
            self.entities[e] = c
        for prop in props:
            p = onto.lookup_prefix(prop.namespace.base_iri)
            e = absolutize_entity_name(prop.name, p)
            if isinstance(prop, DataPropertyClass):
                dp = OwlDataProperty(e)
                self.entities[e] = dp
                dp.parent_class_names = [absolutize_entity_name(s.name) for s in prop.is_a]
            elif isinstance(prop, ObjectPropertyClass):
                op = OwlObjectProperty(e)
                self.entities[e] = op
                op.parent_class_names = [absolutize_entity_name(s.name) for s in prop.is_a]
        for individual in individuals:
            p = onto.lookup_prefix(individual.namespace.base_iri)
            e = absolutize_entity_name(individual.name, p)
            i = OwlIndividual(e)
            for x in dir(individual):
                p = getattr(individual, x)
                if isinstance(p, ClassValueList) or isinstance(p, IndividualValueList):
                    e = absolutize_entity_name(x)
                    for a in p:
                        i.add_property_assertion(e, str(a))
            for inst_of in individual.is_instance_of:
                p = onto.lookup_prefix(inst_of.namespace.base_iri)
                e2 = absolutize_entity_name(inst_of.name, p)
                i.be_type_of(self.get_entity(e2))
            self.entities[e] = i
        dct = {}
        assign_optional_dct(dct, OWL_CLASS, {abs_name: self.classes[abs_name].to_dict() for abs_name in self.classes})
        assign_optional_dct(dct, OWL_OBJECT_PROPERTY, {abs_name: self.object_properties[abs_name].to_dict()
                                                       for abs_name in self.object_properties})
        assign_optional_dct(dct, OWL_DATA_PROPERTY, {abs_name: self.data_properties[abs_name].to_dict()
                                                     for abs_name in self.data_properties})
        assign_optional_dct(dct, OWL_INDIVIDUAL, {abs_name: self.individuals[abs_name].to_dict()
                                                  for abs_name in self.individuals})
        return dct
