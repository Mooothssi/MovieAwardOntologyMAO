from app.models import Film, Country, Language
from dirs import ROOT_DIR
from ontogen import Ontology
from ontogen.converter import OntogenConverter
from ontogen.mixins.base import DjModelOntogenMixin
from ontogen.wrapper import all_subclasses

if __name__ == '__main__':
    converter = OntogenConverter.load_from_spec(ROOT_DIR / "mao.yaml")

    for cls in all_subclasses(DjModelOntogenMixin):
        if cls == DjModelOntogenMixin:
            continue
        for inst in cls.objects.all():
            indiv = cls.model_to_entity(converter.ontology, inst)
            converter.ontology.add_entity(indiv)

    # for f in Language.objects.all():
    #     indiv = Language.model_to_entity(converter.ontology, f)
    #     converter.ontology.add_entity(indiv)
    # for f in Country.objects.all():
    #     indiv = Country.model_to_entity(converter.ontology, f)
    #     converter.ontology.add_entity(indiv)
    # for f in Film.objects.all():
    #     indiv = Film.model_to_entity(converter.ontology, f)
    #     converter.ontology.add_entity(indiv)
    onto: Ontology = converter.sync_with_ontology()
    onto.save_to_file(ROOT_DIR / "mao.owl")
