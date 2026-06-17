from json import loads
from redturtle.linkmap.controlpanels.settings import ILinkMapSettings
from xml.etree import ElementTree as ET

import plone.api
import pytest


@pytest.mark.usefixtures("integration")
class TestLinkMapViews:
    def test_json_view_returns_schema_shape(self, portal):
        plone.api.portal.set_registry_record(
            "data_ultima_modifica",
            "17/06/2026",
            interface=ILinkMapSettings,
        )
        plone.api.portal.set_registry_record(
            "entries",
            "amministrazione_trasparente|https://www.example.org/amministrazione-trasparente\n"
            "disposizioni_generali|https://www.example.org/disposizioni-generali",
            interface=ILinkMapSettings,
        )

        view = portal.restrictedTraverse("@@at_map.json")
        output = view()

        assert "application/json" in portal.REQUEST.RESPONSE.getHeader("Content-Type")
        payload = loads(output)
        assert payload["data_ultima_modifica"] == "17/06/2026"
        assert list(payload.keys()) == ["at_art2_bis_c1", "data_ultima_modifica"]
        assert payload["at_art2_bis_c1"]["amministrazione_trasparente"] == (
            "https://www.example.org/amministrazione-trasparente"
        )

    def test_json_view_ensures_required_root_key(self, portal):
        plone.api.portal.set_registry_record(
            "entries",
            "disposizioni_generali|https://www.example.org/disposizioni-generali",
            interface=ILinkMapSettings,
        )

        payload = loads(portal.restrictedTraverse("@@at_map.json")())

        assert "amministrazione_trasparente" in payload["at_art2_bis_c1"]
        assert payload["at_art2_bis_c1"]["amministrazione_trasparente"] == portal.absolute_url()

    def test_xml_view_returns_namespaced_schema_shape(self, portal):
        plone.api.portal.set_registry_record(
            "data_ultima_modifica",
            "18/06/2026",
            interface=ILinkMapSettings,
        )
        plone.api.portal.set_registry_record(
            "entries",
            "amministrazione_trasparente|https://www.example.org/at\n"
            "accesso_civico|https://www.example.org/accesso-civico",
            interface=ILinkMapSettings,
        )

        xml_output = portal.restrictedTraverse("@@at_map.xml")()

        assert "application/xml" in portal.REQUEST.RESPONSE.getHeader("Content-Type")

        ns = {"at": "https://guida-servizi.anticorruzione.it/trasparenza"}
        root = ET.fromstring(xml_output)

        assert root.tag == "{https://guida-servizi.anticorruzione.it/trasparenza}amministrazione_trasparente"
        assert root.find("at:data_ultima_modifica", ns).text == "18/06/2026"
        category_node = root.find("at:map/at:at_art2_bis_c1", ns)
        assert category_node is not None
        assert category_node.find("at:amministrazione_trasparente", ns).text == "https://www.example.org/at"
        assert category_node.find("at:accesso_civico", ns).text == "https://www.example.org/accesso-civico"
