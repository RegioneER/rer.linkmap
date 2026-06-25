# -*- coding: utf-8 -*-
from defusedxml.ElementTree import fromstring as safe_fromstring
from json import loads
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from rer.linkmap.controlpanels.settings import ILinkMapSettings
from rer.linkmap.testing import RER_LINKMAP_INTEGRATION_TESTING  # noqa: E501
from zExceptions import NotFound

import unittest


class TestLinkmapViews(unittest.TestCase):
    """Test that rer.linkmap is properly installed."""

    layer = RER_LINKMAP_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_json_view_returns_schema_shape(self):
        """Test that JSON view returns properly shaped data."""
        api.portal.set_registry_record(
            "expose_json",
            True,
            interface=ILinkMapSettings,
        )
        api.portal.set_registry_record(
            "data_ultima_modifica",
            "17/06/2026",
            interface=ILinkMapSettings,
        )
        api.portal.set_registry_record(
            "amministrazione_trasparente",
            "https://www.example.org/amministrazione-trasparente",
            interface=ILinkMapSettings,
        )
        api.portal.set_registry_record(
            "disposizioni_generali",
            "https://www.example.org/disposizioni-generali",
            interface=ILinkMapSettings,
        )

        view = api.content.get_view(
            name="at_map.json", context=self.portal, request=self.request
        )
        output = view()

        assert "application/json" in self.request.RESPONSE.getHeader("Content-Type")
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

    def test_json_view_disabled_returns_not_found(self):
        """Test that JSON view returns 404 when expose_json is False."""
        api.portal.set_registry_record(
            "expose_json",
            False,
            interface=ILinkMapSettings,
        )
        api.portal.set_registry_record(
            "amministrazione_trasparente",
            "https://www.example.org/amministrazione-trasparente",
            interface=ILinkMapSettings,
        )

        with self.assertRaises(NotFound):
            api.content.get_view(
                name="at_map.json", context=self.portal, request=self.request
            )()

    def test_xml_view_disabled_returns_not_found(self):
        """Test that XML view returns 404 when expose_xml is False."""
        api.portal.set_registry_record(
            "expose_xml",
            False,
            interface=ILinkMapSettings,
        )
        api.portal.set_registry_record(
            "amministrazione_trasparente",
            "https://www.example.org/amministrazione-trasparente",
            interface=ILinkMapSettings,
        )

        with self.assertRaises(NotFound):
            api.content.get_view(
                name="at_map.xml", context=self.portal, request=self.request
            )()

    def test_json_view_ensures_required_root_key(self):
        """Test that JSON view adds required amministrazione_trasparente key."""
        api.portal.set_registry_record(
            "expose_json",
            True,
            interface=ILinkMapSettings,
        )
        api.portal.set_registry_record(
            "disposizioni_generali",
            "https://www.example.org/disposizioni-generali",
            interface=ILinkMapSettings,
        )

        payload = loads(
            api.content.get_view(
                name="at_map.json", context=self.portal, request=self.request
            )()
        )

        assert "amministrazione_trasparente" in payload["at_art2_bis_c1"]
        assert (
            payload["at_art2_bis_c1"]["amministrazione_trasparente"]
            == self.portal.absolute_url()
        )

    def test_xml_view_returns_namespaced_schema_shape(self):
        """Test that XML view returns properly namespaced XML."""
        api.portal.set_registry_record(
            "expose_xml",
            True,
            interface=ILinkMapSettings,
        )
        api.portal.set_registry_record(
            "data_ultima_modifica",
            "18/06/2026",
            interface=ILinkMapSettings,
        )
        api.portal.set_registry_record(
            "amministrazione_trasparente",
            "https://www.example.org/at",
            interface=ILinkMapSettings,
        )
        api.portal.set_registry_record(
            "accesso_civico",
            "https://www.example.org/accesso-civico",
            interface=ILinkMapSettings,
        )

        xml_output = api.content.get_view(
            name="at_map.xml", context=self.portal, request=self.request
        )()

        assert "application/xml" in self.request.RESPONSE.getHeader("Content-Type")

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

    def test_json_view_not_accessible_from_non_root_context(self):
        """Test that JSON view is only accessible from portal root."""
        api.portal.set_registry_record(
            "expose_json",
            True,
            interface=ILinkMapSettings,
        )
        with api.env.adopt_roles(["Manager"]):
            page = api.content.create(
                container=self.portal,
                type="Document",
                id="test-page",
                title="Test page",
            )

        with self.assertRaises((NotFound, AttributeError)):
            page.restrictedTraverse("@@at_map.json")()

    def test_xml_view_not_accessible_from_non_root_context(self):
        """Test that XML view is only accessible from portal root."""
        api.portal.set_registry_record(
            "expose_xml",
            True,
            interface=ILinkMapSettings,
        )
        with api.env.adopt_roles(["Manager"]):
            page = api.content.create(
                container=self.portal,
                type="Document",
                id="test-page-xml",
                title="Test page xml",
            )

        with self.assertRaises((NotFound, AttributeError)):
            page.restrictedTraverse("@@at_map.xml")()

    def test_json_view_with_multiple_fields(self):
        """Test JSON view with multiple category fields."""
        api.portal.set_registry_record(
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
            api.portal.set_registry_record(
                field_name,
                url,
                interface=ILinkMapSettings,
            )

        payload = loads(
            api.content.get_view(
                name="at_map.json", context=self.portal, request=self.request
            )()
        )
        c1 = payload["at_art2_bis_c1"]

        for field_name, url in fields.items():
            assert c1[field_name] == url

    def test_xml_view_with_multiple_fields(self):
        """Test XML view with multiple category fields."""
        api.portal.set_registry_record(
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
            api.portal.set_registry_record(
                field_name,
                url,
                interface=ILinkMapSettings,
            )

        xml_output = api.content.get_view(
            name="at_map.xml", context=self.portal, request=self.request
        )()
        ns = {"at": "https://guida-servizi.anticorruzione.it/trasparenza"}
        root = safe_fromstring(xml_output)
        category_node = root.find("at:map/at:at_art2_bis_c1", ns)

        for field_name, url in fields.items():
            element = category_node.find(f"at:{field_name}", ns)
            assert element is not None
            assert element.text == url

    def test_empty_fields_not_included_in_output(self):
        """Test that empty/unset fields are not included in output."""
        api.portal.set_registry_record(
            "expose_json",
            True,
            interface=ILinkMapSettings,
        )
        api.portal.set_registry_record(
            "amministrazione_trasparente",
            "https://example.org/at",
            interface=ILinkMapSettings,
        )
        # disposizioni_generali is not set

        payload = loads(
            api.content.get_view(
                name="at_map.json", context=self.portal, request=self.request
            )()
        )
        c1 = payload["at_art2_bis_c1"]

        assert "amministrazione_trasparente" in c1
        assert "disposizioni_generali" not in c1

    def test_default_expose_flags_are_true(self):
        """Test that expose_json and expose_xml default to True."""
        # Don't explicitly set the flags, verify they default to True
        api.portal.set_registry_record(
            "amministrazione_trasparente",
            "https://example.org/at",
            interface=ILinkMapSettings,
        )

        # Both views should work with defaults
        json_output = api.content.get_view(
            name="at_map.json", context=self.portal, request=self.request
        )()
        xml_output = api.content.get_view(
            name="at_map.xml", context=self.portal, request=self.request
        )()

        assert loads(json_output)
        assert "amministrazione_trasparente" in xml_output
