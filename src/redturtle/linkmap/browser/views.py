from json import dumps
from plone import api
from Products.Five import BrowserView
from redturtle.linkmap.linkmap import CATEGORY_C1
from redturtle.linkmap.linkmap import CATEGORY_KEYS
from redturtle.linkmap.linkmap import build_category_map
from redturtle.linkmap.linkmap import ensure_required_root_url
from redturtle.linkmap.linkmap import is_valid_date
from redturtle.linkmap.linkmap import today_date_string
from xml.sax.saxutils import escape


REGISTRY_PREFIX = "redturtle.linkmap.controlpanels.settings.ILinkMapSettings"


def get_linkmap_entries():
    return api.portal.get_registry_record(
        f"{REGISTRY_PREFIX}.entries",
        default="",
    )


def get_data_ultima_modifica():
    value = api.portal.get_registry_record(
        f"{REGISTRY_PREFIX}.data_ultima_modifica",
        default="",
    )
    if is_valid_date(value):
        return value
    return today_date_string()


def build_payload():
    raw_entries = get_linkmap_entries()
    data_ultima_modifica = get_data_ultima_modifica()
    try:
        category_map = build_category_map(raw_entries)
    except ValueError:
        category_map = {}
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
        f"  <data_ultima_modifica>{escape(payload['data_ultima_modifica'])}</data_ultima_modifica>",
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
        self.request.response.setHeader("Content-Type", "application/json; charset=utf-8")
        payload = build_payload()
        return dumps(payload, indent=2, ensure_ascii=False, sort_keys=True)


class ATMapXMLView(BrowserView):
    def __call__(self):
        self.request.response.setHeader("Content-Type", "application/xml; charset=utf-8")
        payload = build_payload()
        return build_xml(payload)
