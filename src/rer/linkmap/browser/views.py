from Acquisition import aq_base
from json import dumps
from lxml import etree
from plone import api
from Products.Five import BrowserView
from rer.linkmap.linkmap import CATEGORY_C1
from rer.linkmap.linkmap import CATEGORY_KEYS
from rer.linkmap.linkmap import ensure_required_root_url
from rer.linkmap.linkmap import is_valid_date
from rer.linkmap.linkmap import is_valid_url
from rer.linkmap.linkmap import today_date_string
from zExceptions import NotFound

REGISTRY_PREFIX = "rer.linkmap.controlpanels.settings.ILinkMapSettings"
ROOT_KEY = "amministrazione_trasparente"
NAMESPACE = "https://guida-servizi.anticorruzione.it/trasparenza"


def get_registry_value(field_name, default=""):
    return api.portal.get_registry_record(
        f"{REGISTRY_PREFIX}.{field_name}",
        default=default,
    )


def get_expose_json():
    return get_registry_value("expose_json", default=False)


def get_expose_xml():
    return get_registry_value("expose_xml", default=False)


def get_data_ultima_modifica():
    value = get_registry_value("data_ultima_modifica")
    if is_valid_date(value):
        return value
    return today_date_string()


def build_category_map_from_fields():
    """Build category map from individual field values."""
    category_map = {}
    for key in CATEGORY_KEYS:
        value = get_registry_value(key)
        if value and is_valid_url(value.strip()):
            category_map[key] = value.strip()
    return category_map


def build_payload():
    data_ultima_modifica = get_data_ultima_modifica()
    category_map = build_category_map_from_fields()
    ensure_required_root_url(category_map, api.portal.get().absolute_url())

    payload = {
        "data_ultima_modifica": data_ultima_modifica,
        CATEGORY_C1: category_map,
    }
    return payload


def _qname(tag):
    return f"{{{NAMESPACE}}}{tag}"


def _serialize_xml(root):
    return etree.tostring(
        root, xml_declaration=True, encoding="utf-8", pretty_print=True
    ).decode("utf-8")


def build_xml(payload):
    root = etree.Element(_qname("amministrazione_trasparente"), nsmap={None: NAMESPACE})

    data_node = etree.SubElement(root, _qname("data_ultima_modifica"))
    data_node.text = payload["data_ultima_modifica"]

    map_node = etree.SubElement(root, _qname("map"))

    category = CATEGORY_C1
    category_node = etree.SubElement(map_node, _qname(category))
    map_values = payload.get(category, {})
    for map_key in CATEGORY_KEYS:
        map_url = map_values.get(map_key)
        if not map_url:
            continue
        key_node = etree.SubElement(category_node, _qname(map_key))
        key_node.text = map_url

    return _serialize_xml(root)


class ATMapJSONView(BrowserView):
    def __call__(self):
        if aq_base(self.context) is not aq_base(api.portal.get()):
            raise NotFound()
        if not get_expose_json():
            raise NotFound()
        self.request.response.setHeader(
            "Content-Type", "application/json; charset=utf-8"
        )
        payload = build_payload()
        return dumps(payload, indent=2, ensure_ascii=False)


class ATMapXMLView(BrowserView):
    def __call__(self):
        if aq_base(self.context) is not aq_base(api.portal.get()):
            raise NotFound()
        if not get_expose_xml():
            raise NotFound()
        self.request.response.setHeader(
            "Content-Type", "application/xml; charset=utf-8"
        )
        payload = build_payload()
        return build_xml(payload)
