from json import loads
from rer.linkmap.controlpanels.settings import ILinkMapSettings
from defusedxml.ElementTree import fromstring as safe_fromstring

import plone.api
import pytest
from zExceptions import NotFound


@pytest.mark.usefixtures("integration")
class TestLinkMapViews:
    """Test LinkMap JSON and XML view exposure with boolean flags."""

    def test_json_view_returns_schema_shape(self, portal):
        """Test that JSON view returns properly shaped data."""
        plone.api.portal.set_registry_record(
            "expose_json",
            True,
            interface=ILinkMapSettings,
        )
        plone.api.portal.set_registry_record(
            "data_ultima_modifica",
            "17/06/2026",
            interface=ILinkMapSettings,
        )
        plone.api.portal.set_registry_record(
            "amministrazione_trasparente",
            "https://www.example.org/amministrazione-trasparente",
            interface=ILinkMapSettings,
        )
        plone.api.portal.set_registry_record(
            "disposizioni_generali",
            "https://www.example.org/disposizioni-generali",
            interface=ILinkMapSettings,
        )

        view = portal.restrictedTraverse("@@at_map.json")
        output = view()

        assert "application/json" in portal.REQUEST.RESPONSE.getHeader("Content-Type")
        payload = loads(output)
        assert payload["data_ultima_modifica"] == "17/06/2026"
        assert sorted(payload.keys()) == [
            "at_art2_bis_c1",
            "data_ultima_modifica",
        ]
        assert payload["at_art2_bis_c1"]["amministrazione_trasparente"] == (
            "https://www.example.org/amministrazione-trasparente"
        )
        assert payload["at_art2_bis_c1"]["disposizioni_generali"] == (
            "https://www.example.org/disposizioni-generali"
        )

    def test_json_view_disabled_returns_not_found(self, portal):
        """Test that JSON view returns 404 when expose_json is False."""
        plone.api.portal.set_registry_record(
            "expose_json",
            False,
            interface=ILinkMapSettings,
        )
        plone.api.portal.set_registry_record(
            "amministrazione_trasparente",
            "https://www.example.org/amministrazione-trasparente",
            interface=ILinkMapSettings,
        )

        with pytest.raises(NotFound):
            portal.restrictedTraverse("@@at_map.json")()

    def test_xml_view_disabled_returns_not_found(self, portal):
        """Test that XML view returns 404 when expose_xml is False."""
        plone.api.portal.set_registry_record(
            "expose_xml",
            False,
            interface=ILinkMapSettings,
        )
        plone.api.portal.set_registry_record(
            "amministrazione_trasparente",
            "https://www.example.org/amministrazione-trasparente",
            interface=ILinkMapSettings,
        )

        with pytest.raises(NotFound):
            portal.restrictedTraverse("@@at_map.xml")()

    def test_json_view_ensures_required_root_key(self, portal):
        """Test that JSON view adds required amministrazione_trasparente key."""
        plone.api.portal.set_registry_record(
            "expose_json",
            True,
            interface=ILinkMapSettings,
        )
        plone.api.portal.set_registry_record(
            "disposizioni_generali",
            "https://www.example.org/disposizioni-generali",
            interface=ILinkMapSettings,
        )

        payload = loads(portal.restrictedTraverse("@@at_map.json")())

        assert "amministrazione_trasparente" in payload["at_art2_bis_c1"]
        assert (
            payload["at_art2_bis_c1"]["amministrazione_trasparente"]
            == portal.absolute_url()
        )

    def test_xml_view_returns_namespaced_schema_shape(self, portal):
        """Test that XML view returns properly namespaced XML."""
        plone.api.portal.set_registry_record(
            "expose_xml",
            True,
            interface=ILinkMapSettings,
        )
        plone.api.portal.set_registry_record(
            "data_ultima_modifica",
            "18/06/2026",
            interface=ILinkMapSettings,
        )
        plone.api.portal.set_registry_record(
            "amministrazione_trasparente",
            "https://www.example.org/at",
            interface=ILinkMapSettings,
        )
        plone.api.portal.set_registry_record(
            "accesso_civico",
            "https://www.example.org/accesso-civico",
            interface=ILinkMapSettings,
        )

        xml_output = portal.restrictedTraverse("@@at_map.xml")()

        assert "application/xml" in portal.REQUEST.RESPONSE.getHeader("Content-Type")

        ns = {"at": "https://guida-servizi.anticorruzione.it/trasparenza"}
        root = safe_fromstring(xml_output)

        assert (
            root.tag
            == "{https://guida-servizi.anticorruzione.it/trasparenza}amministrazione_trasparente"
        )
        assert root.find("at:data_ultima_modifica", ns).text == "18/06/2026"
        category_node = root.find("at:map/at:at_art2_bis_c1", ns)
        assert category_node is not None
        assert (
            category_node.find("at:amministrazione_trasparente", ns).text
            == "https://www.example.org/at"
        )
        assert (
            category_node.find("at:accesso_civico", ns).text
            == "https://www.example.org/accesso-civico"
        )

    def test_json_view_not_accessible_from_non_root_context(self, portal):
        """Test that JSON view is only accessible from portal root."""
        plone.api.portal.set_registry_record(
            "expose_json",
            True,
            interface=ILinkMapSettings,
        )
        with plone.api.env.adopt_roles(["Manager"]):
            page = plone.api.content.create(
                container=portal,
                type="Document",
                id="test-page",
                title="Test page",
            )

        with pytest.raises((NotFound, AttributeError)):
            page.restrictedTraverse("@@at_map.json")()

    def test_xml_view_not_accessible_from_non_root_context(self, portal):
        """Test that XML view is only accessible from portal root."""
        plone.api.portal.set_registry_record(
            "expose_xml",
            True,
            interface=ILinkMapSettings,
        )
        with plone.api.env.adopt_roles(["Manager"]):
            page = plone.api.content.create(
                container=portal,
                type="Document",
                id="test-page-xml",
                title="Test page xml",
            )

        with pytest.raises((NotFound, AttributeError)):
            page.restrictedTraverse("@@at_map.xml")()

    def test_json_view_with_multiple_fields(self, portal):
        """Test JSON view with multiple category fields."""
        plone.api.portal.set_registry_record(
            "expose_json",
            True,
            interface=ILinkMapSettings,
        )
        fields = {
            "amministrazione_trasparente": "https://example.org/at",
            "bandi_di_concorso": "https://example.org/bandi",
            "personale": "https://example.org/personale",
            "bilanci": "https://example.org/bilanci",
        }
        for field_name, url in fields.items():
            plone.api.portal.set_registry_record(
                field_name,
                url,
                interface=ILinkMapSettings,
            )

        payload = loads(portal.restrictedTraverse("@@at_map.json")())
        c1 = payload["at_art2_bis_c1"]

        for field_name, url in fields.items():
            assert c1[field_name] == url

    def test_xml_view_with_multiple_fields(self, portal):
        """Test XML view with multiple category fields."""
        plone.api.portal.set_registry_record(
            "expose_xml",
            True,
            interface=ILinkMapSettings,
        )
        fields = {
            "amministrazione_trasparente": "https://example.org/at",
            "bandi_di_concorso": "https://example.org/bandi",
            "personale": "https://example.org/personale",
        }
        for field_name, url in fields.items():
            plone.api.portal.set_registry_record(
                field_name,
                url,
                interface=ILinkMapSettings,
            )

        xml_output = portal.restrictedTraverse("@@at_map.xml")()
        ns = {"at": "https://guida-servizi.anticorruzione.it/trasparenza"}
        root = safe_fromstring(xml_output)
        category_node = root.find("at:map/at:at_art2_bis_c1", ns)

        for field_name, url in fields.items():
            element = category_node.find(f"at:{field_name}", ns)
            assert element is not None
            assert element.text == url

    def test_empty_fields_not_included_in_output(self, portal):
        """Test that empty/unset fields are not included in output."""
        plone.api.portal.set_registry_record(
            "expose_json",
            True,
            interface=ILinkMapSettings,
        )
        plone.api.portal.set_registry_record(
            "amministrazione_trasparente",
            "https://example.org/at",
            interface=ILinkMapSettings,
        )
        # disposizioni_generali is not set

        payload = loads(portal.restrictedTraverse("@@at_map.json")())
        c1 = payload["at_art2_bis_c1"]

        assert "amministrazione_trasparente" in c1
        assert "disposizioni_generali" not in c1

    def test_default_expose_flags_are_true(self, portal):
        """Test that expose_json and expose_xml default to True."""
        # Don't explicitly set the flags, verify they default to True
        plone.api.portal.set_registry_record(
            "amministrazione_trasparente",
            "https://example.org/at",
            interface=ILinkMapSettings,
        )

        # Both views should work with defaults
        json_output = portal.restrictedTraverse("@@at_map.json")()
        xml_output = portal.restrictedTraverse("@@at_map.xml")()

        assert loads(json_output)
        assert "amministrazione_trasparente" in xml_output
