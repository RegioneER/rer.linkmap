from Acquisition import aq_base
from json import dumps
from plone import api
from Products.Five import BrowserView
from rer.linkmap.linkmap import CATEGORY_C1
from rer.linkmap.linkmap import CATEGORY_KEYS
from rer.linkmap.linkmap import ensure_required_root_url
from rer.linkmap.linkmap import is_valid_date
from rer.linkmap.linkmap import is_valid_url
from rer.linkmap.linkmap import today_date_string
from xml.sax.saxutils import escape
from zExceptions import NotFound

REGISTRY_PREFIX = "rer.linkmap.controlpanels.settings.ILinkMapSettings"
ROOT_KEY = "amministrazione_trasparente"


def get_registry_value(field_name, default=""):
    return api.portal.get_registry_record(
        f"{REGISTRY_PREFIX}.{field_name}",
        default=default,
    )


def get_expose_json():
    return get_registry_value("expose_json", default=True)


def get_expose_xml():
    return get_registry_value("expose_xml", default=True)


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


def build_xml(payload):
    root_open = '<amministrazione_trasparente xmlns="https://guida-servizi.anticorruzione.it/trasparenza">'
    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        root_open,
        f"  <data_ultima_modifica>{escape(payload['data_ultima_modifica'])}"
        "</data_ultima_modifica>",
        "  <map>",
    ]

    category = CATEGORY_C1

    lines.append(f"    <{category}>")
    map_values = payload.get(category, {})
    for map_key in CATEGORY_KEYS:
        map_url = map_values.get(map_key)
        if not map_url:
            continue
        lines.append(f"      <{map_key}>{escape(map_url)}</{map_key}>")
    lines.append(f"    </{category}>")
    lines.extend(["  </map>", "</amministrazione_trasparente>"])
    return "\n".join(lines)


class ATMapJSONView(BrowserView):
    def __call__(self):
        if aq_base(self.context) is not aq_base(api.portal.get()):
            raise NotFound()
        if not get_expose_json():
            raise NotFound("JSON view is not enabled")
        self.request.response.setHeader(
            "Content-Type", "application/json; charset=utf-8"
        )
        payload = build_payload()
        return dumps(payload, indent=2, ensure_ascii=False, sort_keys=True)


class ATMapXMLView(BrowserView):
    def __call__(self):
        if aq_base(self.context) is not aq_base(api.portal.get()):
            raise NotFound()
        if not get_expose_xml():
            raise NotFound("XML view is not enabled")
        self.request.response.setHeader(
            "Content-Type", "application/xml; charset=utf-8"
        )
        payload = build_payload()
        return build_xml(payload)
